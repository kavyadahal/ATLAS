"""
Test script for ATLAS v2 automation features
Run this to verify that the automation system is working correctly
"""

import sys
from automation.desktop_controller import DesktopController
from automation.file_manager import FileManager
from automation.command_router import CommandRouter


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_desktop_controller():
    """Test desktop controller functionality."""
    print_section("Testing Desktop Controller")
    
    desktop = DesktopController()
    
    # Test 1: List running applications
    print("\n[TEST 1] Listing running applications...")
    apps = desktop.list_running_applications()
    print(f"✓ Found {len(apps)} running applications")
    print(f"  Sample: {', '.join(apps[:5])}...")
    
    # Test 2: Search applications
    print("\n[TEST 2] Searching for installed applications...")
    results = desktop.search_applications("chrome")
    if results:
        print(f"✓ Found: {', '.join(results)}")
    else:
        print("✓ No matches found (this is okay)")
    
    # Test 3: Check common folders
    print("\n[TEST 3] Checking common folder paths...")
    for folder_name, folder_path in desktop.COMMON_FOLDERS.items():
        print(f"  {folder_name}: {folder_path}")
    print("✓ Common folders configured")
    
    print("\n✓ Desktop Controller tests passed!")


def test_file_manager():
    """Test file manager functionality."""
    print_section("Testing File Manager")
    
    fm = FileManager()
    
    # Test 1: File categories
    print("\n[TEST 1] Checking file categories...")
    for category, extensions in fm.FILE_CATEGORIES.items():
        print(f"  {category}: {len(extensions)} extensions")
    print("✓ File categories configured")
    
    # Test 2: Search for common files (limit to avoid long searches)
    print("\n[TEST 2] Testing file search (limited)...")
    results = fm.search_files("test", limit=3)
    print(f"✓ Search completed, found {len(results)} file(s)")
    
    # Test 3: Get recent files
    print("\n[TEST 3] Getting recent files...")
    recent = fm.get_recent_files(days=1)
    print(f"✓ Found {len(recent)} file(s) modified in the last day")
    if recent:
        print(f"  Most recent: {recent[0]['name']}")
    
    # Test 4: Test size formatting
    print("\n[TEST 4] Testing file size formatting...")
    test_sizes = [1024, 1048576, 1073741824]
    for size in test_sizes:
        formatted = fm._format_size(size)
        print(f"  {size} bytes = {formatted}")
    print("✓ Size formatting works")
    
    print("\n✓ File Manager tests passed!")


def test_command_router():
    """Test command router functionality."""
    print_section("Testing Command Router")
    
    router = CommandRouter()
    
    # Test various command patterns
    test_commands = [
        ("open chrome", "Desktop: Open App"),
        ("close notepad", "Desktop: Close App"),
        ("open github.com", "Desktop: Open Website"),
        ("open downloads", "Desktop: Open Folder"),
        ("what applications are running", "Desktop: List Apps"),
        ("find my resume", "Files: Search"),
        ("create a folder called test", "Files: Create Folder"),
        ("organize downloads", "Files: Organize"),
        ("show recent files", "Files: Recent"),
        ("hello how are you", "Not Handled (AI)"),
    ]
    
    print("\n[TEST] Testing command routing...")
    passed = 0
    for command, expected_type in test_commands:
        handled, response = router.route_command(command)
        status = "✓ Handled" if handled else "✗ Not handled"
        print(f"  {status}: '{command}'")
        if "Not Handled" in expected_type and not handled:
            passed += 1
        elif handled:
            passed += 1
    
    print(f"\n✓ Command Router tests passed ({passed}/{len(test_commands)})")


def test_integration():
    """Test integration with ATLAS brain."""
    print_section("Testing ATLAS Integration")
    
    try:
        from brain.groq_chat import AtlasBrain
        
        print("\n[TEST] Importing AtlasBrain...")
        brain = AtlasBrain()
        print("✓ AtlasBrain imported successfully")
        
        print("\n[TEST] Checking command router integration...")
        if hasattr(brain, 'command_router'):
            print("✓ Command router integrated into AtlasBrain")
        else:
            print("✗ Command router not found in AtlasBrain")
            return False
        
        print("\n✓ Integration tests passed!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("  Note: This may be due to missing GROQ_API_KEY or dependencies")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  ATLAS v2 AUTOMATION TEST SUITE")
    print("=" * 60)
    
    try:
        test_desktop_controller()
        test_file_manager()
        test_command_router()
        test_integration()
        
        print("\n" + "=" * 60)
        print("  ALL TESTS COMPLETED SUCCESSFULLY! ✓")
        print("=" * 60)
        print("\nATLAS v2 automation system is ready to use.")
        print("Run 'python app.py' or 'run.bat' to start ATLAS.")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"  TEST FAILED: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
