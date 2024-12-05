import logging

import requests
from typing import Optional, List
import json
import os
import boto3
from requests import Response
from requests.auth import AuthBase
from aws_requests_auth.aws_auth import AWSRequestsAuth
from typing import Dict, Any

from nora_lib.interactions.models import (
    AnnotationBatch,
    StepCost,
    Event,
    Message,
    ReturnedMessage,
    ReturnedEvent,
    Thread,
    ThreadRelationsResponse,
    VirtualThread,
)


class InteractionsService:
    """
    Service which saves interactions to the Interactions API
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        token: Optional[str] = None,
        auth: Optional[AuthBase] = None,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        if auth:
            self.auth = auth
        elif token:
            self.auth = BearerAuth(token)
        else:
            raise Exception("Either token or auth must be provided")

    def _post(self, url: str, json: Dict[str, Any]) -> Response:
        return requests.post(
            url,
            json=json,
            auth=self.auth,
            timeout=self.timeout,
        )

    def save_message(
        self, message: Message, virtual_thread_id: Optional[str] = None
    ) -> None:
        """
        Save a message to the Interaction Store
        :param virtual_thread_id: Optional ID of a virtual thread to associate with the message
        """
        message_url = f"{self.base_url}/interaction/v1/message"
        response = self._post(
            message_url,
            message.model_dump(),
        )
        response.raise_for_status()
        if virtual_thread_id:
            # Use an event to tag the message with the virtual thread ID
            event = Event(
                type=VirtualThread.EVENT_TYPE,
                actor_id=message.actor_id,
                message_id=message.message_id,
                data={
                    VirtualThread.ID_FIELD: virtual_thread_id,
                    VirtualThread.EVENT_TYPE_FIELD: VirtualThread.EVENT_TYPE,
                },
                timestamp=message.ts,
            )
            self.save_event(event)

    def save_event(self, event: Event, virtual_thread_id: Optional[str] = None) -> str:
        """
        Save an event to the Interaction Store. Returns an event id.
        :param virtual_thread_id: Optional ID of a virtual thread to associate with the event
        """
        event_url = f"{self.base_url}/interaction/v1/event"
        response = self._post(
            event_url,
            event.model_dump(),
        )
        response.raise_for_status()
        if virtual_thread_id:
            # Use an event to tag the event with the virtual thread ID
            # Attach it to the same message as this event, along with the event type
            event = Event(
                type=VirtualThread.EVENT_TYPE,
                actor_id=event.actor_id,
                message_id=event.message_id,
                data={
                    VirtualThread.ID_FIELD: virtual_thread_id,
                    VirtualThread.EVENT_TYPE_FIELD: event.type,
                },
                timestamp=event.timestamp,
            )
            self.save_event(event)
        response_message = json.loads(response.text)
        event_id = response_message["event_id"]
        return event_id

    def save_thread(self, thread: Thread) -> None:
        """Save a thread to the Interactions API"""
        thread_url = f"{self.base_url}/interaction/v1/thread"
        response = self._post(
            thread_url,
            thread.model_dump(),
        )
        response.raise_for_status()

    def get_virtual_thread_content(
        self, message_id: str, virtual_thread_id: str
    ) -> List[ReturnedMessage]:
        """Fetch all messages and events in a virtual thread
        Returns all messages and events in the same thread as the given message,
        but filtered to only include those associated with the given virtual thread.
        :param message_id: The ID of a message in the virtual thread
        :param virtual_thread_id: The ID of the virtual thread
        """
        message_search_url = f"{self.base_url}/interaction/v1/search/message"
        # Fetch all events and filter on the client side
        # Need an IStore schema change to do this server-side
        request_body = {
            "id": message_id,
            "relations": {
                "preceding_messages": {
                    "max": 100,
                    "relations": {"events": {}},
                },
                "events": {},
            },
        }

        response = self._post(
            message_search_url,
            request_body,
        )
        response.raise_for_status()
        result = ReturnedMessage.model_validate(response.json()["message"])
        all_messages = result.preceding_messages + [result]
        virtual_thread_content = []
        for msg in all_messages:
            event_types_in_virtual_thread = set(
                event.data[VirtualThread.EVENT_TYPE_FIELD]
                for event in msg.events
                if event.type == VirtualThread.EVENT_TYPE
                and event.data.get(VirtualThread.ID_FIELD) == virtual_thread_id
            )
            if not event_types_in_virtual_thread:
                continue
            virtual_thread_content.append(msg)
            msg.events = [
                event
                for event in msg.events
                if event.type != VirtualThread.EVENT_TYPE
                and event.type in event_types_in_virtual_thread
            ]
            if VirtualThread.EVENT_TYPE not in event_types_in_virtual_thread:
                # An event has been tagged with the virtual thread ID
                # but the message itself is not in the virtual thread
                # Somewhat pathological case, probably shouldn't happen
                # Set the message text to empty string
                msg.text = ""
        return virtual_thread_content

    def save_annotation(self, annotation: AnnotationBatch) -> None:
        """Save an annotation to the Interactions API"""
        annotation_url = f"{self.base_url}/interaction/v1/annotation"
        response = self._post(
            annotation_url,
            annotation.model_dump(),
        )
        response.raise_for_status()

    def get_message(self, message_id: str) -> ReturnedMessage:
        """Fetch a message from the Interactions API"""
        message_url = f"{self.base_url}/interaction/v1/search/message"
        request_body = {
            "id": message_id,
            "relations": {"thread": {}, "channel": {}, "events": {}, "annotations": {}},
        }
        response = self._post(
            message_url,
            request_body,
        )
        response.raise_for_status()
        res_dict = response.json()["message"]
        res = ReturnedMessage.model_validate(res_dict)

        # thread_id and channel_id are for some reason nested in the response
        if not res.thread_id:
            res.thread_id = res_dict.get("thread", {}).get("thread_id")
        if not res.channel_id:
            res.channel_id = res_dict.get("channel", {}).get("channel_id")

        return res

    def get_event(self, event_id: str) -> ReturnedEvent:
        """Fetch an event from the Interactions API"""
        event_url = f"{self.base_url}/interaction/v1/search/event"
        request_body = {
            "id": event_id,
        }
        response = self._post(
            event_url,
            request_body,
        )
        response.raise_for_status()
        res_dict = response.json()["events"][0]
        res = ReturnedEvent.model_validate(res_dict)
        return res

    def fetch_all_threads_by_channel(
        self,
        channel_id: str,
        min_timestamp: Optional[str] = None,
        thread_event_types: Optional[list[str]] = None,
        most_recent: Optional[int] = None,
    ) -> dict:
        """Fetch a message from the Interactions API"""
        message_url = f"{self.base_url}/interaction/v1/search/channel"
        request_body = self._channel_lookup_request(
            channel_id=channel_id,
            min_timestamp=min_timestamp,
            thread_event_types=thread_event_types,
            most_recent=most_recent,
        )
        response = self._post(
            message_url,
            request_body,
        )
        response.raise_for_status()
        return response.json()

    def fetch_thread_messages_and_events_for_message(
        self,
        message_id: str,
        event_types: List[str],
        min_timestamp: Optional[str] = None,
        most_recent: Optional[int] = None,
    ) -> ThreadRelationsResponse:
        """Fetch messages sorted by timestamp and events for agent context"""
        message_url = f"{self.base_url}/interaction/v1/search/message"
        request_body = self._thread_lookup_request(
            message_id,
            event_types=event_types,
            min_timestamp=min_timestamp,
            most_recent=most_recent,
        )
        response = self._post(
            message_url,
            request_body,
        )
        response.raise_for_status()
        json_response = response.json()

        return ThreadRelationsResponse.model_validate(
            json_response.get("message", {}).get("thread", {})
        )

    def fetch_messages_and_events_for_thread(
        self,
        thread_id: str,
        event_type: Optional[str] = None,
        min_timestamp: Optional[str] = None,
    ) -> dict:
        """Fetch messages and events for the given thread from the Interactions API"""
        thread_search_url = f"{self.base_url}/interaction/v1/search/thread"
        message_query = {
            "filter": {"min_timestamp": min_timestamp} if min_timestamp else None,
            "apply_annotations_from_actors": ["*"],
        }
        request_body = {
            "id": thread_id,
            "relations": {
                "messages": message_query,
                "events": {"filter": {"type": event_type}} if event_type else {},
            },
        }

        response = self._post(
            thread_search_url,
            request_body,
        )
        response.raise_for_status()
        return response.json()

    def fetch_events_for_message(
        self,
        message_id: str,
        event_type: Optional[str] = None,
    ) -> dict:
        """Fetch messages and events for the thread containing a given message from the Interactions API"""
        message_search_url = f"{self.base_url}/interaction/v1/search/message"
        request_body = {
            "id": message_id,
            "relations": {
                "events": {"filter": {"type": event_type}} if event_type else {},
            },
        }

        response = self._post(
            message_search_url,
            request_body,
        )
        response.raise_for_status()
        return response.json()

    def fetch_all_by_channel(
        self,
        channel_id: str,
        min_timestamp: Optional[str] = None,
        event_types: Optional[List[str]] = None,
        most_recent: Optional[int] = None,
    ) -> dict:
        """
        Fetch all threads, messages, and events including nested ones for a given channel
        """
        channel_search_url = f"{self.base_url}/interaction/v1/search/channel"
        event_query = {"filter": None if event_types is None else {"type": event_types}}
        message_filter_query = {
            "min_timestamp": min_timestamp if min_timestamp else None,
            "most_recent": most_recent if most_recent else None,
        }
        message_query = {
            "relations": {"events": event_query, "annotations:": {}},
            "filter": message_filter_query,
            "apply_annotations_from_actors": ["*"],
        }
        request_body = {
            "id": channel_id,
            "relations": {
                "threads": {
                    "relations": {
                        "messages": message_query,
                        "events": event_query,
                    }
                },
            },
        }
        response = self._post(
            channel_search_url,
            request_body,
        )
        response.raise_for_status()
        return response.json()

    def fetch_all_by_thread(
        self,
        thread_id: str,
        min_timestamp: Optional[str] = None,
        event_types: Optional[List[str]] = None,
        most_recent: Optional[int] = None,
    ) -> dict:
        """
        Fetch all messages and events including nested ones for a given thread
        """
        thread_search_url = f"{self.base_url}/interaction/v1/search/thread"
        event_query = {"filter": None if event_types is None else {"type": event_types}}
        message_filter_query = {
            "min_timestamp": min_timestamp if min_timestamp else None,
            "most_recent": most_recent if most_recent else None,
        }
        message_query = {
            "relations": {"events": event_query, "annotations:": {}},
            "filter": message_filter_query,
            "apply_annotations_from_actors": ["*"],
        }
        request_body = {
            "id": thread_id,
            "relations": {
                "messages": message_query,
                "events": event_query,
            },
        }
        response = self._post(
            thread_search_url,
            request_body,
        )
        response.raise_for_status()
        return response.json()

    def report_cost(self, step_cost: StepCost) -> Optional[str]:
        """Save a cost report to the Interactions Store. Returning event id"""
        try:
            return self.save_event(step_cost.to_event())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logging.warning(
                    f"Cannot find message id {step_cost.message_id} to attach cost report to."
                )
                return None
            else:
                raise e

    @staticmethod
    def _channel_lookup_request(
        channel_id: str,
        min_timestamp: Optional[str] = None,
        thread_event_types: Optional[list[str]] = None,
        most_recent: Optional[int] = None,
    ) -> dict:
        """Interaction service API request to get threads and messages for a channel"""
        message_filter_query = {
            "min_timestamp": min_timestamp if min_timestamp else None,
            "most_recent": most_recent if most_recent else None,
        }
        return {
            "id": channel_id,
            "relations": {
                "threads": {
                    "relations": {
                        "messages": {
                            "filter": message_filter_query,
                            "apply_annotations_from_actors": ["*"],
                        },
                        "events": {"filter": {"type": thread_event_types or []}},
                    }
                }
            },
        }

    @staticmethod
    def _thread_lookup_request(
        message_id: str,
        event_types: list[str],
        min_timestamp: Optional[str] = None,
        most_recent: Optional[int] = None,
    ) -> dict:
        """will return all messages for the thread containing the given message and events associated with each message"""
        message_filter_query = {
            "min_timestamp": min_timestamp if min_timestamp else None,
            "most_recent": most_recent if most_recent else None,
        }
        return {
            "id": message_id,
            "relations": {
                "thread": {
                    "relations": {
                        "messages": {
                            "filter": message_filter_query,
                            "relations": {"events": {"filter": {"type": event_types}}},
                            "apply_annotations_from_actors": ["*"],
                        },
                    }
                }
            },
        }

    @staticmethod
    def fetch_bearer_token(secret_id: str) -> str:
        secrets_manager = boto3.client("secretsmanager", region_name="us-west-2")
        return json.loads(
            secrets_manager.get_secret_value(SecretId=secret_id)["SecretString"]
        )["token"]

    @staticmethod
    def from_env() -> "InteractionsService":
        """Load the configuration based on the environment."""
        url = os.getenv(
            "INTERACTION_STORE_URL",
            "https://nora-retrieval-public.prod.s2.allenai.org",
        )
        token = os.getenv(
            "INTERACTION_STORE_TOKEN",
            InteractionsService.fetch_bearer_token(
                "nora/prod/interaction-bearer-token"
            ),
        )

        return InteractionsService(base_url=url, token=token)


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r
