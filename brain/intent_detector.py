"""
Intent Detection Module
Determines whether user input is a command to execute or a conversation to have.
"""

import re
from typing import Tuple, Optional, Dict, Any


class IntentDetector:
    """Detects user intent and extracts command parameters."""
    
    # Command patterns with priorities (higher = checked first)
    COMMAND_PATTERNS = {
        # File Operations - PART 2 & 3: Smart file creation with content
        'create_file_with_content': {
            'patterns': [
                # PART 3: Flexible patterns for writing code/content to files
                # Match "write [content/description] in/to filename.ext" - for cases like "write hello world in test.py"
                r'write\s+.+?\s+(?:in|to)\s+([a-zA-Z0-9_\-]+\.(?:py|js|html|css|json|md|yaml|yml|txt))\b',
                # Match "write [anything] in/to filename.ext" (catches "write X in file.py")
                r'write\s+(?:a\s+)?(?:some\s+)?(?:simple\s+)?(?:python\s+|javascript\s+|js\s+|html\s+|css\s+)?(?:code|script|function|program)?\s+(?:in|to)\s+([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)',
                r'write\s+(?:a\s+)?(?:python\s+|code\s+)?(?:file|script)\s+(?:in\s+)?([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)',
                # Match "generate [anything] in/to filename.ext"
                r'generate\s+(?:a\s+)?(?:some\s+)?(?:simple\s+)?(?:python\s+|javascript\s+|js\s+|html\s+|css\s+)?(?:code|script|function|program)?\s+(?:in|to|for)\s+([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)',
                r'generate\s+[a-zA-Z0-9_\-\s]+\s+(?:in|to|for)\s+([a-zA-Z0-9_\-]+\.(?:py|js|html|css|json|md|yaml|yml|txt))',
                r'generate\s+(?:a\s+)?(?:python\s+|code\s+)?(?:file|script)\s+(?:in\s+)?([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)',
                # Match "add [anything] to filename.ext"
                r'add\s+(?:a\s+)?(?:some\s+)?(?:simple\s+)?(?:python\s+|javascript\s+|js\s+)?(?:code|function|script)?\s+to\s+([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)',
                # Match "create filename.ext with/containing [content]"
                r'create\s+(?:a\s+)?([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+).+(?:containing|with|that\s+(?:has|says|includes))',
                r'make\s+(?:a\s+)?([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+).+(?:containing|with|that\s+(?:has|says|includes))',
                # Match code file creation with purpose
                r'create\s+([a-zA-Z0-9_\-]+\.(?:py|js|html|css|json|md|yaml|yml))\s+(?:for|that|to|which)',
                # With explicit content instructions
                r'create\s+([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)\s+(?:write|containing)',
                r'make\s+([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)\s+(?:write|containing)',
            ],
            'priority': 11
        },
        'create_file': {
            'patterns': [
                # Just filename (no keywords) - highest priority - must have extension
                r'^create\s+([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)(?:\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents))?$',
                r'^make\s+([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)(?:\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents))?$',
                # With "file" keyword and specific filename
                r'^create\s+(?:a\s+)?(?:text\s+|python\s+)?file\s+(?:named\s+|called\s+)([a-zA-Z0-9_\-]+(?:\.[a-zA-Z0-9]+)?)(?:\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents))?$',
                r'^make\s+(?:a\s+)?(?:text\s+|python\s+)?file\s+(?:named\s+|called\s+)([a-zA-Z0-9_\-]+(?:\.[a-zA-Z0-9]+)?)(?:\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents))?$',
                r'^new\s+file\s+(?:named\s+|called\s+)([a-zA-Z0-9_\-]+(?:\.[a-zA-Z0-9]+)?)(?:\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents))?$',
                # Generic "create file" without specific name - no capture groups for filename
                r'^create\s+(?:a\s+)?(?:text\s+|python\s+)?file$',
                r'^make\s+(?:a\s+)?(?:text\s+|python\s+)?file$',
                r'^new\s+(?:text\s+)?file$',
                # Generic with location
                r'^create\s+(?:a\s+)?(?:text\s+|python\s+)?file\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents)$',
                r'^make\s+(?:a\s+)?(?:text\s+|python\s+)?file\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents)$',
                r'^new\s+(?:text\s+)?file\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents)$',
            ],
            'priority': 10
        },
        'create_folder': {
            'patterns': [
                # With specific folder name
                r'^create\s+(?:a\s+)?folder\s+(?:named\s+|called\s+)([a-zA-Z0-9_\-]+)(?:\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents))?$',
                r'^make\s+(?:a\s+)?folder\s+(?:named\s+|called\s+)([a-zA-Z0-9_\-]+)(?:\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents))?$',
                r'^new\s+folder\s+(?:named\s+|called\s+)([a-zA-Z0-9_\-]+)(?:\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents))?$',
                # Generic "create folder" without specific name
                r'^create\s+(?:a\s+)?folder$',
                r'^make\s+(?:a\s+)?folder$',
                r'^new\s+folder$',
                # Generic with location
                r'^create\s+(?:a\s+)?folder\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents)$',
                r'^make\s+(?:a\s+)?folder\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents)$',
                r'^new\s+folder\s+(?:in|on|at)\s+(?:my\s+)?(desktop|downloads|documents)$',
            ],
            'priority': 10
        },
        'delete_file': {
            'patterns': [
                # File with extension (highest priority)
                r'delete\s+([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)',
                r'remove\s+([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)',
                r'del\s+([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)',
                # With "file" keyword
                r'delete\s+(?:the\s+)?file\s+([a-zA-Z0-9_\-\.]+(?:\.[a-zA-Z0-9]+)?)',
                r'remove\s+(?:the\s+)?file\s+([a-zA-Z0-9_\-\.]+(?:\.[a-zA-Z0-9]+)?)',
            ],
            'priority': 10
        },
        'search_files': {
            'patterns': [
                r'find\s+(?:my\s+)?(?:the\s+)?files?\s+(?:named\s+|called\s+)?(.+)',
                r'search\s+for\s+(?:the\s+)?files?\s+(?:named\s+)?(.+)',
                r'where\s+is\s+(?:the\s+)?file\s+(.+)',
                r'locate\s+(?:the\s+)?file\s+(.+)',
            ],
            'priority': 9
        },
        'open_file': {
            'patterns': [
                r'open\s+([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)',
            ],
            'priority': 9
        },
        'read_file': {
            'patterns': [
                r'read\s+(?:file\s+)?([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)',
                r'show\s+(?:me\s+)?(?:file\s+)?([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)',
            ],
            'priority': 9
        },
        'edit_file': {
            'patterns': [
                r'edit\s+(?:file\s+)?([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)',
            ],
            'priority': 9
        },
        
        # Application Control (Lower priority - only matches non-file names)
        'open_app': {
            'patterns': [
                r'open\s+([a-zA-Z][a-zA-Z0-9\s]*?)(?:\s|$)(?![a-zA-Z0-9_\-]*\.[a-zA-Z])',
                r'launch\s+([a-zA-Z][a-zA-Z0-9\s]*)',
                r'start\s+([a-zA-Z][a-zA-Z0-9\s]*)',
            ],
            'priority': 7
        },
        'close_app': {
            'patterns': [
                r'close\s+(\w+(?:\s+\w+)?)',
                r'quit\s+(\w+(?:\s+\w+)?)',
                r'kill\s+(\w+(?:\s+\w+)?)',
                r'stop\s+(\w+(?:\s+\w+)?)',
            ],
            'priority': 8
        },
        
        # Website/URL (higher priority to catch domains before apps)
        'open_website': {
            'patterns': [
                # Full URLs with protocol
                r'open\s+(https?://[\w\.-]+(?:\.\w+)*(?:/[\w\.-]*)*)',
                r'go\s+to\s+(https?://[\w\.-]+(?:\.\w+)*(?:/[\w\.-]*)*)',
                r'visit\s+(https?://[\w\.-]+(?:\.\w+)*(?:/[\w\.-]*)*)',
                # Domains with extension
                r'open\s+(?:website\s+)?((?:www\.)?[\w\.-]+\.(?:com|org|net|io|edu|gov|co|uk|in|de|fr|jp|cn|au|br|ru|it|es|nl|ca|mx|kr|se|no|fi|dk|pl|be|ch|at)(?:/[\w\.-]*)*)',
                r'go\s+to\s+((?:www\.)?[\w\.-]+\.(?:com|org|net|io|edu|gov|co|uk|in|de|fr|jp|cn|au|br|ru|it|es|nl|ca|mx|kr|se|no|fi|dk|pl|be|ch|at)(?:/[\w\.-]*)*)',
                r'visit\s+((?:www\.)?[\w\.-]+\.(?:com|org|net|io|edu|gov|co|uk|in|de|fr|jp|cn|au|br|ru|it|es|nl|ca|mx|kr|se|no|fi|dk|pl|be|ch|at)(?:/[\w\.-]*)*)',
            ],
            'priority': 11
        },
        
        # Folder Operations
        'open_folder': {
            'patterns': [
                r'open\s+(?:my\s+)?(desktop|downloads|documents|pictures|videos|music)',
            ],
            'priority': 8
        },
        'organize_downloads': {
            'patterns': [
                r'organize\s+(?:my\s+)?downloads',
                r'clean\s+(?:up\s+)?(?:my\s+)?downloads',
                r'sort\s+(?:my\s+)?downloads',
            ],
            'priority': 7
        },
        
        # System Commands
        'list_apps': {
            'patterns': [
                r'what\s+(?:apps|applications)\s+are\s+running',
                r'list\s+running\s+(?:apps|applications)',
                r'show\s+running\s+(?:apps|applications)',
                r'which\s+(?:apps|applications)\s+are\s+running',
            ],
            'priority': 7
        },
        
        # Python execution
        'run_python': {
            'patterns': [
                r'run\s+(?:python\s+)?(?:file\s+)?(.+\.py)',
                r'execute\s+(?:python\s+)?(?:file\s+)?(.+\.py)',
            ],
            'priority': 9
        },
    }
    
    # Conversational indicators (if these are present, treat as chat)
    CONVERSATION_INDICATORS = [
        r'\bwho\s+are\s+you\b',
        r'\bwhat\s+is\s+your\s+name\b',
        r'\bhow\s+are\s+you\b',
        r'\bwhat\s+(?:is|are)\b',
        r'\bwhy\s+',
        r'\bexplain\b',
        r'\btell\s+me\s+about\b',
        r'\bcan\s+you\s+(?:help|assist|tell)\b',
        r'\b(?:thanks|thank\s+you)\b',
        r'^\s*hello\b',  # Only match "hello" at the start (greeting context)
        r'^\s*hi\b',     # Only match "hi" at the start (greeting context)
        r'\bgoodbye\b',
    ]
    
    def __init__(self):
        """Initialize the intent detector."""
        pass
    
    def detect_intent(self, text: str) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Detect the intent of user input.
        
        Args:
            text: User input text
            
        Returns:
            Tuple of (intent_name, parameters_dict)
            Returns ('chat', None) if no command detected
        """
        text_lower = text.lower().strip()
        
        # Check if it's clearly a conversation (before stripping prefixes)
        for indicator in self.CONVERSATION_INDICATORS:
            if re.search(indicator, text_lower):
                return ('chat', None)
        
        # Strip common conversational prefixes to extract the core command
        # This allows "Can you create file.txt" to match "create file.txt"
        conversational_prefixes = [
            r'^(?:can|could|would|will)\s+you\s+(?:please\s+)?',
            r'^please\s+',
            r'^(?:i\s+want\s+you\s+to|i\s+need\s+you\s+to|i\s+would\s+like\s+you\s+to)\s+',
            r'^(?:i\s+want\s+to|i\s+need\s+to|i\s+would\s+like\s+to)\s+',
            r'^atlas[,\s]+',
            r'^hey[,\s]+',
        ]
        
        normalized_text = text_lower
        for prefix_pattern in conversational_prefixes:
            normalized_text = re.sub(prefix_pattern, '', normalized_text)
        
        # Check command patterns by priority
        sorted_commands = sorted(
            self.COMMAND_PATTERNS.items(),
            key=lambda x: x[1]['priority'],
            reverse=True
        )
        
        for intent_name, intent_data in sorted_commands:
            for pattern in intent_data['patterns']:
                # Try matching against normalized text (with prefixes stripped)
                match = re.search(pattern, normalized_text)
                if match:
                    # Extract parameters from match groups
                    params = self._extract_parameters(intent_name, match, text)
                    return (intent_name, params)
        
        # No command detected, treat as conversation
        return ('chat', None)
    
    def _extract_parameters(
        self,
        intent: str,
        match: re.Match,
        original_text: str
    ) -> Dict[str, Any]:
        """
        Extract parameters from regex match based on intent type.
        
        Args:
            intent: The detected intent
            match: Regex match object
            original_text: Original user input
            
        Returns:
            Dictionary of parameters
        """
        params = {'original_text': original_text}
        
        if intent == 'create_file_with_content':
            # Extract filename from pattern
            if match.lastindex and match.lastindex >= 1 and match.group(1):
                filename = match.group(1).strip()
                # Ensure extension exists
                if '.' not in filename:
                    filename += '.txt'
                params['filename'] = filename
                params['has_content_intent'] = True
                
                # Try to extract location if specified
                if match.lastindex >= 2 and match.group(2):
                    params['location'] = match.group(2).strip()
                else:
                    params['location'] = 'desktop'
            else:
                params['filename'] = 'newfile.txt'
                params['location'] = 'desktop'
                params['has_content_intent'] = True
        
        elif intent == 'create_file':
            # Check if filename was captured
            if match.lastindex and match.lastindex >= 1 and match.group(1):
                filename = match.group(1).strip()
                # Ensure .txt extension if no extension provided
                if '.' not in filename:
                    filename += '.txt'
                params['filename'] = filename
                
                # Extract location if provided
                if match.lastindex >= 2 and match.group(2):
                    params['location'] = match.group(2).strip()
                else:
                    params['location'] = 'desktop'
            else:
                # No filename provided, use default
                params['filename'] = 'example.txt'
                # Check if location is in group 1 when no filename
                if match.lastindex and match.lastindex >= 1 and match.group(1):
                    params['location'] = match.group(1).strip()
                else:
                    params['location'] = 'desktop'
        
        elif intent == 'create_folder':
            # Check if folder name was captured
            if match.lastindex and match.lastindex >= 1 and match.group(1):
                params['folder_name'] = match.group(1).strip()
                if match.lastindex >= 2 and match.group(2):
                    params['location'] = match.group(2).strip()
                else:
                    params['location'] = 'desktop'
            else:
                # No folder name provided, use default
                params['folder_name'] = 'NewFolder'
                # Check if location is in group 1 when no folder name
                if match.lastindex and match.lastindex >= 1 and match.group(1):
                    params['location'] = match.group(1).strip()
                else:
                    params['location'] = 'desktop'
        
        elif intent in ['delete_file', 'search_files', 'open_file', 'read_file', 'edit_file']:
            if match.lastindex and match.lastindex >= 1:
                filename = match.group(1).strip()
                params['filename'] = filename
                if intent == 'delete_file':
                    params['query'] = filename  # For backward compatibility
        
        elif intent in ['open_app', 'close_app']:
            if match.lastindex and match.lastindex >= 1:
                params['app_name'] = match.group(1).strip()
        
        elif intent == 'open_website':
            # Try to get URL from match groups first
            if match.lastindex and match.lastindex >= 1:
                params['url'] = match.group(1).strip()
            else:
                # Fallback to regex search
                url_match = re.search(
                    r'(?:https?://)?(?:www\.)?[\w\.-]+\.(?:com|org|net|io|edu|gov|co|uk|in|de|fr|jp|cn|au|br|ru|it|es|nl|ca|mx|kr|se|no|fi|dk|pl|be|ch|at)(?:/[\w\.-]*)*',
                    original_text.lower()
                )
                if url_match:
                    params['url'] = url_match.group(0)
        
        elif intent == 'open_folder':
            if match.lastindex and match.lastindex >= 1:
                params['folder'] = match.group(1).strip()
        
        elif intent == 'run_python':
            if match.lastindex and match.lastindex >= 1:
                params['filename'] = match.group(1).strip()
        
        return params
    
    def is_command(self, text: str) -> bool:
        """
        Quick check if text is likely a command.
        
        Args:
            text: User input
            
        Returns:
            True if text appears to be a command
        """
        intent, _ = self.detect_intent(text)
        return intent != 'chat'
