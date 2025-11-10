"""Dispatch post-ritual actions through consent-aware connectors."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .consent_policy import ConsentDecision, ConsentPolicy
from ..connectors import (
    APIClientConnector,
    MCPBridgeConnector,
    UIAutomationConnector,
    LocalLLMConnector,
)

LOGGER = logging.getLogger(__name__)


@dataclass
class ActionResult:
    """Outcome of a dispatched action."""

    action: Dict[str, Any]
    success: bool
    response: Dict[str, Any]
    decision: ConsentDecision

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "success": self.success,
            "response": self.response,
            "decision": self.decision.to_dict(),
        }


class ActionDispatcher:
    """Routes consented actions to the appropriate connector."""

    def __init__(self, consent_policy: ConsentPolicy) -> None:
        self.consent_policy = consent_policy
        self.api = APIClientConnector()
        self.mcp = MCPBridgeConnector()
        self.ui = UIAutomationConnector()

        llm_base_url = os.getenv("SOULBOX_LLM_URL", "http://127.0.0.1:1234")
        llm_model = os.getenv("SOULBOX_LLM_MODEL", "local-llm")
        llm_dry_run = os.getenv("SOULBOX_LLM_DRY_RUN", "true").lower() not in {"false", "0", "no"}
        self.llm = LocalLLMConnector(base_url=llm_base_url, model=llm_model, dry_run=llm_dry_run)

        prefs_env = os.getenv("SOULBOX_LLM_PREFS")
        self.model_preferences_path = Path(prefs_env) if prefs_env else Path(__file__).resolve().parent.parent / "model_preferences.json"
        self.model_preferences = self._load_model_preferences()

        self._handlers = {
            "api": self._handle_api,
            "mcp": self._handle_mcp,
            "ui": self._handle_ui,
            "llm": self._handle_llm,
        }

    # ------------------------------------------------------------------
    def dispatch(self, actions: Iterable[Dict[str, Any]], *, intent: str, context: Dict[str, Any]) -> List[ActionResult]:
        results: List[ActionResult] = []
        for action in actions:
            action_type = action.get("type")
            scope = action.get("scope") or f"connector:{action_type}"
            decision = self.consent_policy.evaluate(
                scopes=[scope],
                context={**context, "action": action},
                intent=f"connector::{intent}",
                message=action.get("description", ""),
            )
            if not decision.allowed:
                LOGGER.warning("Consent denied for action %s: %s", action_type, decision.reason)
                results.append(
                    ActionResult(
                        action=action,
                        success=False,
                        response={"error": decision.reason},
                        decision=decision,
                    )
                )
                continue

            handler = self._handlers.get(action_type)
            if not handler:
                msg = f"Unknown action type '{action_type}'"
                LOGGER.error(msg)
                results.append(
                    ActionResult(
                        action=action,
                        success=False,
                        response={"error": msg},
                        decision=decision,
                    )
                )
                continue

            try:
                response = handler(action)
                results.append(
                    ActionResult(
                        action=action,
                        success=True,
                        response=response,
                        decision=decision,
                    )
                )
            except Exception as exc:  # pragma: no cover - defensive
                LOGGER.exception("Failed to execute %s action", action_type)
                results.append(
                    ActionResult(
                        action=action,
                        success=False,
                        response={"error": str(exc)},
                        decision=decision,
                    )
                )
        return results

    # ------------------------------------------------------------------
    def _handle_api(self, action: Dict[str, Any]) -> Dict[str, Any]:
        from .intent_router import safe_get

        request = self.api.create_request(
            endpoint=safe_get(action, "endpoint"),
            method=action.get("method", "GET"),
            payload=action.get("payload"),
            headers=action.get("headers"),
        )
        return self.api.execute(request)

    def _handle_mcp(self, action: Dict[str, Any]) -> Dict[str, Any]:
        return self.mcp.execute_request(
            agent_id=action.get("agent_id", "unknown"),
            message=action.get("message", ""),
            metadata=action.get("metadata") or {},
        )

    def _handle_ui(self, action: Dict[str, Any]) -> Dict[str, Any]:
        return self.ui.execute_macro(
            description=action.get("description", "UI automation"),
            steps=action.get("steps", []),
        )

    def _handle_llm(self, action: Dict[str, Any]) -> Dict[str, Any]:
        from ..connectors.local_llm import ChatMessage

        messages_data = action.get("messages")
        system_prompt = action.get("system_prompt")
        temperature = float(action.get("temperature", 0.2))
        selected_model = self._select_llm_model(action)

        if messages_data:
            messages = [
                ChatMessage(role=item.get("role", "user"), content=item.get("content", ""))
                for item in messages_data
            ]
        else:
            prompt = action.get("prompt")
            if not prompt:
                raise ValueError("LLM action requires 'prompt' or 'messages'")
            messages = [ChatMessage(role="user", content=str(prompt))]

        response = self.llm.chat_completion(
            messages=messages,
            system_prompt=system_prompt,
            temperature=temperature,
            model=selected_model,
        )
        response.setdefault("model", selected_model)
        return response

    # ------------------------------------------------------------------
    def _load_model_preferences(self) -> Dict[str, str]:
        if self.model_preferences_path.exists():
            try:
                return json.loads(self.model_preferences_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                LOGGER.warning("Failed to parse model preferences at %s", self.model_preferences_path)
        return {}

    def _select_llm_model(self, action: Dict[str, Any]) -> str:
        if model := action.get("model"):
            return str(model)
        purpose = action.get("purpose") or action.get("capability")
        if purpose and purpose in self.model_preferences:
            return self.model_preferences[purpose]
        return self.model_preferences.get("default", self.llm.model)
