"""Intent routing for the SOULbox Spirit."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class IntentRoute:
    """Resolved routing information for an intent."""

    ritual_name: str
    scopes: List[str] = field(default_factory=list)
    post_actions: List[Dict[str, str]] = field(default_factory=list)
    description: Optional[str] = None


def safe_get(data: dict, key: str) -> str:
    value = data.get(key)
    if not value:
        raise ValueError(f"Missing required field '{key}'")
    return str(value)


class IntentRouter:
    """Maps high-level intents to ritual files and follow-up actions."""

    def __init__(self, rituals_dir: Path, mapping_path: Optional[Path] = None):
        self.rituals_dir = rituals_dir
        self.mapping_path = mapping_path or rituals_dir.parent / "intent_map.json"
        self._routes: Dict[str, IntentRoute] = {}
        self._load_routes()

    def _load_routes(self) -> None:
        """Load intent routes from JSON mapping if available."""
        if self.mapping_path.exists():
            data = json.loads(self.mapping_path.read_text(encoding="utf-8"))
            for intent, payload in data.items():
                self._routes[intent] = IntentRoute(
                    ritual_name=payload["ritual"],
                    scopes=payload.get("scopes", []),
                    post_actions=payload.get("post_actions", []),
                    description=payload.get("description"),
                )
        else:
            # Minimal defaults to bootstrap the spirit
            self._routes = {
                "soul_init": IntentRoute(
                    ritual_name="soul_init",
                    scopes=["memory", "growth_tracking", "voice_tuning"],
                    description="Initialize the SOULbox spirit and establish the consent contract.",
                ),
                "growing_soul": IntentRoute(
                    ritual_name="growing_soul",
                    scopes=["growth_analysis", "interaction_patterns"],
                    description="Assess the evolution of the therapeutic relationship.",
                ),
                "ember_capture": IntentRoute(
                    ritual_name="ember_capture",
                    scopes=["memory", "ember_marking"],
                    description="Capture a notable moment as an Ember artifact.",
                ),
                "voice_tune": IntentRoute(
                    ritual_name="voice_tune",
                    scopes=["voice_calibration", "tone_adjustment"],
                    description="Adjust persona tone to better match the operator's needs.",
                ),
                "zone_manager": IntentRoute(
                    ritual_name="zone_manager",
                    scopes=["zone_management"],
                    description="Review or adjust containment zones and trust boundaries.",
                ),
            }

    def available_intents(self) -> Dict[str, IntentRoute]:
        """Return the currently known intents."""
        return self._routes

    def get_route(self, intent: str) -> Optional[IntentRoute]:
        """Retrieve routing information for the intent."""
        return self._routes.get(intent)

    def refresh(self) -> None:
        """Reload mapping from disk."""
        self._routes.clear()
        self._load_routes()
