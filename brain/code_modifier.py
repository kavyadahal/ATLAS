"""
Code Modifier Module
Handles code modifications: append, replace functions, and insert code.
"""

import os
import re
from typing import Tuple, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class CodeModifier:
    """Handles intelligent code modifications."""
    
    def __init__(self):
        """Initialize the code modifier."""
        self.logger = logging.getLogger(__name__)
        self._brain = None  # Lazy load
    
    def _get_brain(self):
        """Lazy load the AI brain."""
        if self._brain is None:
            from brain.groq_chat import AtlasBrain
            self._brain = AtlasBrain()
        return self._brain
    
    def modify_file(
        self,
        filepath: str,
        modification_type: str,
        user_request: str,
        target_function: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Modify a file based on user request.
        
        Args:
            filepath: Path to the file
            modification_type: Type of modification (append, replace, insert, overwrite)
            user_request: User's request describing what to do
            target_function: Optional function name to replace
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Read the file
            if not os.path.exists(filepath):
                return False, f"File '{filepath}' not found, Sir."
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()
            
            # Determine modification type
            if modification_type == 'overwrite':
                return self._overwrite_file(filepath, user_request)
            elif modification_type == 'append':
                return self._append_to_file(filepath, original_content, user_request)
            elif modification_type == 'replace_function':
                return self._replace_function(filepath, original_content, user_request, target_function)
            elif modification_type == 'insert':
                return self._insert_code(filepath, original_content, user_request)
            else:
                return False, f"Unknown modification type '{modification_type}', Sir."
            
        except Exception as e:
            self.logger.error(f"Error modifying file: {e}")
            return False, f"Error modifying file: {str(e)}, Sir."
    
    def _overwrite_file(self, filepath: str, user_request: str) -> Tuple[bool, str]:
        """
        Overwrite entire file with new generated content.
        
        Args:
            filepath: Path to the file
            user_request: User's request
            
        Returns:
            Tuple of (success, message)
        """
        try:
            filename = os.path.basename(filepath)
            file_ext = os.path.splitext(filename)[1]
            
            # Generate new content
            new_content = self._generate_code(user_request, file_ext, "full_file")
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True, f"Successfully overwrote {filename} with new content, Sir."
            
        except Exception as e:
            return False, f"Error overwriting file: {str(e)}, Sir."
    
    def _append_to_file(self, filepath: str, original_content: str, user_request: str) -> Tuple[bool, str]:
        """
        Append code to the end of a file.
        
        Args:
            filepath: Path to the file
            original_content: Current file content
            user_request: User's request
            
        Returns:
            Tuple of (success, message)
        """
        try:
            filename = os.path.basename(filepath)
            file_ext = os.path.splitext(filename)[1]
            
            # Generate code to append
            new_code = self._generate_code(user_request, file_ext, "append")
            
            # Ensure proper spacing
            if original_content and not original_content.endswith('\n\n'):
                if original_content.endswith('\n'):
                    separator = '\n'
                else:
                    separator = '\n\n'
            else:
                separator = ''
            
            # Combine content
            updated_content = original_content + separator + new_code
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            return True, f"Successfully added code to {filename}, Sir."
            
        except Exception as e:
            return False, f"Error appending to file: {str(e)}, Sir."
    
    def _replace_function(
        self,
        filepath: str,
        original_content: str,
        user_request: str,
        target_function: Optional[str]
    ) -> Tuple[bool, str]:
        """
        Replace a specific function in the file.
        
        Args:
            filepath: Path to the file
            original_content: Current file content
            user_request: User's request
            target_function: Name of function to replace
            
        Returns:
            Tuple of (success, message)
        """
        try:
            filename = os.path.basename(filepath)
            file_ext = os.path.splitext(filename)[1]
            
            # Extract function name if not provided
            if not target_function:
                target_function = self._extract_function_name(user_request)
            
            if not target_function:
                return False, "I couldn't identify which function to replace, Sir. Please specify the function name."
            
            # Find the function in the file
            if file_ext == '.py':
                function_pattern = rf'^(def {re.escape(target_function)}\s*\([^)]*\):.*?)(?=\n(?:def |class |\Z))'
            elif file_ext == '.js':
                function_pattern = rf'(function {re.escape(target_function)}\s*\([^)]*\)\s*\{{.*?\n\}})'
            else:
                return False, f"Function replacement not yet supported for {file_ext} files, Sir."
            
            match = re.search(function_pattern, original_content, re.MULTILINE | re.DOTALL)
            
            if not match:
                return False, f"I couldn't find the function '{target_function}' in {filename}, Sir."
            
            old_function = match.group(1)
            
            # Generate replacement function
            prompt = f"""Generate ONLY the replacement code for the function '{target_function}' based on this request: {user_request}

The function should be in {file_ext} format.
Return ONLY the function code, no explanations, no markdown, just the code."""
            
            new_function = self._generate_code(prompt, file_ext, "function")
            
            # Replace the function
            updated_content = original_content.replace(old_function, new_function.strip())
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            return True, f"Successfully replaced function '{target_function}' in {filename}, Sir."
            
        except Exception as e:
            self.logger.error(f"Error replacing function: {e}")
            return False, f"Error replacing function: {str(e)}, Sir."
    
    def _insert_code(self, filepath: str, original_content: str, user_request: str) -> Tuple[bool, str]:
        """
        Insert code at a specific location (smart positioning).
        
        Args:
            filepath: Path to the file
            original_content: Current file content
            user_request: User's request
            
        Returns:
            Tuple of (success, message)
        """
        try:
            filename = os.path.basename(filepath)
            file_ext = os.path.splitext(filename)[1]
            
            # For now, append with a note about smart insertion
            # This can be enhanced later with line number detection
            new_code = self._generate_code(user_request, file_ext, "insert")
            
            # Smart positioning: insert before last line if it's a main guard
            lines = original_content.split('\n')
            
            if file_ext == '.py' and len(lines) > 2:
                # Check for if __name__ == "__main__"
                for i in range(len(lines) - 1, max(len(lines) - 10, -1), -1):
                    if 'if __name__' in lines[i]:
                        # Insert before this
                        lines.insert(i, '\n' + new_code.strip() + '\n')
                        updated_content = '\n'.join(lines)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                        
                        return True, f"Successfully inserted code into {filename}, Sir."
            
            # Default: append
            return self._append_to_file(filepath, original_content, user_request)
            
        except Exception as e:
            return False, f"Error inserting code: {str(e)}, Sir."
    
    def _extract_function_name(self, user_request: str) -> Optional[str]:
        """
        Extract function name from user request.
        
        Args:
            user_request: User's request text
            
        Returns:
            Function name or None
        """
        # Look for patterns like "replace login()" or "replace the login function"
        patterns = [
            r'replace\s+(?:the\s+)?(\w+)\s*\(\)',
            r'replace\s+(?:the\s+)?(\w+)\s+function',
            r'update\s+(?:the\s+)?(\w+)\s*\(\)',
            r'update\s+(?:the\s+)?(\w+)\s+function',
            r'modify\s+(?:the\s+)?(\w+)\s*\(\)',
            r'modify\s+(?:the\s+)?(\w+)\s+function',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_request, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _generate_code(self, request: str, file_ext: str, context: str) -> str:
        """
        Generate code using AI.
        
        Args:
            request: What to generate
            file_ext: File extension
            context: Context (full_file, append, function, insert)
            
        Returns:
            Generated code
        """
        try:
            # Build prompt based on context
            language = self._get_language_name(file_ext)
            
            if context == "full_file":
                prompt = f"Generate a complete {language} file for: {request}. Return ONLY the code, no explanations."
            elif context == "append":
                prompt = f"Generate {language} code to add to an existing file: {request}. Return ONLY the code to append, no explanations."
            elif context == "function":
                prompt = request  # Already formatted
            else:  # insert
                prompt = f"Generate {language} code for: {request}. Return ONLY the code, no explanations."
            
            # Use AI to generate
            brain = self._get_brain()
            response = brain.chat(prompt)
            
            # Clean the response
            code = self._clean_code_response(response, language)
            
            return code
            
        except Exception as e:
            self.logger.error(f"Error generating code: {e}")
            # Return a comment as fallback
            return f"# TODO: {request}\n"
    
    def _get_language_name(self, file_ext: str) -> str:
        """Get language name from extension."""
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.html': 'HTML',
            '.css': 'CSS',
        }
        return lang_map.get(file_ext, 'code')
    
    def _clean_code_response(self, response: str, language: str) -> str:
        """
        Clean AI response to extract just the code.
        
        Args:
            response: AI response
            language: Programming language
            
        Returns:
            Cleaned code
        """
        # Remove markdown code blocks
        patterns = [
            rf'```{language.lower()}\n(.*?)```',
            r'```\n(.*?)```',
            rf'```{language}\n(.*?)```',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip() + '\n'
        
        # Remove common prefixes
        response = re.sub(r'^(?:Here\'s|Here is).*?:\s*', '', response, flags=re.IGNORECASE)
        response = re.sub(r'^(?:Sure|Certainly).*?:\s*', '', response, flags=re.IGNORECASE)
        
        # If no code blocks found, return as is
        return response.strip() + '\n'
