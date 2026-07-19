"""
Comprehensive test for voice command variations with fuzzy matching.
This test validates that ATLAS can handle common speech-to-text errors.
"""

from automation.desktop_controller import DesktopController
from brain.intent_detector import IntentDetector

def run_comprehensive_tests():
    """Run comprehensive tests for voice variations."""
    
    desktop = DesktopController()
    detector = IntentDetector()
    
    print("=" * 80)
    print("ATLAS VOICE COMMAND FUZZY MATCHING - COMPREHENSIVE TEST")
    print("=" * 80)
    
    # All test cases from requirements
    test_cases = [
        # Original working commands (should still work)
        ("open vscode", "vscode", "BASELINE"),
        ("open google", "google", "BASELINE"),
        ("open chrome", "chrome", "BASELINE"),
        ("open notepad", "notepad", "BASELINE"),
        
        # VSCode variations (speech errors)
        ("open vscod", "vscode", "FUZZY"),
        ("open vsco", "vscode", "FUZZY"),
        ("open vis code", "visual studio code", "FUZZY"),  # Matches to full name (also valid)
        
        # Google variations (speech errors)
        ("open goggle", "google", "FUZZY"),
        ("open googel", "google", "FUZZY"),
        ("open Google", "google", "FUZZY"),  # Capitalization
        
        # Chrome variations (speech errors)
        ("open chrom", "chrome", "FUZZY"),
        ("open crome", "chrome", "FUZZY"),
        
        # Launch/start commands
        ("launch vscod", "vscode", "FUZZY"),
        ("start goggle", "google", "FUZZY"),
    ]
    
    print("\n📋 TEST RESULTS")
    print("-" * 80)
    
    total = 0
    passed = 0
    failed = 0
    
    for command, expected_app, test_type in test_cases:
        total += 1
        
        # Step 1: Intent detection
        intent, params = detector.detect_intent(command)
        
        if intent not in ['open_app', 'open_website']:
            print(f"❌ FAIL | '{command}' -> Intent: {intent} (expected open_app)")
            failed += 1
            continue
        
        # Step 2: Get app name
        app_name = params.get('app_name', '')
        
        # Step 3: Fuzzy match
        matched = desktop._fuzzy_match_app_name(app_name)
        
        # Check if matched correctly
        success = matched == expected_app or (matched and expected_app in matched)
        
        if success:
            marker = "✓" if test_type == "BASELINE" else "🔍"
            print(f"{marker} PASS | '{command:25s}' -> '{app_name:15s}' -> '{matched:15s}' [{test_type}]")
            passed += 1
        else:
            print(f"❌ FAIL | '{command:25s}' -> '{app_name:15s}' -> '{matched or 'None':15s}' (expected: {expected_app})")
            failed += 1
    
    # Summary
    print("-" * 80)
    print(f"\n📊 SUMMARY")
    print(f"   Total Tests:  {total}")
    print(f"   ✓ Passed:     {passed} ({passed*100//total}%)")
    print(f"   ❌ Failed:     {failed}")
    
    if failed == 0:
        print(f"\n🎉 ALL TESTS PASSED! Voice command fuzzy matching is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Review the results above.")
    
    # Detailed explanation
    print("\n" + "=" * 80)
    print("WHAT THIS MEANS")
    print("=" * 80)
    print("""
✓ BASELINE tests: Normal commands work as before
🔍 FUZZY tests: Speech errors are automatically corrected

Examples of corrections:
  • "open vscod"  → automatically opens VSCode
  • "open goggle" → automatically opens Google (Chrome)
  • "open chrom"  → automatically opens Chrome

The fuzzy matching threshold is set to 75%, which means:
  - Minor typos and speech errors are corrected
  - Completely different words are NOT matched (safety)
  - Exact matches always work perfectly
""")
    
    print("=" * 80)
    
    return failed == 0

if __name__ == "__main__":
    success = run_comprehensive_tests()
    exit(0 if success else 1)
