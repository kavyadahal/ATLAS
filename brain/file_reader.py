"""
File Reader Module
Reads and analyzes code files to provide explanations.
"""

import os
import re
from typing import Tuple, Optional, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class FileReader:
    """Reads and analyzes files for explanation and understanding."""
    
    def __init__(self):
        """Initialize the file reader."""
        self.logger = logging.getLogger(__name__)
        self._brain = None  # Lazy load
    
    def _get_brain(self):
        """Lazy load the AI brain."""
        if self._brain is None:
            from brain.groq_chat import AtlasBrain
            self._brain = AtlasBrain()
        return self._brain
    
    def read_file(self, filepath: str) -> Tuple[bool, str, Optional[str]]:
        """
        Read a file and return its contents.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Tuple of (success, message, content)
        """
        try:
            if not os.path.exists(filepath):
                return False, f"File '{filepath}' not found, Sir.", None
            
            if not os.path.isfile(filepath):
                return False, f"'{filepath}' is not a file, Sir.", None
            
            # Check file size
            file_size = os.path.getsize(filepath)
            if file_size > 1024 * 1024:  # 1MB limit
                return False, f"File '{filepath}' is too large to read (>1MB), Sir.", None
            
            # Read the file
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return True, "File read successfully, Sir.", content
            
        except UnicodeDecodeError:
            return False, f"Unable to read '{filepath}' - it appears to be a binary file, Sir.", None
        except PermissionError:
            return False, f"Permission denied reading '{filepath}', Sir.", None
        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            return False, f"Error reading file: {str(e)}, Sir.", None
    
    def explain_file(self, filepath: str) -> Tuple[bool, str]:
        """
        Read and explain a file using AI.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Tuple of (success, explanation)
        """
        try:
            # Read the file
            success, message, content = self.read_file(filepath)
            
            if not success:
                return False, message
            
            # Get file info
            filename = os.path.basename(filepath)
            file_ext = os.path.splitext(filename)[1]
            
            # Analyze the file
            analysis = self._analyze_file_structure(content, file_ext)
            
            # Generate explanation using AI
            explanation = self._generate_explanation(filename, content, analysis, file_ext)
            
            return True, explanation
            
        except Exception as e:
            self.logger.error(f"Error explaining file: {e}")
            return False, f"Error explaining file: {str(e)}, Sir."
    
    def _analyze_file_structure(self, content: str, file_ext: str) -> Dict[str, Any]:
        """
        Analyze file structure to extract key information.
        
        Args:
            content: File content
            file_ext: File extension
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            'lines': len(content.split('\n')),
            'size': len(content),
            'language': self._detect_language(file_ext)
        }
        
        if file_ext == '.py':
            analysis.update(self._analyze_python(content))
        elif file_ext == '.js':
            analysis.update(self._analyze_javascript(content))
        
        return analysis
    
    def _detect_language(self, file_ext: str) -> str:
        """Detect programming language from extension."""
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.xml': 'XML',
            '.md': 'Markdown',
            '.txt': 'Text',
            '.yaml': 'YAML',
            '.yml': 'YAML',
        }
        return lang_map.get(file_ext, 'Unknown')
    
    def _analyze_python(self, content: str) -> Dict[str, Any]:
        """Analyze Python code structure."""
        analysis = {}
        
        # Find imports
        imports = re.findall(r'^(?:import|from)\s+(\S+)', content, re.MULTILINE)
        analysis['imports'] = imports[:10]  # First 10
        
        # Find functions
        functions = re.findall(r'^def\s+(\w+)\s*\(', content, re.MULTILINE)
        analysis['functions'] = functions
        
        # Find classes
        classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
        analysis['classes'] = classes
        
        return analysis
    
    def _analyze_javascript(self, content: str) -> Dict[str, Any]:
        """Analyze JavaScript code structure."""
        analysis = {}
        
        # Find functions
        functions = re.findall(r'function\s+(\w+)\s*\(', content)
        analysis['functions'] = functions
        
        # Find arrow functions
        arrow_funcs = re.findall(r'const\s+(\w+)\s*=\s*\(.*?\)\s*=>', content)
        analysis['arrow_functions'] = arrow_funcs
        
        # Find classes
        classes = re.findall(r'class\s+(\w+)', content)
        analysis['classes'] = classes
        
        return analysis
    
    def _generate_explanation(
        self,
        filename: str,
        content: str,
        analysis: Dict[str, Any],
        file_ext: str
    ) -> str:
        """
        Generate AI explanation of the file.
        
        Args:
            filename: Name of the file
            content: File content
            analysis: Structural analysis
            file_ext: File extension
            
        Returns:
            Explanation text
        """
        # Build context for AI
        context = f"File: {filename}\n"
        context += f"Type: {analysis.get('language', 'Unknown')}\n"
        context += f"Lines: {analysis.get('lines', 0)}\n"
        
        if 'functions' in analysis and analysis['functions']:
            context += f"Functions: {', '.join(analysis['functions'][:5])}\n"
        
        if 'classes' in analysis and analysis['classes']:
            context += f"Classes: {', '.join(analysis['classes'][:5])}\n"
        
        if 'imports' in analysis and analysis['imports']:
            context += f"Key imports: {', '.join(analysis['imports'][:5])}\n"
        
        # Truncate content if too long
        max_content_length = 3000
        if len(content) > max_content_length:
            content_preview = content[:max_content_length] + "\n... (truncated)"
        else:
            content_preview = content
        
        # Create prompt for AI
        prompt = f"""Explain this code file to the user. Be concise but thorough.

{context}

Content:
```
{content_preview}
```

Provide:
1. Overall purpose and architecture
2. Key components (classes, functions, modules)
3. Main functionality
4. Important patterns or design decisions

Keep it professional and informative."""
        
        try:
            brain = self._get_brain()
            explanation = brain.chat(prompt)
            return explanation
        except Exception as e:
            self.logger.error(f"Error generating explanation: {e}")
            
            # Fallback to structural explanation
            fallback = f"File: {filename}\n\n"
            fallback += f"This is a {analysis.get('language', 'code')} file with {analysis.get('lines', 0)} lines.\n\n"
            
            if 'classes' in analysis and analysis['classes']:
                fallback += f"Classes: {', '.join(analysis['classes'])}\n"
            
            if 'functions' in analysis and analysis['functions']:
                fallback += f"Functions: {', '.join(analysis['functions'][:10])}\n"
            
            fallback += "\nI encountered an issue generating a detailed explanation, Sir."
            return fallback
