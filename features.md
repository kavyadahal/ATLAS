# ATLAS Features Documentation

## Overview
ATLAS v2 is an AI Operating System - a cloud-powered voice assistant with desktop control and smart file management capabilities. It combines conversational AI with system automation to provide a seamless hands-free computing experience.

---

## 🎯 Core Features

### 1. Voice Interface
- **Wake Word Activation**: Activate ATLAS by saying "Hey Jarvis"
- **Speech-to-Text (STT)**: Local speech recognition using Vosk (offline)
- **Text-to-Speech (TTS)**: Natural voice output using Piper TTS with ONNX model (Ryan voice)
- **Echo Prevention**: Smart detection to prevent ATLAS from hearing its own voice
- **Dual Input Mode**: Supports both voice commands and text input simultaneously
- **Conversation State Management**: Maintains context with 30-second timeout for follow-up questions

### 2. Conversational AI
- **Cloud-Powered Intelligence**: Uses Groq API with Llama 3.3 70B model for natural conversations
- **Context-Aware Responses**: Maintains conversation history for coherent interactions
- **Identity System**: ATLAS has a defined personality (friendly, intelligent, concise) and creator information
- **Natural Language Understanding**: Can discuss various topics, answer questions, and provide explanations
- **Memory Integration**: Recalls important information from previous conversations

### 3. Long-Term Memory System
- **Vector-Based Storage**: Uses ChromaDB for semantic memory search
- **Local ONNX Embeddings**: all-MiniLM-L6-v2 model (384 dimensions) - no API key required
- **Automatic Memory Storage**: Remembers important conversation details
- **Semantic Search**: Retrieves relevant memories based on context similarity
- **Profile Support**: Can store and recall user profile information
- **Memory Deduplication**: Avoids storing duplicate or very similar memories

---

## 🖥️ Desktop Control Features

### 4. Application Management
- **Open Applications**: Launch apps by name with fuzzy matching for voice recognition errors
  - Examples: "Open Chrome", "Launch VS Code", "Start Spotify"
  - Supports common apps: Chrome, Firefox, Edge, VSCode, Notepad, Calculator, Office apps, Discord, Spotify, Teams
- **Close Applications**: Terminate running applications by name
  - Examples: "Close Chrome", "Quit Notepad"
- **List Running Apps**: View all currently running applications
- **Fuzzy App Matching**: Handles voice recognition errors (e.g., "vscod" → "vscode", "goggle" → "google")
- **Website Apps**: Opens web services directly (YouTube, Gmail, GitHub, Reddit, Twitter, Facebook, Instagram)

### 5. Window Management
- **Minimize Windows**: Minimize application windows by name
- **Maximize Windows**: Maximize application windows by name
- **Focus Windows**: Bring specific windows to the foreground
- **Multi-Window Support**: Handles applications with multiple windows

### 6. Web Browsing
- **Open Websites**: Launch URLs in default browser
  - Supports full URLs: "Open https://example.com"
  - Supports domains: "Open google.com"
  - Auto-adds https:// protocol if missing
- **Quick Access**: Direct commands for popular sites (YouTube, Gmail, etc.)

### 7. Folder Access
- **Quick Folder Opening**: Open common system folders by name
  - Desktop, Downloads, Documents, Pictures, Videos, Music
  - Example: "Open my downloads folder"

---

## 📁 File Management Features

### 8. Smart File Creation
- **AI-Powered Content Generation**: Creates files with intelligent content based on context
- **Multi-Format Support**: Supports 13 file types:
  - Code: `.py`, `.js`, `.html`, `.css`
  - Data: `.json`, `.yaml`, `.yml`, `.csv`, `.xml`
  - Documents: `.txt`, `.md`, `.ini`, `.toml`
- **Context-Aware Content**: Generates appropriate code/content based on filename and request
  - Example: "Create calculator.py" → generates a functional calculator script
  - Example: "Create README.md" → generates project documentation template
- **Template System**: Built-in templates for common file types
- **Location Support**: Create files on Desktop, Downloads, or Documents
- **Safety Validation**: Validates filenames for security and compatibility

