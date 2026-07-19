# ATLAS Architecture Documentation

## Overview

ATLAS is a true desktop AI assistant that executes commands directly rather than explaining how to do them. The system intelligently routes user requests to either direct execution or conversational AI based on intent detection.

## System Flow

```
Voice / Terminal Input
        │
        ▼
process_user_input(text)
        │
        ▼
Intent Detector
        │
 ┌──────┴────────┐
 │               │
 ▼               ▼
Executable?      Chat?
 │               │
Yes              No
 │               │
 ▼               ▼
Executor      Groq Chat
 │               │
 └──────┬────────┘
        ▼
Speaker + Console
```

## Core Principle

**ATLAS must NEVER ask Groq how to perform an action that ATLAS itself is capable of performing.**

If a request is executable (file operations, app control, system commands), it bypasses Groq entirely and executes directly.

## Architecture Components

### 1. Intent Detector (`brain/intent_detector.py`)

**Purpose**: Classify user input as either a command or conversation.

**Supported Intents**:
- `create_file` - Create a new file
- `create_folder` - Create a new folder
- `delete_file` - Delete a file
- `search_files` - Search for files
- `open_app` - Open an application
- `close_app` - Close an application
- `open_website` - Open a URL in browser
- `open_folder` - Open system folders
- `organize_downloads` - Organize Downloads folder
- `list_apps` - List running applications
- `run_python` - Execute Python scripts
- `chat` - Conversational query (sent to Groq)

**How It Works**:
1. Checks for conversation indicators (who, what, why, explain, etc.)
2. Matches user input against command patterns using regex
3. Extracts parameters from the matched pattern
4. Returns intent name and parameters dictionary

**Example**:
```python
Input: "Create a text file on my desktop"
Output: ('create_file', {'filename': 'newfile.txt', 'location': 'desktop'})

Input: "What is Python?"
Output: ('chat', None)
```

### 2. Command Executor (`brain/executor.py`)

**Purpose**: Execute detected commands using automation modules.

**Dependencies**:
- `automation.desktop_controller` - Application and system control
- `automation.file_manager` - File and folder operations

**Execution Flow**:
1. Receives intent name and parameters from Intent Detector
2. Routes to appropriate handler method (`_handle_{intent}`)
3. Executes the command using automation modules
4. Returns (success: bool, message: str)

**File Operations**:
- Create files/folders
- Delete files
- Search files
- Organize downloads

**Application Control**:
- Open/close applications
- Open websites
- Open system folders
- List running applications

**System Operations**:
- Run Python scripts
- Execute system commands

### 3. Automation Modules

#### File Manager (`automation/file_manager.py`)

**Capabilities**:
- Search files and folders
- Create/delete files and folders
- Copy/move/rename files
- Compress/extract ZIP files
- Organize files by type
- Get recent files
- File information retrieval

**Example**:
```python
files.create_file("C:/Users/Hp/Desktop/test.txt")
# Returns: (True, "Successfully created the file, Sir.")
```

#### Desktop Controller (`automation/desktop_controller.py`)

**Capabilities**:
- Open/close applications
- Open websites in browser
- Open system folders (Desktop, Downloads, etc.)
- List running applications
- Window management (minimize, maximize, focus)
- Search for installed applications

**Supported Applications**:
- Chrome, Firefox, Edge
- VS Code, Notepad
- Calculator, Explorer
- Spotify, Discord, Teams
- Office applications (Word, Excel, PowerPoint)
- And more...

**Example**:
```python
desktop.open_application("chrome")
# Returns: (True, "Successfully opened chrome, Sir.")
```

### 4. Groq Chat Integration (`brain/groq_chat.py`)

**Purpose**: Handle conversational queries using Groq LLM.

**When Used**:
- Questions (who, what, why, how)
- Explanations
- General conversation
- Information requests
- Identity questions

**Features**:
- Memory integration via ChromaDB
- Context-aware responses
- Identity and creator information
- Maintains conversation history

### 5. Main Application (`app.py`)

**Input Handling**:
- Concurrent voice and keyboard input
- Wake word detection ("Hey Jarvis")
- Conversation mode with timeout
- Thread-safe queue processing

**Processing Pipeline**:
```python
def process_user_input(text):
    # 1. Detect intent
    intent, params = intent_detector.detect_intent(text)
    
    # 2. Route based on intent
    if intent == 'chat':
        # Send to Groq
        reply = atlas.chat(text)
    else:
        # Execute command
        success, message = executor.execute(intent, params)
    
    # 3. Output result
    print(message)
    speaker.speak(message)
```

