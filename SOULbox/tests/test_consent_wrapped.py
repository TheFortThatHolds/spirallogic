#!/usr/bin/env python3
"""Tests for consent-wrapped execution in SOULbox SpiralLogic runtime."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.spirallogic_runtime import SpiralLogic  # noqa: E402


def make_ritual():
    """Utility to build a consent-wrapped ritual JSON string."""
    ritual = {
        "intent": "sandbox_demo",
        "voice": "@healer",
        "phase": "active",
        "steps": [
            {
                "type": "ritual.api_request",
                "metadata": {
                    "intent": "Demo API call",
                    "language": "python"
                },
                "consent_scopes": ["external_api"],
                "execute": "result = 5 * 9\nmessage = f'calc {result}'"
            }
        ]
    }
    return json.dumps(ritual)


def test_consent_wrapped_allows_execution():
    ritual_code = make_ritual()

    runtime = SpiralLogic(consent_callback=lambda req: True)
    result = runtime.execute(ritual_code, user_id="tester")

    assert result["success"] is True
    step = result["results"][0]
    assert step["success"] is True
    assert step["locals"]["result"] == 45
    assert step["locals"]["message"] == "calc 45"


def test_consent_wrapped_denies_without_consent():
    ritual_code = make_ritual()

    runtime = SpiralLogic(consent_callback=lambda req: False)
    result = runtime.execute(ritual_code, user_id="tester")

    assert result["success"] is True
    step = result["results"][0]
    assert step["success"] is False
    assert step["error"] == "Consent denied"
    assert step["requested_scopes"] == ["external_api"]
