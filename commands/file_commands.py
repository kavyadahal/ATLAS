"""
File Commands Module
Implements file operation commands.
"""

from typing import Dict, Any, Tuple
from pathlib import Path
import os


def register_file_commands(registry, file_manager, file_writer):
    """
    Register all file-related commands.
    
    Args:
        registry: CommandRegistry instance
        file_manager: FileManager instance
        file_writer: FileWriter instance
    """
    
    @registry.register('create_file_with_content')
    def create_file_with_content(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle smart file creation with AI-generated content."""
        filename = params.get('filename', 'newfile.txt')
        location = params.get('location', 'desktop')
        user_request = params.get('original_text', '')
        
        return file_writer.create_file_with_content(
            filename=filename,
            location=location,
            user_request=user_request,
            content=None
        )
    
    @registry.register('create_file')
    def create_file(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle basic file creation."""
        filename = params.get('filename', 'newfile.txt')
        location = params.get('location', 'desktop')
        user_request = params.get('original_text', '')
        
        file_ext = os.path.splitext(filename)[1].lower()
        
        # For code files, generate content
        if file_ext in ['.py', '.js', '.html', '.css', '.json', '.md']:
            return file_writer.create_file_with_content(
                filename=filename,
                location=location,
                user_request=user_request,
                content=None
            )
        
        # For other files, create empty
        location_map = {
            'desktop': str(Path.home() / 'Desktop'),
            'downloads': str(Path.home() / 'Downloads'),
            'documents': str(Path.home() / 'Documents'),
        }
        
        base_path = location_map.get(location.lower(), location_map['desktop'])
        file_path = os.path.join(base_path, filename)
        
        success, message = file_manager.create_file(file_path)
        
        if success:
            return True, f"Created {filename} on {location}, Sir."
        else:
            return False, message
    
    @registry.register('create_folder')
    def create_folder(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle folder creation."""
        folder_name = params.get('folder_name', 'NewFolder')
        location = params.get('location', 'desktop')
        
        location_map = {
            'desktop': str(Path.home() / 'Desktop'),
            'downloads': str(Path.home() / 'Downloads'),
            'documents': str(Path.home() / 'Documents'),
        }
        
        base_path = location_map.get(location.lower(), location_map['desktop'])
        folder_path = os.path.join(base_path, folder_name)
        
        return file_manager.create_folder(folder_path)
    
    @registry.register('delete_file')
    def delete_file(params: Dict[str, Any]) -> Tuple[bool, str] | Tuple[None, str, str]:
        """Handle file deletion - requires confirmation."""
        query = params.get('query', '')
        filename = params.get('filename', query)
        
        # Search for the file first
        results = file_manager.search_files(filename, limit=1)
        
        if not results:
            return False, f"I couldn't find a file matching '{filename}', Sir."
        
        file_path = results[0]['path']
        file_name = results[0]['name']
        
        # Check if this is a confirmed deletion
        if params.get('confirmed'):
            try:
                os.remove(file_path)
                return True, f"Deleted '{file_name}', Sir."
            except Exception as e:
                return False, f"Error deleting file: {str(e)}, Sir."
        else:
            # Return confirmation needed
            return (None, f"Found '{file_name}' at {file_path}. Please confirm deletion, Sir.", 'needs_confirmation')
    
    @registry.register('search_files')
    def search_files(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle file search."""
        query = params.get('query', '')
        
        results = file_manager.search_files(query, limit=5)
        
        if results:
            response = f"I found {len(results)} file(s), Sir:\n"
            for i, file in enumerate(results, 1):
                response += f"{i}. {file['name']} ({file['path']})\n"
            return True, response.strip()
        else:
            return False, f"I couldn't find any files matching '{query}', Sir."
    
    @registry.register('open_file')
    def open_file(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle opening a file."""
        filename = params.get('filename', '')
        
        if os.path.exists(filename):
            file_path = os.path.abspath(filename)
        else:
            results = file_manager.search_files(filename, limit=1)
            if results:
                file_path = results[0]['path']
            else:
                return False, f"I couldn't find '{filename}', Sir."
        
        try:
            import subprocess
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            else:  # macOS/Linux
                subprocess.run(['xdg-open', file_path])
            return True, f"Opening {filename}, Sir."
        except Exception as e:
            return False, f"Error opening file: {str(e)}, Sir."
    
    @registry.register('read_file')
    def read_file(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle reading a file."""
        filename = params.get('filename', '')
        
        if os.path.exists(filename):
            file_path = os.path.abspath(filename)
        else:
            results = file_manager.search_files(filename, limit=1)
            if results:
                file_path = results[0]['path']
            else:
                return False, f"I couldn't find '{filename}', Sir."
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) > 1000:
                content = content[:1000] + "\n...(file truncated)"
            
            return True, f"Contents of {filename}:\n\n{content}"
        except Exception as e:
            return False, f"Error reading file: {str(e)}, Sir."
    
    @registry.register('edit_file')
    def edit_file(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle editing a file."""
        filename = params.get('filename', '')
        
        if os.path.exists(filename):
            file_path = os.path.abspath(filename)
        else:
            results = file_manager.search_files(filename, limit=1)
            if results:
                file_path = results[0]['path']
            else:
                return False, f"I couldn't find '{filename}', Sir."
        
        try:
            import subprocess
            try:
                subprocess.run(['code', file_path], check=True)
                return True, f"Opening {filename} in VS Code, Sir."
            except:
                if os.name == 'nt':
                    os.startfile(file_path)
                else:
                    subprocess.run(['xdg-open', file_path])
                return True, f"Opening {filename} in default editor, Sir."
        except Exception as e:
            return False, f"Error opening file for editing: {str(e)}, Sir."
