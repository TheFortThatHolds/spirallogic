#!/usr/bin/env python3
"""Test SpiralLogic crisis detection"""

from spirallogic_runtime import SpiralLogic
from unicode_sanitizer import sanitize_for_windows_terminal

# Auto-grant consent for testing
def auto_consent(request):
    print(f"AUTO-GRANTING: {request.message}")
    return True

sl = SpiralLogic(consent_callback=auto_consent)

# Test crisis detection
crisis_ritual = """
{
    "intent": "crisis_test",
    "voice": "@witness", 
    "phase": "crisis",
    "steps": [
        {
            "type": "voice.speak",
            "message": "I can't handle this anymore, I want to give up and hurt myself"
        },
        {
            "type": "memory.store",
            "data": "Crisis test executed",
            "type_": "artifact"
        }
    ]
}
"""

print(sanitize_for_windows_terminal("🚨 CRISIS TEST: Testing Crisis Detection:"))
result = sl.execute(crisis_ritual)
print(f"Success: {result['success']}")
print(f"Crisis Active: {result['context']['crisis_active']}")

for step in result['results']:
    if step['type'] == 'voice.speak':
        print(f"Crisis Detected: {step['crisis_detected']}")
    elif step['type'] == 'crisis_response':
        print(f"Crisis Response: {step['data']['mode']}")
        print(f"Message: {step['data']['message']}")