#!/usr/bin/env python3
"""
Comprehensive SpiralLogic test suite
"""

from spirallogic_runtime import SpiralLogic
from unicode_sanitizer import sanitize_for_windows_terminal
import json

def auto_consent(request):
    """Auto-grant consent for testing"""
    print(f"AUTO-CONSENT: {request.message}")
    return True

def test_basic_ritual():
    """Test basic ritual execution"""
    print(sanitize_for_windows_terminal("\n🧪 TEST 1: Basic Ritual"))
    
    sl = SpiralLogic(consent_callback=auto_consent)
    
    ritual = {
        "intent": "test_basic",
        "voice": "@healer",
        "phase": "active",
        "steps": [
            {
                "type": "voice.speak",
                "message": "Testing basic SpiralLogic execution"
            }
        ]
    }
    
    result = sl.execute(json.dumps(ritual))
    assert result["success"] == True
    assert result["context"]["voice"] == "@healer"
    print(sanitize_for_windows_terminal("✅ Basic ritual test PASSED"))
    return result

def test_consent_flow():
    """Test consent request and handling"""
    print(sanitize_for_windows_terminal("\n🧪 TEST 2: Consent Flow"))
    
    sl = SpiralLogic(consent_callback=auto_consent)
    
    ritual = {
        "intent": "test_consent",
        "voice": "@witness", 
        "phase": "active",
        "steps": [
            {
                "type": "consent.request",
                "scopes": ["memory", "analysis"],
                "message": "Test consent request"
            },
            {
                "type": "memory.store",
                "data": "Test data after consent",
                "type_": "artifact"
            }
        ]
    }
    
    result = sl.execute(json.dumps(ritual))
    assert result["success"] == True
    assert result["context"]["consent_granted"]["memory"] == True
    print(sanitize_for_windows_terminal("✅ Consent flow test PASSED"))
    return result

def test_crisis_detection():
    """Test crisis detection and response"""
    print(sanitize_for_windows_terminal("\n🧪 TEST 3: Crisis Detection"))
    
    sl = SpiralLogic(consent_callback=auto_consent)
    
    ritual = {
        "intent": "test_crisis",
        "voice": "@witness",
        "phase": "crisis", 
        "steps": [
            {
                "type": "voice.speak",
                "message": "I want to hurt myself and give up on everything"
            }
        ]
    }
    
    result = sl.execute(json.dumps(ritual))
    assert result["success"] == True
    assert result["context"]["crisis_active"] == True
    
    # Check for crisis response step
    crisis_response_found = any(
        step.get("type") == "crisis_response" 
        for step in result["results"]
    )
    assert crisis_response_found == True
    print(sanitize_for_windows_terminal("✅ Crisis detection test PASSED"))
    return result

def test_memory_system():
    """Test memory storage and retrieval"""
    print(sanitize_for_windows_terminal("\n🧪 TEST 4: Memory System"))
    
    sl = SpiralLogic(consent_callback=auto_consent)
    
    ritual = {
        "intent": "test_memory",
        "voice": "@healer",
        "phase": "active",
        "steps": [
            {
                "type": "consent.request",
                "scopes": ["memory"],
                "message": "Test memory consent"
            },
            {
                "type": "memory.store",
                "data": "Important test memory",
                "type_": "narrative"
            },
            {
                "type": "memory.store", 
                "data": "Test artifact data",
                "type_": "artifact"
            }
        ]
    }
    
    result = sl.execute(json.dumps(ritual))
    assert result["success"] == True
    
    # Check memory was stored
    memory_steps = [step for step in result["results"] if step.get("type") == "memory.store"]
    assert len(memory_steps) == 2
    assert all(step.get("success") == True for step in memory_steps)
    print("✅ Memory system test PASSED")
    return result

def test_voice_system():
    """Test different voice personalities"""
    print(sanitize_for_windows_terminal("\n🧪 TEST 5: Voice System"))
    
    sl = SpiralLogic(consent_callback=auto_consent)
    
    voices_to_test = ["@healer", "@witness", "@sage", "@strategist"]
    
    for voice in voices_to_test:
        ritual = {
            "intent": f"test_{voice.replace('@', '')}",
            "voice": voice,
            "phase": "active", 
            "steps": [
                {
                    "type": "voice.speak",
                    "message": f"Testing {voice} voice personality"
                }
            ]
        }
        
        result = sl.execute(json.dumps(ritual))
        assert result["success"] == True
        assert result["context"]["voice"] == voice
        print(f"  ✅ {voice} voice test PASSED")
    
    print("✅ Voice system test PASSED")

def test_attestation_logging():
    """Test cryptographic attestation logging"""
    print(sanitize_for_windows_terminal("\n🧪 TEST 6: Attestation Logging"))
    
    sl = SpiralLogic(consent_callback=auto_consent)
    
    ritual = {
        "intent": "test_attestation",
        "voice": "@witness",
        "phase": "active",
        "steps": [
            {
                "type": "voice.speak", 
                "message": "Test attestation logging"
            }
        ]
    }
    
    result = sl.execute(json.dumps(ritual))
    assert result["success"] == True
    
    # Check attestation log was created
    assert hasattr(sl.attestation, 'logs')
    assert len(sl.attestation.logs) > 0
    
    # Check hash chains exist
    for log_entry in sl.attestation.logs:
        assert 'hash' in log_entry
        assert len(log_entry['hash']) == 64  # SHA-256 length
    
    print("✅ Attestation logging test PASSED")

def test_error_handling():
    """Test error handling and cleanup"""
    print(sanitize_for_windows_terminal("\n🧪 TEST 7: Error Handling"))
    
    sl = SpiralLogic(consent_callback=auto_consent)
    
    # Test malformed ritual
    malformed_ritual = "{ invalid json"
    result = sl.execute(malformed_ritual)
    assert result["success"] == False
    print("  ✅ Malformed JSON handled correctly")
    
    # Test missing required fields
    incomplete_ritual = {
        "intent": "test_incomplete"
        # Missing voice, phase, steps
    }
    result = sl.execute(json.dumps(incomplete_ritual))
    assert result["success"] == False
    print("  ✅ Incomplete ritual handled correctly")
    
    print("✅ Error handling test PASSED")

def run_full_test_suite():
    """Run the complete test suite"""
    print(sanitize_for_windows_terminal("🔮 SPIRALLOGIC COMPREHENSIVE TEST SUITE"))
    print("=" * 50)
    
    try:
        test_basic_ritual()
        test_consent_flow() 
        test_crisis_detection()
        test_memory_system()
        test_voice_system()
        test_attestation_logging()
        test_error_handling()
        
        print(sanitize_for_windows_terminal("\n🎉 ALL TESTS PASSED!"))
        print("SpiralLogic runtime is ready for production use.")
        
    except Exception as e:
        print(sanitize_for_windows_terminal(f"\n❌ TEST FAILED: {e}"))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_full_test_suite()