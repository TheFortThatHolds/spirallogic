"""HTTP connector governed by consent scopes."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class APIRequest:
    endpoint: str
    method: str = "GET"
    payload: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None


class APIClientConnector:
    """HTTP client with opt-in dry-run mode."""

    def __init__(self, *, dry_run: bool = True, timeout: int = 15) -> None:
        self.dry_run = dry_run
        self.timeout = timeout
        self.last_request: Optional[APIRequest] = None

    def create_request(
        self,
        *,
        endpoint: str,
        method: str = "GET",
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIRequest:
        if not endpoint:
            raise ValueError("API endpoint required")
        return APIRequest(endpoint=endpoint, method=method.upper(), payload=payload, headers=headers)

    def execute(self, request: APIRequest) -> Dict[str, Any]:
        if self.dry_run:
            self.last_request = request
            return {
                "status": "dry_run",
                "endpoint": request.endpoint,
                "method": request.method,
                "payload": request.payload,
            }

        self.last_request = request
        return self._perform_http_call(request)

    def _perform_http_call(self, request: APIRequest) -> Dict[str, Any]:
        import urllib.error
        import urllib.request

        data = None
        headers = request.headers or {}
        if request.payload is not None:
            data = json.dumps(request.payload).encode("utf-8")
            headers.setdefault("Content-Type", "application/json")

        http_request = urllib.request.Request(
            request.endpoint,
            data=data,
            method=request.method,
            headers=headers,
        )

        try:
            with urllib.request.urlopen(http_request, timeout=self.timeout) as response:  # type: ignore[arg-type]
                body = response.read().decode("utf-8")
                return {
                    "status": response.status,
                    "body": body,
                    "headers": dict(response.headers),
                }
        except urllib.error.HTTPError as exc:
            return {
                "status": exc.code,
                "body": exc.read().decode("utf-8", errors="replace"),
            }
        except urllib.error.URLError as exc:
            return {
                "status": "error",
                "error": str(exc.reason) if hasattr(exc, "reason") else str(exc),
            }
