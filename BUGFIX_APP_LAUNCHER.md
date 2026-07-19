# Application Launcher Bug Fix

## Problem Summary

ATLAS was correctly detecting app opening commands but execution was failing with errors like:
- `'google' is not recognized as an internal or external command`
- `'chrome.exe' is not recognized as an internal or external command`

The issue was that the system tried to execute app names/executables directly without proper path resolution.

## Root Cause

1. **Path Resolution Issue**: In `desktop_controller.py`, the code tried to run executables like `chrome.exe` directly using `subprocess.Popen([exe], shell=True)`, but Chrome and most apps are not in the Windows PATH.

2. **Missing Aliases**: Common aliases like "google" were not mapped to Chrome.

3. **Website Detection**: URLs without domain extensions (like "open google.com") were incorrectly routed to file/app opening instead of browser.

## Changes Made

### 1. Fixed `automation/desktop_controller.py`

**Added:**
- `'google'` and `'google chrome'` aliases for Chrome
- `'code'` and `'calc'` aliases for VS Code and Calculator
- `WEBSITE_APPS` dictionary for common web apps (YouTube, Gmail, etc.)

**Improved `open_application()` method:**
- Now uses `shutil.which()` to find executables in system PATH
- Checks multiple Program Files locations (including `%LOCALAPPDATA%\Programs`)
- Searches standard paths: `C:\Program Files`, `C:\Program Files (x86)`, `%LOCALAPPDATA%\Programs`
- Uses `shell=False` for safer subprocess execution
- Handles timeout for long-running process detection
- Returns clear error messages when apps aren't found

**Before:**
```python
# Would fail because chrome.exe is not in PATH
subprocess.Popen([exe], shell=True)
```

**After:**
```python
# Uses shutil.which to find the executable
import shutil
exe_path = shutil.which(exe_name)
if exe_path:
    subprocess.Popen([exe_path], shell=False)
```

### 2. Enhanced `brain/intent_detector.py`

**Improved website detection:**
- Added support for full URLs with protocols (`https://google.com`)
- Expanded domain extensions (added `.co`, `.uk`, `.in`, etc.)
- Increased priority to 11 (higher than app opening at 7)
- Better URL extraction from match groups

**Before:**
```python
'open_website': {
    'patterns': [
        r'open\s+(?:website\s+)?(?:www\.)?[\w\.-]+\.(?:com|org|net|io|edu|gov)',
    ],
    'priority': 9
}
```

**After:**
```python
'open_website': {
    'patterns': [
        r'open\s+(https?://[\w\.-]+(?:\.\w+)*(?:/[\w\.-]*)*)',
        r'open\s+(?:website\s+)?((?:www\.)?[\w\.-]+\.(?:com|org|net|io|...|at)(?:/[\w\.-]*)*)',
    ],
    'priority': 11  # Higher than app opening
}
```

### 3. Updated `automation/command_router.py`

**Enhanced website command detection:**
- Added protocol detection (`https://`)
- Expanded domain extension list
- Better URL extraction with fallback logic

## Supported Commands Now

### Application Opening
```
✓ open google          → Opens Chrome
✓ open chrome          → Opens Chrome
✓ open google chrome   → Opens Chrome
✓ open vscode          → Opens VS Code
✓ open code            → Opens VS Code
✓ open visual studio code → Opens VS Code
✓ open notepad         → Opens Notepad
✓ open calculator      → Opens Calculator
✓ open calc            → Opens Calculator
```

### Website Opening
```
✓ open youtube         → Opens YouTube in browser
✓ open gmail           → Opens Gmail in browser
✓ open google.com      → Opens Google in browser
✓ open youtube.com     → Opens YouTube in browser
✓ open https://google.com → Opens Google in browser
✓ go to reddit.com     → Opens Reddit in browser
✓ visit github.com     → Opens GitHub in browser
```

### Website Apps (Auto-redirect)
The following commands now open websites instead of searching for apps:
- `open youtube` → https://www.youtube.com
- `open gmail` → https://mail.google.com
- `open github` → https://github.com
- `open reddit` → https://www.reddit.com
- `open twitter` → https://twitter.com
- `open facebook` → https://www.facebook.com
- `open instagram` → https://www.instagram.com

## How It Works

1. **Intent Detection**: User says "open google"
2. **Routing**: `intent_detector.py` detects `open_app` intent with `app_name='google'`
3. **Execution**: `desktop_controller.py` checks if "google" is in `COMMON_APPS`
4. **Resolution**: Finds Chrome executable using:
   - `shutil.which('chrome.exe')` (checks PATH)
   - Direct path check in Program Files directories
5. **Launch**: Opens Chrome with `subprocess.Popen([exe_path], shell=False)`

## Error Handling

The system now provides clear error messages:
- **App not found**: "I couldn't find {app_name}, Sir. Please ensure it's installed."
- **Generic error**: "An error occurred while trying to open {app_name}, Sir."

## Testing Recommendations

Run the following commands to verify:

```python
# Test in Python console
from automation.desktop_controller import DesktopController
dc = DesktopController()

# Test app opening
dc.open_application('google')        # Should open Chrome
dc.open_application('chrome')        # Should open Chrome
dc.open_application('vscode')        # Should open VS Code
dc.open_application('notepad')       # Should open Notepad

# Test website apps
dc.open_application('youtube')       # Should open YouTube in browser
dc.open_application('gmail')         # Should open Gmail in browser

# Test website opening
dc.open_website('google.com')        # Should open Google
dc.open_website('https://github.com') # Should open GitHub
```

## Files Modified

1. `automation/desktop_controller.py` - Core application launcher logic
2. `brain/intent_detector.py` - Intent detection patterns and priorities
3. `automation/command_router.py` - Command routing and website detection

## No Changes Made To

As requested, the following were NOT modified:
- AI provider configuration
- Memory system
- Voice system
- Project architecture
- Existing command functionality
- README/documentation files (except this bugfix doc)

## Notes

- The fix maintains backward compatibility
- All existing commands continue to work
- Error messages are user-friendly and clear
- The system is more robust with better path detection
- Security improved by using `shell=False` in subprocess calls
