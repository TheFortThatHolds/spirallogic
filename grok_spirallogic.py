#!/usr/bin/env python3
"""
GROK's SpiralLogic implementation - JSON-schema aligned proof of concept.

This pared-down runtime is intended to mirror the data structures expected by
`spirallogic_runtime.SpiralLogic` while remaining lightweight enough for rapid
demos. Rituals are described with the interim JSON schema that current
SpiralLogic examples use (until the dedicated syntax parser ships).
"""

from __future__ import annotations

import json
import hashlib
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from unicode_sanitizer import sanitize_for_windows_terminal

# ---------------------------------------------------------------------------
# Exceptions & validation helpers
# ---------------------------------------------------------------------------

class SchemaError(Exception):
    """Raised when a ritual fails JSON schema validation."""


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise SchemaError(message)


def _expect_type(value: Any, expected_type: Any, path: str) -> None:
    if not isinstance(value, expected_type):
        expected_name = getattr(expected_type, "__name__", str(expected_type))
        raise SchemaError(f"{path} must be {expected_name}")


STEP_TYPES = {
    "consent.request",
    "voice.speak",
    "memory.store",
    "memory.recall",
    "crisis.detect",
}


def validate_ritual_schema(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Validate ritual JSON against the interim schema and normalise defaults."""

    _expect_type(raw, dict, "ritual")
    _expect("intent" in raw, "ritual.intent is required")
    _expect("voice" in raw, "ritual.voice is required")
    _expect("phase" in raw, "ritual.phase is required")
    _expect("steps" in raw, "ritual.steps is required")

    intent = raw["intent"]
    voice = raw["voice"]
    phase = raw["phase"]
    steps = raw["steps"]

    _expect_type(intent, str, "ritual.intent")
    _expect_type(voice, str, "ritual.voice")
    _expect_type(phase, str, "ritual.phase")
    _expect_type(steps, list, "ritual.steps")
    _expect(steps, "ritual.steps cannot be empty")

    validated_steps: List[Dict[str, Any]] = []
    for index, step in enumerate(steps):
        path = f"ritual.steps[{index}]"
        _expect_type(step, dict, path)
        _expect("type" in step, f"{path}.type is required")

        step_type = step["type"]
        _expect_type(step_type, str, f"{path}.type")
        if step_type not in STEP_TYPES:
            raise SchemaError(f"{path}.type '{step_type}' is not recognised")

        normalised = dict(step)  # shallow copy so we do not mutate input

        if step_type == "consent.request":
            scopes = normalised.get("scopes", [])
            message = normalised.get("message", "Permission requested")
            _expect_type(scopes, list, f"{path}.scopes")
            for scope in scopes:
                _expect_type(scope, str, f"{path}.scopes[]")
            _expect_type(message, str, f"{path}.message")
            normalised.setdefault("timeout_ms", 30000)

        elif step_type == "voice.speak":
            message = normalised.get("message", "")
            _expect(message, f"{path}.message is required for voice.speak")
            _expect_type(message, str, f"{path}.message")
            if "wait_for_response" in normalised:
                _expect_type(normalised["wait_for_response"], bool, f"{path}.wait_for_response")
            if "voice" in normalised:
                _expect_type(normalised["voice"], str, f"{path}.voice")

        elif step_type == "memory.store":
            data = normalised.get("data")
            _expect(data is not None, f"{path}.data is required for memory.store")
            _expect_type(data, str, f"{path}.data")
            normalised.setdefault("type_", "narrative")
            if "tags" in normalised:
                _expect_type(normalised["tags"], list, f"{path}.tags")

        elif step_type == "memory.recall":
            query = normalised.get("query", "")
            _expect_type(query, str, f"{path}.query")
            if "max_results" in normalised:
                _expect_type(normalised["max_results"], int, f"{path}.max_results")

        elif step_type == "crisis.detect":
            text = normalised.get("text", "")
            _expect_type(text, str, f"{path}.text")

        validated_steps.append(normalised)

    return {
        "intent": intent,
        "voice": voice,
        "phase": phase,
        "steps": validated_steps,
    }


# ---------------------------------------------------------------------------
# Core runtime (demo friendly)
# ---------------------------------------------------------------------------

@dataclass
class AttestationEntry:
    timestamp: float
    event: str
    data: Dict[str, Any]


class Attestation:
    def __init__(self) -> None:
        self.logs: List[AttestationEntry] = []

    def log(self, event: str, data: Dict[str, Any]) -> str:
        entry = AttestationEntry(time.time(), event, data)
        self.logs.append(entry)
        serialised = json.dumps({"timestamp": entry.timestamp, "event": event, "data": data}, sort_keys=True)
        return hashlib.sha256(serialised.encode()).hexdigest()


class Runtime:
    def __init__(self) -> None:
        self.consent_granted = False
        self.memory = {"narrative": {}, "artifact": {}}
        self.crisis_active = False
        self.attestation = Attestation()
        self.active_voice: Optional[str] = None

    # ---------------------- parsing & validation ----------------------
    def parse_ritual(self, ritual: str) -> Dict[str, Any]:
        try:
            ritual_data = json.loads(ritual)
        except json.JSONDecodeError as exc:
            raise SchemaError(f"Ritual must be valid JSON: {exc}") from exc
        return validate_ritual_schema(ritual_data)

    def validate(self, ritual_data: Dict[str, Any]) -> bool:
        # Validation already handled in parse_ritual but we keep this hook for parity
        self.attestation.log("validation", {"status": "passed", "intent": ritual_data["intent"]})
        return True

    # ---------------------- execution helpers ------------------------
    def _detect_crisis(self, text: str) -> bool:
        crisis_keywords = {"giving up", "ending it", "suicide", "hopeless"}
        lowered = text.lower()
        detected = any(keyword in lowered for keyword in crisis_keywords)
        if detected:
            self.crisis_active = True
            self.attestation.log("crisis_detected", {"trigger": text})
        return detected

    def _store_memory(self, step: Dict[str, Any]) -> None:
        bucket = "narrative" if step.get("type_", "narrative") == "narrative" else "artifact"
        entry_id = f"{bucket}_{len(self.memory[bucket]) + 1}"
        self.memory[bucket][entry_id] = {
            "data": step.get("data"),
            "tags": step.get("tags", []),
        }
        self.attestation.log("memory_store", {"bucket": bucket, "entry_id": entry_id})

    def execute_step(self, step: Dict[str, Any], ritual_metadata: Dict[str, Any]) -> None:
        step_type = step["type"]

        if step_type == "consent.request":
            message = sanitize_for_windows_terminal(step.get("message", "Permission requested."))
            scopes = step.get("scopes", [])
            print(message)
            if not self.consent_granted:
                print(sanitize_for_windows_terminal("[GROK] Auto-granting consent for demo purposes."))
                self.consent_granted = True
            self.attestation.log("consent_request", {"granted": self.consent_granted, "scopes": scopes})

        elif step_type == "voice.speak":
            voice = step.get("voice", ritual_metadata["voice"])
            message = sanitize_for_windows_terminal(step["message"])
            if voice != self.active_voice:
                self.active_voice = voice
                self.attestation.log("voice_activate", {"voice": voice})
            print(f"[{voice}] {message}")
            self.attestation.log("voice_speak", {"voice": voice})
            if self._detect_crisis(step["message"]):
                print(sanitize_for_windows_terminal("[CRISIS] Trigger detected - pausing ritual."))

        elif step_type == "memory.store":
            if not self.consent_granted:
                print(sanitize_for_windows_terminal("Consent is required before storing memory."))
                self.attestation.log("memory_store_blocked", {"reason": "consent_not_granted"})
                return
            self._store_memory(step)

        elif step_type == "memory.recall":
            query = sanitize_for_windows_terminal(step.get("query", ""))
            print(f"[memory.recall] Query: {query}")
            self.attestation.log("memory_recall", {"query": query, "max_results": step.get("max_results", 5)})

        elif step_type == "crisis.detect":
            text = step.get("text", "")
            if self._detect_crisis(text):
                print(sanitize_for_windows_terminal("[CRISIS] Trigger detected via crisis.detect step."))
            else:
                print(sanitize_for_windows_terminal("[CRISIS] No trigger detected."))

    # ---------------------- main entry point -------------------------
    def run(self, ritual: str) -> None:
        try:
            ritual_data = self.parse_ritual(ritual)
        except SchemaError as exc:
            print(sanitize_for_windows_terminal(f"Ritual validation failed: {exc}"))
            self.attestation.log("validation", {"status": "failed", "error": str(exc)})
            return

        if not self.validate(ritual_data):
            print(sanitize_for_windows_terminal("Ritual validation failed."))
            return

        for step in ritual_data.get("steps", []):
            try:
                self.execute_step(step, ritual_data)
            except Exception as exc:  # pragma: no cover - demo safeguard
                print(sanitize_for_windows_terminal(f"Step execution failed: {exc}"))
                self.attestation.log("step_error", {"type": step.get("type"), "error": str(exc)})
                break

        if self.crisis_active:
            print(sanitize_for_windows_terminal("Crisis response: taking a pause."))
            self.attestation.log("crisis_response", {"action": "pause"})

        attestation_payload = [
            {
                "timestamp": entry.timestamp,
                "event": entry.event,
                "data": entry.data,
            }
            for entry in self.attestation.logs
        ]
        print("Attestation logs:", json.dumps(attestation_payload, indent=2))


# ---------------------------------------------------------------------------
# Demo usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(sanitize_for_windows_terminal('dY"r Testing GROK\'s SpiralLogic Implementation'))
    runtime = Runtime()
    sample_ritual = """
{
    "intent": "journaling_support",
    "voice": "@healer",
    "phase": "contemplative",
    "steps": [
        {
            "type": "consent.request",
            "scopes": ["memory"],
            "message": "I'd like to remember your journaling patterns to provide better support over time. Is that okay?"
        },
        {
            "type": "voice.speak",
            "message": "Let's create a safe space for your thoughts. What's been on your mind today?"
        },
        {
            "type": "memory.store",
            "data": "User initiated journaling session - seeking emotional processing space",
            "type_": "narrative"
        }
    ]
}
    """
    runtime.run(sample_ritual)