### 9. File Operations
- **Search Files**: Find files by name across common directories (Desktop, Downloads, Documents, Pictures)
- **Open Files**: Launch files with their default application
- **Read Files**: Display file contents (upcoming feature)
- **Edit Files**: Modify file contents with AI assistance (upcoming feature)
- **Delete Files**: Remove files with confirmation for safety
- **Create Folders**: Create new directories with custom names
- **Rename Files**: Change file names while preserving location
- **Copy Files**: Duplicate files to new locations
- **Move Files**: Relocate files to different directories
- **File Information**: Get detailed metadata (size, dates, extension)

### 10. File Organization
- **Auto-Organize Downloads**: Automatically sort downloads folder by file type
  - Categories: Documents, Images, Videos, Audio, Archives, Code, Executables
  - Handles duplicate filenames intelligently
- **Recent Files Search**: Find files modified within the last N days
- **Bulk Operations**: Process multiple files efficiently

### 11. Archive Management
- **Compress Folders**: Create ZIP archives from folders
- **Extract Archives**: Extract ZIP files to specified locations
- **Automatic Naming**: Smart default names for compressed files

---

## 🧠 Intelligence Features

### 12. Intent Detection System
- **Command vs. Conversation**: Automatically distinguishes between commands and chat
- **Priority-Based Matching**: Uses pattern priority to resolve ambiguous inputs
- **Parameter Extraction**: Intelligently extracts filenames, locations, and other parameters
- **Natural Language Patterns**: Understands variations in how commands are phrased
- **Context Sensitivity**: Differentiates between similar patterns (e.g., "open file.txt" vs "open chrome")

### 13. Command Execution
- **Unified Command Registry**: Centralized command management system
- **Modular Architecture**: Separate modules for app, file, and system commands
- **Error Handling**: Graceful failure with informative messages
- **Python Script Execution**: Run Python files directly through ATLAS

### 14. Safety & Confirmation System
- **Dangerous Operation Detection**: Identifies risky operations (file deletion, etc.)
- **Explicit Confirmation**: Requires user approval for destructive actions
- **Confirmation Dialog**: Clear yes/no prompts for dangerous operations
- **Cancel Support**: Easy cancellation of pending operations
- **State Management**: Tracks pending confirmations across interactions

---

## 🔧 System Features

### 15. Logging & Monitoring
- **Comprehensive Logging**: All operations logged with timestamps
- **Separate Log Categories**: Desktop actions, file operations, commands, errors
- **Persistent Logs**: Saved to `data/logs/automation_log.txt`
- **Debug Information**: Detailed error context for troubleshooting

### 16. Multi-Threading Architecture
- **Concurrent Input Processing**: Handles voice and text input simultaneously
- **Non-Blocking Operations**: Voice listening doesn't interrupt command processing
- **Queue-Based Processing**: Orderly processing of multiple inputs
- **Recognition ID Tracking**: Unique identifiers for each input for debugging

### 17. User Interface
- **Console UI**: Clean, colored terminal interface
- **Status Indicators**: Clear visual feedback for operations
- **Prompt System**: Consistent user prompts for input
- **Error Messages**: User-friendly error explanations
- **Processing Feedback**: Real-time status updates

### 18. Configuration Management
- **Environment Variables**: Secure API key storage via `.env` file
- **Configurable Models**: Switch between different Groq models
- **Flexible Voice Models**: Support for different Piper TTS voices
- **Path Configuration**: Customizable file paths and directories

---

## 🛠️ Technical Features

### 19. API Integration
- **Groq API**: Cloud-based LLM for chat (Llama 3.3 70B Versatile)
- **No Local LLM Required**: Fully cloud-powered intelligence
- **Free Tier Support**: Works with Groq's free tier
- **API Error Handling**: Graceful handling of network issues

### 20. Cross-Platform Components
- **Windows Integration**: Native Windows API support (pywin32)
- **Process Management**: Cross-process communication via psutil
- **Path Handling**: Platform-aware file path operations
- **System Calls**: Safe subprocess execution

### 21. Developer Tools
- **Automated Installation**: One-click setup with `install.bat`
- **Model Download Scripts**: Easy voice model acquisition
- **Test Suite**: Comprehensive testing for core functionality
  - Fuzzy matching tests
  - Intent detection tests
  - Voice variation tests
  - Automation tests
