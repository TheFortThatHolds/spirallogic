"""Connector for consent-gated UI automation (stubbed)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class UIAction:
    description: str
    steps: List[str]
    metadata: Optional[Dict[str, Any]] = None


class UIAutomationConnector:
    """Records requested UI automation flows instead of executing them."""

    def __init__(self) -> None:
        self.last_macro: Optional[UIAction] = None

    def execute_macro(self, *, description: str, steps: List[str], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        action = UIAction(description=description, steps=steps, metadata=metadata)
        self.last_macro = action
        # TODO: Integrate with automation tooling under strict consent scopes
        return {
            "status": "stubbed",
            "description": action.description,
            "steps": action.steps,
            "metadata": action.metadata or {},
        }
