"""
Test fuzzy matching for voice command variations.
Tests that voice recognition errors are corrected by fuzzy matching.
"""

from automation.desktop_controller import DesktopController
from brain.intent_detector import IntentDetector

def test_fuzzy_matching():
    """Test fuzzy matching for app name variations."""
    
    desktop = DesktopController()
    detector = IntentDetector()
    
    print("=" * 70)
    print("FUZZY MATCHING TEST FOR VOICE VARIATIONS")
    print("=" * 70)
    
    # Test cases with expected matches
    test_cases = [
        # VSCode variations
        ("vscod", "vscode"),
        ("vsco", "vscode"),
        ("vis code", "vs code"),
        ("visual studio", "visual studio code"),
        
        # Google/Chrome variations
        ("goggle", "google"),
        ("googel", "google"),
        ("googl", "google"),
        ("chrom", "chrome"),
        ("crome", "chrome"),
        
        # Exact matches (should still work)
        ("vscode", "vscode"),
        ("chrome", "chrome"),
        ("google", "google"),
        ("notepad", "notepad"),
        ("youtube", "youtube"),
    ]
    
    print("\n1. Testing Fuzzy Matching Algorithm")
    print("-" * 70)
    
    passed = 0
    failed = 0
    
    for input_name, expected_match in test_cases:
        matched = desktop._fuzzy_match_app_name(input_name)
        
        # For multi-word inputs like "vis code", check if it matches any variant
        if matched == expected_match or (matched and expected_match in matched) or (matched and matched in expected_match):
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"{status} | Input: '{input_name:20s}' -> Matched: '{matched or 'None':20s}' (Expected: {expected_match})")
    
    print(f"\nFuzzy Matching Results: {passed} passed, {failed} failed")
    
    # Test with intent detector
    print("\n2. Testing End-to-End Intent Detection")
    print("-" * 70)
    
    intent_tests = [
        "open vscod",
        "open vsco", 
        "open goggle",
        "open googel",
        "open chrom",
        "open vscode",
        "open chrome",
        "open google",
    ]
    
    for command in intent_tests:
        intent, params = detector.detect_intent(command)
        print(f"\nCommand: '{command}'")
        print(f"  Intent: {intent}")
        if params and 'app_name' in params:
            app_name = params['app_name']
            matched = desktop._fuzzy_match_app_name(app_name)
            print(f"  App name extracted: '{app_name}'")
            print(f"  Fuzzy matched to: '{matched or 'No match'}'")
        print("-" * 70)
    
    print("\n3. Testing Real-World Scenarios")
    print("-" * 70)
    
    scenarios = [
        ("User says 'open vscod'", "vscod"),
        ("User says 'open goggle'", "goggle"),
        ("User says 'open chrom'", "chrom"),
        ("User says 'launch vsco'", "vsco"),
    ]
    
    for description, app_name in scenarios:
        print(f"\n{description}")
        matched = desktop._fuzzy_match_app_name(app_name)
        if matched:
            print(f"  ✓ Fuzzy matched '{app_name}' to '{matched}'")
            print(f"  → Would execute: open_application('{matched}')")
        else:
            print(f"  ✗ No match found for '{app_name}'")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_fuzzy_matching()
