# ATLAS v2 – Automation Features Guide

## Overview

ATLAS has been extended with desktop control and smart file system capabilities, transforming it from an AI assistant into an AI Operating System. The existing conversational AI functionality remains fully intact while new automation features have been added.

---

## Architecture

The automation system is implemented in a modular architecture:

```
atlas/
├── automation/
│   ├── __init__.py
│   ├── desktop_controller.py    # Desktop operations
│   ├── file_manager.py          # File operations
│   ├── command_router.py        # Command routing & intent detection
│   └── logger.py                # Logging system
├── brain/
│   └── groq_chat.py             # Updated with automation integration
└── logs/                        # Auto-generated log files
```

### Key Components

1. **DesktopController**: Manages desktop operations (open/close apps, window management)
2. **FileManager**: Handles file system operations (search, move, copy, delete, organize)
3. **CommandRouter**: Routes natural language commands to appropriate handlers
4. **AutomationLogger**: Logs all operations with timestamps and status

---

## Desktop Control Features

### Opening Applications

**Commands:**
- "Open Chrome"
- "Launch VS Code"
- "Start Spotify"
- "Run Calculator"

**Supported Applications:**
- Chrome, Firefox, Edge
- VS Code, Visual Studio
- Notepad, Calculator
- Spotify, Discord, Teams
- Microsoft Office (Word, Excel, PowerPoint, Outlook)
- And more...

### Closing Applications

**Commands:**
- "Close Chrome"
- "Quit Spotify"
- "Stop Discord"

**Safety:** ATLAS will close the application immediately but logs the action.

### Opening Websites

**Commands:**
- "Open GitHub"
- "Open google.com"
- "Go to youtube.com"
- "Visit stackoverflow.com"

**Note:** URLs can be provided with or without `https://`

### Opening Folders

**Commands:**
- "Open Downloads"
- "Open my Desktop"
- "Open Documents folder"
- "Open Pictures"

**Supported Folders:**
- Desktop
- Downloads
- Documents
- Pictures
- Videos
- Music

### Listing Running Applications

**Commands:**
- "What applications are running?"
- "List running apps"
- "Show running applications"

### Window Management

**Minimize:**
- "Minimize Chrome"
- "Minimize VS Code"

**Maximize:**
- "Maximize Chrome"
- "Maximize Notepad"

**Focus:**
- "Focus VS Code"
- "Switch to Chrome"

**Note:** Window management requires the `pywin32` package.

---

## File System Features

### Searching Files

**Commands:**
- "Find my resume"
- "Search for report.pdf"
- "Where is my presentation?"
- "Locate budget spreadsheet"

**Features:**
- Searches common locations (Desktop, Downloads, Documents, Pictures)
- Returns up to 5 results with full paths
- Shows file size and modification date

### Creating Folders

**Commands:**
- "Create a folder called AI Projects"
- "Make a folder named Work"
- "New folder Documents Backup"

**Note:** Folders are created in Downloads by default.

### Organizing Downloads

**Commands:**
- "Organize Downloads"
- "Clean up Downloads"
- "Sort Downloads folder"

**Features:**
- Automatically categorizes files by type:
  - Documents (PDF, DOC, DOCX, TXT, XLS, PPT, etc.)
  - Images (JPG, PNG, GIF, BMP, SVG, etc.)
  - Videos (MP4, AVI, MKV, MOV, etc.)
  - Audio (MP3, WAV, FLAC, AAC, etc.)
  - Archives (ZIP, RAR, 7Z, TAR, etc.)
  - Code (PY, JS, JAVA, CPP, HTML, CSS, etc.)
  - Executables (EXE, MSI, BAT, etc.)
- Creates category folders and moves files
- Handles duplicate filenames

### Recent Files

**Commands:**
- "Show recent files"
- "Files modified today"
- "Show files modified this week"

**Features:**
- Shows files modified within specified timeframe
- Default: 1 day
- Searches Desktop, Downloads, and Documents
- Returns up to 10 most recent files

### File Operations

**Rename, Move, Copy:**
These operations require specific file paths and are currently simplified in the command router. For advanced usage, import the FileManager directly:

```python
from automation.file_manager import FileManager

fm = FileManager()
success, msg = fm.rename_file("C:/path/to/old.txt", "new.txt")
success, msg = fm.move_file("C:/path/to/file.txt", "C:/destination/")
success, msg = fm.copy_file("C:/path/to/file.txt", "C:/destination/")
```

### Deleting Files (Safety First!)

**Commands:**
- "Delete old_notes.txt"

**Safety Features:**
- ATLAS will search for the file
- Show the file path found
- **Require explicit confirmation** before deletion
- User must say "yes, delete it" to proceed

### Compression & Extraction

**Compress Folder:**
```python
from automation.file_manager import FileManager

fm = FileManager()
success, msg = fm.compress_folder("C:/path/to/folder")
# Creates folder.zip
```

**Extract ZIP:**
```python
success, msg = fm.extract_zip("C:/path/to/archive.zip")
# Extracts to folder with same name
```