## Examples

### Executable Commands

**File Creation**:
```
User: "Create a text file on my desktop"
ATLAS: [Executes directly] "Created newfile.txt on desktop, Sir."
```

**Application Control**:
```
User: "Open Chrome"
ATLAS: [Executes directly] "Successfully opened chrome, Sir."
```

**File Search**:
```
User: "Find my Python files"
ATLAS: [Executes directly] "I found 5 file(s), Sir: ..."
```

**Folder Operations**:
```
User: "Organize my downloads"
ATLAS: [Executes directly] "Successfully organized 12 files in Downloads, Sir."
```

### Conversational Queries

**Questions**:
```
User: "What is Python?"
ATLAS: [Sends to Groq] "Python is a high-level programming language..."
```

**Identity**:
```
User: "Who created you?"
ATLAS: [Quick response] "I was created by [creator], Sir."
```

**Explanations**:
```
User: "Explain how machine learning works"
ATLAS: [Sends to Groq] "Machine learning is a subset of AI..."
```

## Intent Detection Logic

### Priority System

Commands are checked in priority order (higher = checked first):

1. **Priority 10**: File operations (create, delete)
2. **Priority 9**: Specific commands (search, websites, Python)
3. **Priority 8**: Application control (open, close)
4. **Priority 7**: System commands (list apps, organize)

### Conversation Indicators

If input contains these patterns, it's treated as chat:
- who are you, what is your name
- how are you
- what is/are, why, explain
- tell me about
- can you help/assist/tell
- thanks, hello, hi, goodbye

### Pattern Matching

Uses regex patterns to extract commands and parameters:

```python
Pattern: r'create\s+(?:a\s+)?(?:text\s+)?file\s+(?:named\s+|called\s+)?(.+?)(?:\s+(?:in|on|at)\s+(.+))?$'

Match: "create a text file named test.txt on desktop"
Extracted: filename='test.txt', location='desktop'
```

## Adding New Intents

### Step 1: Add Pattern to Intent Detector

```python
'new_intent': {
    'patterns': [
        r'pattern1',
        r'pattern2',
    ],
    'priority': 8
}
```

### Step 2: Add Parameter Extraction

```python
elif intent == 'new_intent':
    params['param1'] = match.group(1).strip()
```

### Step 3: Add Handler to Executor

```python
def _handle_new_intent(self, params: Dict[str, Any]) -> Tuple[bool, str]:
    """Handle new intent."""
    # Implementation
    return True, "Successfully executed, Sir."
```

## Key Design Decisions

### 1. No Groq for Executable Tasks
Commands that ATLAS can execute directly never reach Groq. This ensures fast, reliable execution.

### 2. Pattern-Based Detection
Regex patterns provide precise command matching without LLM overhead.

### 3. Modular Architecture
Separation of concerns:
- Intent detection (brain/)
- Command execution (brain/executor.py)
- Automation (automation/)
- Conversation (brain/groq_chat.py)

### 4. Graceful Fallback
Unknown commands return helpful error messages, not crashes.

### 5. User Confirmation
Destructive operations (delete, overwrite) request confirmation.

## Performance

- **Intent Detection**: < 10ms (regex-based)
- **Command Execution**: 50-500ms (depending on operation)
- **Groq Chat**: 500-2000ms (API call)

Direct execution is 10-40x faster than LLM-based routing.

## Future Enhancements

### Potential New Intents:
- `screenshot` - Take a screenshot
- `clipboard` - Clipboard operations
- `email` - Send emails
- `calendar` - Calendar management
- `reminder` - Set reminders
- `volume_control` - System volume
- `brightness_control` - Screen brightness
- `wifi_control` - Network management
- `battery_status` - Power information

### Improvements:
- Natural language file path parsing
- Multi-step command chains
- User preference learning
- Command history and undo
- Voice command confirmation for destructive ops

## Conclusion

ATLAS achieves its goal of being a true desktop assistant by:

1. **Intelligent routing** between execution and conversation
2. **Direct command execution** for actionable tasks
3. **LLM integration** for conversational needs
4. **Fast, reliable performance** through pattern matching
5. **Modular, extensible architecture** for easy enhancement

The system ensures that when you say "Create a file," ATLAS creates a file—it doesn't explain how to create one.
