from __future__ import annotations

import time
import uuid
from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException

from alignai.exception import APIError
from alignai.proto.ingestion.v1alpha.event_pb2 import Event
from alignai.proto.ingestion.v1alpha.ingestion_pb2 import CollectEventsRequest


class APIClient:
    def __init__(self, api_host: str, api_key: str, api_max_retries: int):
        self.endpoint = urljoin(api_host, "/ingestion.v1alpha.IngestionService/CollectEvents")
        self.api_key = api_key
        self.api_max_retries = api_max_retries

    def send_events(self, events: list[Event]) -> None:
        pb_payload = CollectEventsRequest(request_id=uuid.uuid4().hex, events=events)
        payload = pb_payload.SerializeToString()
        for attempt in range(self.api_max_retries):
            try:
                resp = requests.post(
                    url=self.endpoint,
                    data=payload,
                    headers={"Content-Type": "application/proto", "Authorization": f"Bearer {self.api_key}"},
                    timeout=10,
                )
                status_code = resp.status_code
                if status_code == 200:
                    return
                else:
                    raise APIError(status_code=status_code, err_msg=resp.text)
            except (RequestException, APIError) as e:
                if isinstance(e, APIError) and (400 <= e.status_code < 500) and e.status_code != 429:
                    raise
                if attempt < self.api_max_retries - 1:
                    time.sleep(2**attempt)  # exponential back-off
                    continue
                else:
                    raise