---

## Safety Features

### Confirmation Required

ATLAS requires user confirmation before:
- Deleting files or folders
- Overwriting existing files
- Any irreversible operation

### Logging

All operations are logged to `logs/atlas_automation_YYYYMMDD.log` with:
- Timestamp
- Action type
- Target file/application
- Success or failure status
- Error messages (if any)

**Example Log Entry:**
```
2026-07-19 05:30:15 - ATLAS.Automation - INFO - Desktop Action: OPEN | Target: chrome | Status: SUCCESS
2026-07-19 05:30:42 - ATLAS.Automation - INFO - File Action: SEARCH | Source: resume | Status: SUCCESS
```

### Error Handling

The system gracefully handles:
- File not found
- Application not installed
- Permission denied
- Invalid paths
- File already exists

Returns user-friendly error messages instead of crashing.

---

## Integration with Existing ATLAS

The automation system integrates seamlessly with the existing ATLAS codebase:

1. **Preserved Functionality**: All existing conversational AI features work exactly as before
2. **Intent Detection**: The CommandRouter checks each message first
3. **Fallback to AI**: If not a system command, ATLAS uses the normal AI chat flow
4. **Memory System**: Works alongside the existing vector memory
5. **Voice Interface**: Compatible with the existing voice input/output

---

## Usage Examples

### Example Session 1: Opening Apps
```
You: Open Chrome
ATLAS: Successfully opened chrome, Sir.

You: Launch VS Code
ATLAS: Successfully opened vscode, Sir.

You: What applications are running?
ATLAS: Currently running applications: chrome.exe, Code.exe, explorer.exe, and 12 more, Sir.
```

### Example Session 2: File Management
```
You: Find my resume
ATLAS: I found 1 file(s), Sir:
1. Resume_2026.pdf (C:\Users\Hp\Documents\Resume_2026.pdf)

You: Organize Downloads
ATLAS: Successfully organized 45 files in Downloads, Sir.

You: Show recent files
ATLAS: I found 8 file(s) modified in the last 1 day(s), Sir. Here are the most recent:
1. project_notes.txt - 2026-07-19 05:15:23
2. meeting_agenda.docx - 2026-07-19 04:30:11
...
```

### Example Session 3: Mixed Commands
```
You: Open GitHub
ATLAS: Opening https://github.com, Sir.

You: What's the weather like?
ATLAS: [Uses AI model to respond conversationally]

You: Create a folder called New Project
ATLAS: Successfully created the folder, Sir.
```

---

## Installation

### Install New Dependencies

Run the installation script to install the new packages:

```bash
pip install -r requirements.txt
```

**New dependencies added:**
- `psutil==6.1.1` - For process management
- `pywin32==308` - For window management (Windows only)

### Verify Installation

```python
python -c "import psutil; import win32gui; print('Dependencies installed successfully')"
```

---

## Extending the System

### Adding New Desktop Applications

Edit `automation/desktop_controller.py`:

```python
COMMON_APPS = {
    'your_app': ['YourApp.exe', 'Path\\To\\YourApp.exe'],
    # ... existing apps
}
```

### Adding New File Categories

Edit `automation/file_manager.py`:

```python
FILE_CATEGORIES = {
    'your_category': ['.ext1', '.ext2', '.ext3'],
    # ... existing categories
}
```

### Adding New Commands

Edit `automation/command_router.py` to add new pattern matching and handlers.

---

## Troubleshooting

### Application Not Opening

**Issue:** "I couldn't find or open [app]"

**Solutions:**
1. Check if the application is installed
2. Add the application to `COMMON_APPS` with correct path
3. Try using the full executable name (e.g., "chrome.exe")

### Window Management Not Working

**Issue:** "Window management requires pywin32 package"

**Solution:**
```bash
pip install pywin32
```

### Permission Denied

**Issue:** "Permission denied" when accessing files

**Solutions:**
1. Run ATLAS with appropriate permissions
2. Check if the file is open in another application
3. Verify file/folder permissions

### Logs Not Created

**Issue:** Log files not appearing

**Solution:**
- Logs are created in `logs/` directory
- Check if directory has write permissions
- Look for console output for errors

---

## Best Practices

1. **Be Specific**: Use clear, specific commands (e.g., "Open Chrome" vs. "Open browser")
2. **Confirm Dangerous Actions**: Always confirm before deleting files
3. **Check Logs**: Review logs to track operations
4. **Use Paths**: For complex file operations, provide full paths
5. **Test First**: Test automation commands in a safe environment first

---

## Future Enhancements

Potential areas for expansion:
- Screen capture and image recognition
- Clipboard management
- Scheduled tasks and automation
- System monitoring and alerts
- Integration with external services (email, calendar, etc.)
- Multi-monitor support
- Keyboard shortcut execution
- Process automation and scripting

---

## Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Check file/folder permissions

---

## License

This automation module is part of the ATLAS project and follows the same license as the main project.

---

**ATLAS v2** - Your AI Operating System
