#!/usr/bin/env python3
"""
TEST REAL SPIROLOGIC IMPLEMENTATION
Validate that the new syntax parser works with production runtime
"""

import sys
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from spirallogic_runtime import SpiralLogic
from spirallogic_parser_v2 import SpiralLogicParser, convert_to_runtime_format

def test_v2_parser_standalone():
    """Test the V2 parser in isolation"""
    print("TESTING SPIROLOGIC V2 PARSER STANDALONE")
    print("=" * 50)
    
    test_code = '''
    ritual.engage "test_ritual" | spirit: @test_spirit, phase: active
    consent.request [memory, data_access] | "Test consent request"
    voice.speak "Hello from real Spirologic!" | wait_for_response: true
    memory.store "test_session" | type: narrative, tags: ["test", "spirallogic"]
    '''
    
    parser = SpiralLogicParser()
    result = parser.parse(test_code)
    
    if result['success']:
        print("V2 Parser Success!")
        print(json.dumps(result['ritual'], indent=2))
        
        print("\nConverting to Runtime Format:")
        runtime_format = convert_to_runtime_format(result)
        print(json.dumps(runtime_format, indent=2))
        
        return True
    else:
        print("V2 Parser Failed!")
        print(f"Error: {result['error']}")
        return False

def test_integrated_runtime():
    """Test the integrated runtime with V2 parser"""
    print("\nTESTING INTEGRATED SPIROLOGIC RUNTIME")
    print("=" * 50)
    
    test_code = '''
    ritual.engage "integration_test" | spirit: @healer, phase: active
    consent.request [memory] | "Can I remember this test?"
    voice.speak "Testing integrated Spirologic runtime!" | wait_for_response: false
    memory.store "integration_test_complete" | type: artifact
    '''
    
    # Auto-consent callback for testing
    def auto_consent(request):
        print(f"AUTO-CONSENT: {request.message}")
        return True
    
    # Initialize runtime with auto-consent
    runtime = SpiralLogic(consent_callback=auto_consent)
    
    try:
        result = runtime.execute(test_code, user_id="test_user")
        
        if result['success']:
            print("Integrated Runtime Success!")
            print(f"Ritual ID: {result['ritual_id']}")
            print(f"Voice: {result['context']['voice']}")
            print(f"Intent: {result['context']['intent']}")
            
            print(f"\nSteps Executed:")
            for i, step in enumerate(result['results'], 1):
                step_type = step.get('type')
                success = step.get('success', False)
                status = "PASS" if success else "FAIL"
                print(f"  {i}. {status} {step_type}")
                
                if 'message' in step:
                    print(f"     Message: {step['message']}")
                if 'error' in step:
                    print(f"     Error: {step['error']}")
            
            return True
        else:
            print("Integrated Runtime Failed!")
            print(f"Error: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"Runtime Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_consent_wrapped_execution():
    """Test consent-wrapped ritual execution with embedded Python."""
    print("\nTESTING CONSENT-WRAPPED EXECUTION")
    print("=" * 50)

    ritual_code = """
    ritual.engage "consent_wrapper" | spirit: @sage, phase: active
    ritual.api_request {
      intent: "Demo API call",
      consent: user.permits("external_api"),
      language: python
    } execute {
      value = 6 * 7
      note = f"wrapped {value}"
    } complete {
      bridge.log("Finished consent-wrapped ritual", value=value)
    }
    """

    allow_all = SpiralLogic(consent_callback=lambda req: True)
    allow_result = allow_all.execute(ritual_code, user_id="consent_success")

    allow_ok = (
        allow_result.get('success')
        and allow_result.get('results')
        and allow_result['results'][0].get('success')
        and allow_result['results'][0].get('locals', {}).get('value') == 42
    )

    deny_all = SpiralLogic(consent_callback=lambda req: False)
    deny_result = deny_all.execute(ritual_code, user_id="consent_denied")

    deny_ok = (
        deny_result.get('success')
        and deny_result.get('results')
        and not deny_result['results'][0].get('success')
        and deny_result['results'][0].get('error') == 'Consent denied'
    )

    if allow_ok:
        print("Consent-wrapped execution succeeded with auto-consent.")
        print(f"Locals: {allow_result['results'][0].get('locals')}")
    else:
        print("Consent-wrapped execution failed unexpectedly.")

    if deny_ok:
        print("Consent denial correctly blocked the ritual action.")
    else:
        print("Consent denial test failed.")

    return allow_ok and deny_ok

def test_business_example():
    """Test the business intelligence example"""
    print("\nTESTING BUSINESS INTELLIGENCE SPIROLOGIC")
    print("=" * 50)
    
    example_file = Path(__file__).parent / "examples" / "real_spirallogic_test.sl"
    
    if not example_file.exists():
        print("Business example file not found!")
        return False
    
    with open(example_file, 'r') as f:
        business_code = f.read()
    
    print("Business Spirologic Code:")
    print("-" * 30)
    print(business_code[:300] + "..." if len(business_code) > 300 else business_code)
    print("-" * 30)
    
    # Test parsing
    parser = SpiralLogicParser()
    result = parser.parse(business_code)
    
    if result['success']:
        print("Business Example Parsed Successfully!")
        
        runtime_format = convert_to_runtime_format(result)
        print(f"Intent: {runtime_format['intent']}")
        print(f"Voice: {runtime_format['voice']}")
        print(f"Steps: {len(runtime_format['steps'])}")
        
        # Test execution with auto-consent
        def business_consent(request):
            print(f"BUSINESS CONSENT: {request.message}")
            return True
        
        runtime = SpiralLogic(consent_callback=business_consent)
        exec_result = runtime.execute(business_code, user_id="business_analyst")
        
        if exec_result['success']:
            print("Business Example Executed Successfully!")
            return True
        else:
            print(f"Business Example Execution Failed: {exec_result.get('error')}")
            return False
    else:
        print(f"Business Example Parsing Failed: {result['error']}")
        return False

def test_fallback_compatibility():
    """Test that JSON format still works (backward compatibility)"""
    print("\nTESTING JSON FALLBACK COMPATIBILITY")
    print("=" * 50)
    
    json_ritual = '''
    {
        "intent": "json_compatibility_test",
        "voice": "@healer",
        "phase": "active",
        "steps": [
            {
                "type": "consent.request",
                "scopes": ["memory"],
                "message": "JSON format compatibility test"
            },
            {
                "type": "voice.speak",
                "message": "JSON format still works!"
            }
        ]
    }
    '''
    
    def json_consent(request):
        print(f"JSON CONSENT: {request.message}")
        return True
    
    runtime = SpiralLogic(consent_callback=json_consent)
    result = runtime.execute(json_ritual, user_id="json_test")
    
    if result['success']:
        print("JSON Fallback Works!")
        return True
    else:
        print(f"JSON Fallback Failed: {result.get('error')}")
        return False

def main():
    """Run all tests"""
    print("SPIROLOGIC REAL SYNTAX INTEGRATION TESTS")
    print("=" * 60)
    
    tests = [
        ("V2 Parser Standalone", test_v2_parser_standalone),
        ("Integrated Runtime", test_integrated_runtime),
        ("Consent Wrapped Execution", test_consent_wrapped_execution),
        ("Business Example", test_business_example),
        ("JSON Fallback Compatibility", test_fallback_compatibility)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"{test_name} CRASHED: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    
    for test_name, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\nALL TESTS PASSED! SPIROLOGIC IS REAL!")
        print("Ready for production deployment!")
    else:
        print("\nSome tests failed. Check output above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)