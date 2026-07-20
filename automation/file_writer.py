"""
File Writer Module - Smart File Creation with AI Content Generation
Creates files with intelligent content based on user requests.
"""

import os
import re
import json
from typing import Tuple, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class FileWriter:
    """
    Handles smart file creation with AI-generated content.
    Supports multiple file types with appropriate formatting.
    """
    
    # Supported file extensions (PART 2)
    SUPPORTED_EXTENSIONS = {
        '.py', '.txt', '.md', '.json', '.yaml', '.yml', 
        '.csv', '.html', '.css', '.js', '.xml', '.ini', '.toml'
    }
    
    # File type templates and patterns
    FILE_TYPE_INFO = {
        '.py': {'name': 'Python', 'comment': '#', 'needs_content': True},
        '.txt': {'name': 'Text', 'comment': None, 'needs_content': False},
        '.md': {'name': 'Markdown', 'comment': None, 'needs_content': True},
        '.json': {'name': 'JSON', 'comment': None, 'needs_content': True},
        '.yaml': {'name': 'YAML', 'comment': '#', 'needs_content': True},
        '.yml': {'name': 'YAML', 'comment': '#', 'needs_content': True},
        '.csv': {'name': 'CSV', 'comment': None, 'needs_content': True},
        '.html': {'name': 'HTML', 'comment': '<!--', 'needs_content': True},
        '.css': {'name': 'CSS', 'comment': '/*', 'needs_content': True},
        '.js': {'name': 'JavaScript', 'comment': '//', 'needs_content': True},
        '.xml': {'name': 'XML', 'comment': '<!--', 'needs_content': True},
        '.ini': {'name': 'INI', 'comment': ';', 'needs_content': True},
        '.toml': {'name': 'TOML', 'comment': '#', 'needs_content': True},
    }
    
    def __init__(self):
        """Initialize the FileWriter with AI brain for content generation."""
        self.logger = logging.getLogger(__name__)
        self._brain = None  # Lazy load to avoid circular imports
    
    def _get_brain(self):
        """Lazy load the AI brain for content generation."""
        if self._brain is None:
            from brain.groq_chat import AtlasBrain
            self._brain = AtlasBrain()
        return self._brain
    
    def create_file_with_content(
        self,
        filename: str,
        location: str,
        user_request: str,
        content: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Create a file with smart content generation.
        
        Args:
            filename: Name of the file to create
            location: Location to create the file (desktop, downloads, documents)
            user_request: Original user request for context
            content: Optional explicit content (if None, will be generated)
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # PART 4: Validate filename
            if not self._is_valid_filename(filename):
                return False, f"Invalid filename '{filename}', Sir. Please use only letters, numbers, underscores, hyphens, and dots."
            
            # Get file extension
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Check if extension is supported
            if file_ext not in self.SUPPORTED_EXTENSIONS:
                return False, f"I don't support '{file_ext}' files yet, Sir. Supported types: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}"
            
            # Map location to actual path
            location_map = {
                'desktop': str(Path.home() / 'Desktop'),
                'downloads': str(Path.home() / 'Downloads'),
                'documents': str(Path.home() / 'Documents'),
            }
            
            base_path = location_map.get(location.lower(), location_map['desktop'])
            file_path = os.path.join(base_path, filename)
            
            # PART 4: Check if file exists (don't overwrite without confirmation)
            if os.path.exists(file_path):
                return False, f"A file named '{filename}' already exists at {location}, Sir. Please choose a different name or delete the existing file first."
            
            # PART 4: Create parent directories if needed
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Generate or use provided content
            if content is None:
                content = self._generate_content(filename, file_ext, user_request)
            
            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Created file with content: {file_path}")
            return True, f"Created {filename} on {location} with generated content, Sir."
            
        except PermissionError:
            return False, f"I don't have permission to create files at that location, Sir."
        except Exception as e:
            self.logger.error(f"Error creating file: {e}")
            return False, f"Error creating file: {str(e)}, Sir."
    
    def _is_valid_filename(self, filename: str) -> bool:
        """
        PART 4: Validate filename for safety.
        
        Args:
            filename: The filename to validate
        
        Returns:
            True if filename is valid
        """
        # Check for invalid characters
        invalid_chars = '<>:"|?*\\/\0'
        if any(char in filename for char in invalid_chars):
            return False
        
        # Check for reserved names on Windows
        reserved_names = {
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        }
        name_without_ext = os.path.splitext(filename)[0].upper()
        if name_without_ext in reserved_names:
            return False
        
        # Check length
        if len(filename) > 255:
            return False
        
        return True
    
    def _generate_content(self, filename: str, file_ext: str, user_request: str) -> str:
        """
        Generate appropriate content for the file based on type and user request.
        
        Args:
            filename: Name of the file
            file_ext: File extension
            user_request: Original user request for context
        
        Returns:
            Generated content as string
        """
        file_info = self.FILE_TYPE_INFO.get(file_ext, {})
        file_type = file_info.get('name', 'file')
        
        # Parse the user request to understand what content is needed
        content_intent = self._parse_content_intent(user_request, filename, file_ext)
        
        if content_intent['has_explicit_content']:
            # User specified exact content
            return content_intent['content']
        
        # Generate content using AI
        if file_ext == '.py':
            return self._generate_python_content(filename, user_request)
        elif file_ext == '.json':
            return self._generate_json_content(filename, user_request)
        elif file_ext == '.md':
            return self._generate_markdown_content(filename, user_request)
        elif file_ext == '.html':
            return self._generate_html_content(filename, user_request)
        elif file_ext == '.css':
            return self._generate_css_content(filename, user_request)
        elif file_ext == '.js':
            return self._generate_javascript_content(filename, user_request)
        elif file_ext in ['.yaml', '.yml']:
            return self._generate_yaml_content(filename, user_request)
        elif file_ext == '.csv':
            return self._generate_csv_content(filename, user_request)
        elif file_ext == '.txt':
            return self._generate_text_content(filename, user_request)
        else:
            # Generic content
            return f"# {filename}\n# Created by ATLAS\n"
    
    def _parse_content_intent(self, user_request: str, filename: str, file_ext: str) -> Dict[str, Any]:
        """
        Parse user request to extract explicit content if provided.
        
        Example: "Create notes.txt. Write: Buy milk, Call John"
        """
        result = {'has_explicit_content': False, 'content': ''}
        
        # Look for explicit content patterns
        patterns = [
            r'write[:\s]+(.+)',
            r'containing[:\s]+(.+)',
            r'with[:\s]+(.+)',
            r'that says[:\s]+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_request, re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                # Clean up the content
                content = content.replace('\\n', '\n')
                result['has_explicit_content'] = True
                result['content'] = content
                break
        
        return result
    
    def _generate_python_content(self, filename: str, user_request: str) -> str:
        """Generate Python file content using AI."""
        # Check for specific patterns
        if 'hello world' in user_request.lower():
            return 'print("Hello, World!")\n'
        elif 'calculator' in user_request.lower():
            return self._get_calculator_template()
        
        # Use AI to generate
        prompt = f"Generate a complete, working Python script for: {user_request}. Only return the Python code, no explanations."
        
        try:
            brain = self._get_brain()
            code = brain.chat(prompt)
            
            # Clean up the response (remove markdown code blocks if present)
            code = self._clean_code_response(code, 'python')
            
            return code
        except Exception as e:
            self.logger.error(f"Error generating Python content: {e}")
            return f'# {filename}\n# TODO: Implement functionality\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()\n'
    
    def _generate_json_content(self, filename: str, user_request: str) -> str:
        """Generate JSON content."""
        if 'config' in filename.lower() or 'config' in user_request.lower():
            return json.dumps({
                "name": "ATLAS",
                "version": "1.0.0",
                "description": "Configuration file"
            }, indent=2)
        
        # Generic JSON
        return json.dumps({"data": []}, indent=2)
    
    def _generate_markdown_content(self, filename: str, user_request: str) -> str:
        """Generate Markdown content using AI."""
        if 'readme' in filename.lower():
            project_name = os.path.splitext(filename)[0].upper()
            return f"# {project_name}\n\n## Description\n\nProject description here.\n\n## Usage\n\nUsage instructions here.\n"
        
        # Use AI
        prompt = f"Generate markdown content for: {user_request}. Return only the markdown, no explanations."
        
        try:
            brain = self._get_brain()
            content = brain.chat(prompt)
            return content
        except Exception:
            return f"# {os.path.splitext(filename)[0]}\n\nContent here.\n"
    
    def _generate_html_content(self, filename: str, user_request: str) -> str:
        """Generate HTML content."""
        title = os.path.splitext(filename)[0].replace('_', ' ').title()
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <p>Content created by ATLAS</p>
</body>
</html>
"""
    
    def _generate_css_content(self, filename: str, user_request: str) -> str:
        """Generate CSS content."""
        return """/* CSS Stylesheet */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
}
"""
    
    def _generate_javascript_content(self, filename: str, user_request: str) -> str:
        """Generate JavaScript content."""
        return """// JavaScript File

function main() {
    console.log('Hello from ATLAS');
}

main();
"""
    
    def _generate_yaml_content(self, filename: str, user_request: str) -> str:
        """Generate YAML content."""
        return """# YAML Configuration
name: ATLAS
version: 1.0.0
settings:
  enabled: true
"""
    
    def _generate_csv_content(self, filename: str, user_request: str) -> str:
        """Generate CSV content."""
        return "Name,Value,Date\nExample,123,2026-01-01\n"
    
    def _generate_text_content(self, filename: str, user_request: str) -> str:
        """Generate plain text content."""
        # For notes, use AI to help
        if 'note' in filename.lower() or 'note' in user_request.lower():
            return "Notes:\n\n- \n"
        
        return f"{os.path.splitext(filename)[0]}\n\nCreated by ATLAS\n"
    
    def _get_calculator_template(self) -> str:
        """Get calculator Python template."""
        return """def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

def main():
    print("Simple Calculator")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    
    choice = input("Enter choice (1-4): ")
    
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    
    if choice == '1':
        print(f"Result: {add(num1, num2)}")
    elif choice == '2':
        print(f"Result: {subtract(num1, num2)}")
    elif choice == '3':
        print(f"Result: {multiply(num1, num2)}")
    elif choice == '4':
        print(f"Result: {divide(num1, num2)}")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
"""
    
    def _clean_code_response(self, response: str, language: str) -> str:
        """
        Clean AI response to extract just the code.
        Removes markdown code blocks and explanations.
        """
        # Remove markdown code blocks
        patterns = [
            rf'```{language}\n(.*?)```',
            r'```\n(.*?)```',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                return match.group(1).strip() + '\n'
        
        # If no code blocks found, return as is
        return response.strip() + '\n'
