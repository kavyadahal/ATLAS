"""
File Agent Module
Orchestrates file operations: reading, explaining, and modifying code files.
"""

import os
from typing import Tuple, Optional
from pathlib import Path
import logging

from brain.file_reader import FileReader
from brain.code_modifier import CodeModifier

logger = logging.getLogger(__name__)


class FileAgent:
    """
    AI File Agent that can read, understand, explain, and modify code files.
    """
    
    def __init__(self):
        """Initialize the file agent with reader and modifier."""
        self.reader = FileReader()
        self.modifier = CodeModifier()
        self.logger = logging.getLogger(__name__)
    
    def explain_file(self, filename: str) -> Tuple[bool, str]:
        """
        Read and explain a file to the user.
        
        Args:
            filename: Name or path of the file
            
        Returns:
            Tuple of (success, explanation)
        """
        try:
            # Resolve file path
            filepath = self._resolve_file_path(filename)
            
            if not filepath:
                return False, f"I couldn't find the file '{filename}', Sir."
            
            # Use reader to explain
            return self.reader.explain_file(filepath)
            
        except Exception as e:
            self.logger.error(f"Error in explain_file: {e}")
            return False, f"Error explaining file: {str(e)}, Sir."
    
    def modify_code(
        self,
        filename: str,
        user_request: str,
        operation: str = 'auto'
    ) -> Tuple[bool, str]:
        """
        Modify code in a file based on user request.
        
        Args:
            filename: Name or path of the file
            user_request: User's request describing the modification
            operation: Type of operation (auto, append, replace, insert, overwrite)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Resolve file path
            filepath = self._resolve_file_path(filename)
            
            if not filepath:
                return False, f"I couldn't find the file '{filename}', Sir."
            
            # Determine operation type if auto
            if operation == 'auto':
                operation = self._detect_operation(user_request)
            
            # Extract target function name if it's a replace operation
            target_function = None
            if operation == 'replace_function':
                target_function = self.modifier._extract_function_name(user_request)
            
            # Use modifier to update the file
            return self.modifier.modify_file(
                filepath=filepath,
                modification_type=operation,
                user_request=user_request,
                target_function=target_function
            )
            
        except Exception as e:
            self.logger.error(f"Error in modify_code: {e}")
            return False, f"Error modifying code: {str(e)}, Sir."
    
    def _resolve_file_path(self, filename: str) -> Optional[str]:
        """
        Resolve a filename to a full path.
        
        Args:
            filename: Name or partial path of the file
            
        Returns:
            Full path to the file or None if not found
        """
        # Check if it's already a valid path
        if os.path.exists(filename):
            return os.path.abspath(filename)
        
        # Check in current working directory
        current_dir = os.getcwd()
        candidate = os.path.join(current_dir, filename)
        if os.path.exists(candidate):
            return candidate
        
        # Search in common project locations
        search_paths = [
            current_dir,
            os.path.join(current_dir, 'brain'),
            os.path.join(current_dir, 'core'),
            os.path.join(current_dir, 'automation'),
            os.path.join(current_dir, 'commands'),
            os.path.join(current_dir, 'voice'),
            os.path.join(current_dir, 'ui'),
            os.path.join(current_dir, 'memory'),
        ]
        
        for search_path in search_paths:
            if os.path.exists(search_path):
                candidate = os.path.join(search_path, filename)
                if os.path.exists(candidate):
                    return candidate
        
        # Try recursive search in current directory (limited depth)
        try:
            for root, dirs, files in os.walk(current_dir):
                # Skip hidden and common non-code directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', 'env', '__pycache__', 'node_modules']]
                
                if filename in files:
                    return os.path.join(root, filename)
                
                # Limit depth
                if root.count(os.sep) - current_dir.count(os.sep) > 3:
                    break
        except Exception as e:
            self.logger.error(f"Error searching for file: {e}")
        
        return None
    
    def _detect_operation(self, user_request: str) -> str:
        """
        Detect the type of operation from user request.
        
        Args:
            user_request: User's request text
            
        Returns:
            Operation type (append, replace_function, insert, overwrite)
        """
        request_lower = user_request.lower()
        
        # Check for replace function
        if any(keyword in request_lower for keyword in ['replace', 'update function', 'modify function']):
            if 'function' in request_lower or '()' in user_request:
                return 'replace_function'
        
        # Check for overwrite (rewrite entire file)
        if any(keyword in request_lower for keyword in ['rewrite', 'overwrite', 'completely rewrite']):
            return 'overwrite'
        
        # Check for insert
        if any(keyword in request_lower for keyword in ['insert', 'add before', 'add after']):
            return 'insert'
        
        # Default: append
        return 'append'
