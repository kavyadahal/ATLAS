"""
Test script for application launcher bug fixes.
Tests the fixed app opening and website routing functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from automation.desktop_controller import DesktopController
from brain.intent_detector import IntentDetector
from brain.executor import CommandExecutor

def test_intent_detection():
    """Test that intents are correctly detected."""
    print("=" * 60)
    print("TESTING INTENT DETECTION")
    print("=" * 60)
    
    detector = IntentDetector()
    
    test_cases = [
        ("open google", "open_app", "google"),
        ("open chrome", "open_app", "chrome"),
        ("open vscode", "open_app", "vscode"),
        ("open notepad", "open_app", "notepad"),
        ("open google.com", "open_website", "google.com"),
        ("open youtube.com", "open_website", "youtube.com"),
        ("open https://github.com", "open_website", "https://github.com"),
        ("go to reddit.com", "open_website", "reddit.com"),
        ("open youtube", "open_app", "youtube"),  # Should route to app (then redirect to website)
    ]
    
    passed = 0
    failed = 0
    
    for text, expected_intent, expected_param in test_cases:
        intent, params = detector.detect_intent(text)
        
        if intent == expected_intent:
            print(f"✓ '{text}' -> {intent}")
            if params:
                param_value = params.get('app_name') or params.get('url', '')
                if expected_param.lower() in param_value.lower():
                    print(f"  ✓ Parameter: {param_value}")
                    passed += 1
                else:
                    print(f"  ✗ Parameter mismatch: expected '{expected_param}', got '{param_value}'")
                    failed += 1
            else:
                passed += 1
        else:
            print(f"✗ '{text}' -> Expected: {expected_intent}, Got: {intent}")
            failed += 1
    
    print(f"\nIntent Detection: {passed} passed, {failed} failed")
    return failed == 0


def test_app_aliases():
    """Test that app aliases are properly mapped."""
    print("\n" + "=" * 60)
    print("TESTING APP ALIASES")
    print("=" * 60)
    
    controller = DesktopController()
    
    # Check if aliases exist
    test_aliases = [
        'google',
        'google chrome',
        'chrome',
        'vscode',
        'vs code',
        'visual studio code',
        'code',
        'notepad',
        'calculator',
        'calc',
    ]
    
    passed = 0
    failed = 0
    
    for alias in test_aliases:
        if alias in controller.COMMON_APPS:
            print(f"✓ '{alias}' -> {controller.COMMON_APPS[alias]}")
            passed += 1
        else:
            print(f"✗ '{alias}' not found in COMMON_APPS")
            failed += 1
    
    print(f"\nApp Aliases: {passed} passed, {failed} failed")
    return failed == 0


def test_website_apps():
    """Test that website apps are properly configured."""
    print("\n" + "=" * 60)
    print("TESTING WEBSITE APPS")
    print("=" * 60)
    
    controller = DesktopController()
    
    # Check if website apps exist
    test_website_apps = [
        'youtube',
        'gmail',
        'github',
        'reddit',
        'twitter',
        'facebook',
        'instagram',
    ]
    
    passed = 0
    failed = 0
    
    for app in test_website_apps:
        if app in controller.WEBSITE_APPS:
            print(f"✓ '{app}' -> {controller.WEBSITE_APPS[app]}")
            passed += 1
        else:
            print(f"✗ '{app}' not found in WEBSITE_APPS")
            failed += 1
    
    print(f"\nWebsite Apps: {passed} passed, {failed} failed")
    return failed == 0


def test_path_resolution():
    """Test that common executables can be found."""
    print("\n" + "=" * 60)
    print("TESTING PATH RESOLUTION")
    print("=" * 60)
    
    import shutil
    
    # Test if shutil.which works for common apps
    test_exes = [
        'notepad.exe',
        'calc.exe',
        'explorer.exe',
    ]
    
    passed = 0
    failed = 0
    
    for exe in test_exes:
        path = shutil.which(exe)
        if path:
            print(f"✓ Found '{exe}' at: {path}")
            passed += 1
        else:
            print(f"✗ Could not find '{exe}' in PATH")
            failed += 1
    
    # Test Chrome path resolution (may not be in PATH)
    print(f"\nChecking Chrome installation paths:")
    chrome_paths = [
        os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'Google\\Chrome\\Application\\chrome.exe'),
        os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), 'Google\\Chrome\\Application\\chrome.exe'),
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✓ Found Chrome at: {path}")
            chrome_found = True
            passed += 1
            break
    
    if not chrome_found:
        print(f"⚠ Chrome not found in standard locations (this is OK if Chrome isn't installed)")
    
    print(f"\nPath Resolution: {passed} passed, {failed} failed")
    return failed == 0


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("ATLAS APPLICATION LAUNCHER BUG FIX - TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Intent Detection", test_intent_detection()))
    results.append(("App Aliases", test_app_aliases()))
    results.append(("Website Apps", test_website_apps()))
    results.append(("Path Resolution", test_path_resolution()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ ALL TESTS PASSED - Bug fixes are working correctly!")
        print("\nThe application launcher should now work properly.")
        print("Try saying: 'open google', 'open chrome', 'open youtube.com'")
    else:
        print("\n✗ SOME TESTS FAILED - Please review the output above")
    
    print("\nNote: This test does NOT actually open applications.")
    print("It only verifies that the detection and routing logic is correct.")
    print("\nTo test actual app opening, run ATLAS and try the commands.")


if __name__ == "__main__":
    main()
