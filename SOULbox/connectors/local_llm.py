"""Connector for local LM Studio models using OpenAI-compatible APIs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib import error, request


@dataclass
class ChatMessage:
    role: str
    content: str


class LocalLLMConnector:
    """Calls a local LM Studio instance, defaulting to dry-run for safety."""

    def __init__(
        self,
        *,
        base_url: str = "http://127.0.0.1:1234",
        model: str = "local-llm",
        dry_run: bool = True,
        timeout: int = 30,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.dry_run = dry_run
        self.timeout = timeout
        self.last_payload: Optional[Dict[str, Any]] = None

    # ------------------------------------------------------------------
    def chat_completion(
        self,
        *,
        messages: List[ChatMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        selected_model = model or self.model
        payload: Dict[str, Any] = {
            "model": selected_model,
            "messages": [msg.__dict__ for msg in messages],
            "temperature": temperature,
        }
        if system_prompt:
            payload.setdefault("messages", [])
            payload["messages"].insert(0, {"role": "system", "content": system_prompt})

        if self.dry_run:
            self.last_payload = payload
            return {
                "status": "dry_run",
                "model": selected_model,
                "messages": payload["messages"],
            }

        self.last_payload = payload
        endpoint = f"{self.base_url}/v1/chat/completions"
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        req = request.Request(endpoint, data=data, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:  # type: ignore[arg-type]
                body = json.loads(resp.read().decode("utf-8"))
                return {
                    "status": resp.status,
                    "response": body,
                }
        except error.HTTPError as exc:
            return {
                "status": exc.code,
                "error": exc.read().decode("utf-8", errors="replace"),
            }
        except error.URLError as exc:
            return {
                "status": "error",
                "error": getattr(exc, "reason", str(exc)),
            }

    def list_models(self) -> Dict[str, Any]:
        """Return the LM Studio model catalog."""
        endpoint = f"{self.base_url}/v1/models"
        req = request.Request(endpoint, method="GET")
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:  # type: ignore[arg-type]
                body = json.loads(resp.read().decode("utf-8"))
                return {"status": resp.status, "response": body}
        except error.HTTPError as exc:
            return {"status": exc.code, "error": exc.read().decode("utf-8", errors="replace")}
        except error.URLError as exc:
            return {"status": "error", "error": getattr(exc, "reason", str(exc))}