- **Cleanup Scripts**: Maintenance utilities for project cleanup

### 22. Project Structure
- **Modular Design**: Clear separation of concerns
  - `automation/`: Desktop and file control
  - `brain/`: AI intelligence and intent detection
  - `commands/`: Command registry and implementations
  - `core/`: Main orchestration and state management
  - `memory/`: Vector storage and embeddings
  - `voice/`: Speech recognition and synthesis
  - `ui/`: User interface components
- **Extensible Architecture**: Easy to add new commands and features
- **Clean Abstractions**: Well-defined interfaces between modules

---

## 📊 Supported Commands Summary

### Application Commands
- Open/launch/start [app name]
- Close/quit/kill/stop [app name]
- List running applications
- Minimize/maximize/focus [app name]

### Website Commands
- Open/go to/visit [URL or domain]
- Open [website service] (YouTube, Gmail, etc.)

### File Commands
- Create [filename] on [location]
- Create file named [name]
- Delete/remove [filename]
- Search/find files [query]
- Open [filename]
- Read [filename]
- Edit [filename]

### Folder Commands
- Create folder named [name]
- Open [folder name] (desktop/downloads/documents)
- Organize downloads

### System Commands
- What apps are running?
- Run/execute [python file]

### Conversational
- General questions and answers
- Who are you? / What is your name?
- How are you?
- Tell me about...
- Can you help with...
- Exit/quit/goodbye

---

## 🔐 Security Features

### 23. Safety Measures
- **Filename Validation**: Prevents invalid characters and reserved names
- **Permission Checks**: Handles permission errors gracefully
- **Path Sanitization**: Prevents directory traversal attacks
- **Confirmation for Destructive Actions**: Requires explicit approval for deletions
- **Process Isolation**: Each command runs in controlled environment
- **Error Boundaries**: Failures contained to prevent system crashes

---

## 🎨 User Experience Features

### 24. Voice Recognition Enhancements
- **Fuzzy Matching**: 75% similarity threshold for app names
- **Voice Error Tolerance**: Handles speech recognition mistakes
- **Multiple Pattern Support**: Understands different phrasings
- **Silence Detection**: Automatically stops listening after silence
- **Ambient Noise Handling**: Configurable silence threshold

### 25. Feedback & Responses
- **Polite Address**: Consistently addresses user as "Sir"
- **Confirmation Messages**: Clear success/failure feedback
- **Contextual Responses**: Responses tailored to the action performed
- **Error Explanations**: Helpful messages when operations fail
- **Status Updates**: Real-time progress for long operations

---

## 🚀 Upcoming Features

Based on `upcoming_featires.md`:
1. **File Reading with Explanation**: Open files, read content, and explain to user
2. **AI-Powered File Editing**: Write code logic using Groq and insert into files
3. **Inactivity Timeout**: Auto-sleep after 2 seconds of inactivity (requires re-activation)
4. **System Control**: Volume control and brightness adjustment via voice/text

---

## 📈 Performance Characteristics

- **Response Time**: Near-instant local processing, cloud API dependent for AI responses
- **Memory Footprint**: Efficient vector storage with ChromaDB
- **Offline Capabilities**: Voice recognition works offline (Vosk)
- **Concurrent Operations**: Handles multiple inputs without blocking
- **Scalability**: Memory system scales with usage

---

## 🎓 Use Cases

1. **Hands-Free Computing**: Control your computer entirely by voice
2. **Quick File Management**: Create, organize, and find files naturally
3. **Developer Productivity**: Generate code files with intelligent content
4. **Web Navigation**: Quick access to websites and online services
5. **Conversation Partner**: Ask questions and get AI-powered answers
6. **System Organization**: Keep downloads and files organized automatically
7. **Accessibility**: Voice control for users who prefer or require it
8. **Task Automation**: Combine commands for complex workflows

---

## 📝 Notes

- ATLAS requires an internet connection for AI chat features (Groq API)
- Voice models run locally for privacy and offline capability
- Memory system stores data locally in ChromaDB
- All automation operations are logged for transparency
- Designed for Windows (some features are Windows-specific)
- Continuously evolving with new features and improvements

---

**Version**: 2.0
**Last Updated**: July 2026
**Status**: Active Development
