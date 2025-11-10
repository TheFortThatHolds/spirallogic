"""Consent policy enforcement for the SOULbox Spirit."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ConsentDecision:
    """Outcome of a consent policy evaluation."""

    allowed: bool
    reason: str
    scopes: List[str]
    intent: str
    message: str = ""
    escalation_required: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allowed": self.allowed,
            "reason": self.reason,
            "scopes": self.scopes,
            "intent": self.intent,
            "message": self.message,
            "escalation_required": self.escalation_required,
        }


class ConsentPolicy:
    """Evaluates consent scopes against configurable policy rules."""

    def __init__(self, log_path: Path, policy_path: Optional[Path] = None) -> None:
        self.log_path = log_path
        self.policy_path = policy_path or log_path.parent / "consent_policy.json"
        self._policy = self._load_policy()

    # ------------------------------------------------------------------
    def evaluate(
        self,
        *,
        scopes: Iterable[str],
        context: Optional[Dict[str, Any]] = None,
        intent: str,
        message: str = "",
    ) -> ConsentDecision:
        scopes = list(scopes or [])
        context = context or {}

        if not scopes:
            decision = ConsentDecision(
                allowed=True,
                reason="No scopes requested",
                scopes=[],
                intent=intent,
                message=message,
            )
            self._log_decision(decision, context)
            return decision

        blocked = set(scope for scope in scopes if scope in self._policy.get("blocked_scopes", []))
        manual = set(scope for scope in scopes if scope in self._policy.get("require_manual", []))

        if blocked:
            decision = ConsentDecision(
                allowed=False,
                reason=f"Blocked scopes: {', '.join(sorted(blocked))}",
                scopes=scopes,
                intent=intent,
                message=message,
            )
        elif manual:
            decision = ConsentDecision(
                allowed=False,
                reason=f"Manual review required for scopes: {', '.join(sorted(manual))}",
                scopes=scopes,
                intent=intent,
                message=message,
                escalation_required=True,
            )
        else:
            decision = ConsentDecision(
                allowed=True,
                reason="Scopes permitted by policy",
                scopes=scopes,
                intent=intent,
                message=message,
            )

        self._log_decision(decision, context)
        return decision

    # ------------------------------------------------------------------
    def _load_policy(self) -> Dict[str, Any]:
        if self.policy_path.exists():
            try:
                return json.loads(self.policy_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        return {
            "blocked_scopes": [],
            "require_manual": ["ui_automation", "high_risk_sharing"],
        }

    def _log_decision(self, decision: ConsentDecision, context: Dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "consent_policy",
            "intent": decision.intent,
            "decision": decision.to_dict(),
            "context": context,
        }
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
