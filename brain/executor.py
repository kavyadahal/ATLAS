"""
Command Executor Module
Executes detected commands using existing automation modules.
"""

from typing import Tuple, Dict, Any
from pathlib import Path
import os


class CommandExecutor:
    """Executes commands based on detected intent."""
    
    def __init__(self):
        """Initialize the command executor with automation modules."""
        from automation.desktop_controller import DesktopController
        from automation.file_manager import FileManager
        
        self.desktop = DesktopController()
        self.files = FileManager()
    
    def execute(self, intent: str, params: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute a command based on intent and parameters.
        
        Args:
            intent: The detected intent name
            params: Dictionary of parameters for the command
            
        Returns:
            Tuple of (success, message)
        """
        # Route to appropriate handler
        handler = getattr(self, f'_handle_{intent}', None)
        
        if handler:
            try:
                return handler(params)
            except Exception as e:
                return False, f"Error executing command: {str(e)}, Sir."
        else:
            return False, f"I don't know how to handle '{intent}' yet, Sir."
    
    # File Operations
    
    def _handle_create_file(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle file creation."""
        filename = params.get('filename', 'newfile.txt')
        location = params.get('location', 'desktop')
        
        # Map location keywords to actual paths
        location_map = {
            'desktop': str(Path.home() / 'Desktop'),
            'downloads': str(Path.home() / 'Downloads'),
            'documents': str(Path.home() / 'Documents'),
        }
        
        # Get base path
        base_path = location_map.get(location.lower(), location_map['desktop'])
        file_path = os.path.join(base_path, filename)
        
        # Create the file
        success, message = self.files.create_file(file_path)
        
        if success:
            return True, f"Created {filename} on {location}, Sir."
        else:
            return False, message
    
    def _handle_create_folder(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle folder creation."""
        folder_name = params.get('folder_name', 'NewFolder')
        location = params.get('location', 'desktop')
        
        # Map location keywords
        location_map = {
            'desktop': str(Path.home() / 'Desktop'),
            'downloads': str(Path.home() / 'Downloads'),
            'documents': str(Path.home() / 'Documents'),
        }
        
        base_path = location_map.get(location.lower(), location_map['desktop'])
        folder_path = os.path.join(base_path, folder_name)
        
        return self.files.create_folder(folder_path)
    
    def _handle_delete_file(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle file deletion - requires confirmation."""
        query = params.get('query', '')
        filename = params.get('filename', query)
        
        # Search for the file first
        results = self.files.search_files(filename, limit=1)
        
        if not results:
            return False, f"I couldn't find a file matching '{filename}', Sir."
        
        file_path = results[0]['path']
        file_name = results[0]['name']
        
        # Check if this is a confirmed deletion (has 'confirmed' flag)
        if params.get('confirmed'):
            # Actually delete the file
            try:
                import os
                os.remove(file_path)
                return True, f"Deleted '{file_name}', Sir."
            except Exception as e:
                return False, f"Error deleting file: {str(e)}, Sir."
        else:
            # Return special tuple indicating confirmation needed
            # Format: (None, message, 'needs_confirmation')
            return (None, f"Found '{file_name}' at {file_path}. Please confirm deletion, Sir.", 'needs_confirmation')
    
    def _handle_search_files(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle file search."""
        query = params.get('query', '')
        
        results = self.files.search_files(query, limit=5)
        
        if results:
            response = f"I found {len(results)} file(s), Sir:\n"
            for i, file in enumerate(results, 1):
                response += f"{i}. {file['name']} ({file['path']})\n"
            return True, response.strip()
        else:
            return False, f"I couldn't find any files matching '{query}', Sir."
    
    def _handle_open_file(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle opening a file."""
        filename = params.get('filename', '')
        
        # Check if file exists in current directory
        if os.path.exists(filename):
            file_path = os.path.abspath(filename)
        else:
            # Search for the file
            results = self.files.search_files(filename, limit=1)
            if results:
                file_path = results[0]['path']
            else:
                return False, f"I couldn't find '{filename}', Sir."
        
        # Open file with default application
        try:
            import subprocess
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            else:  # macOS/Linux
                subprocess.run(['xdg-open', file_path])
            return True, f"Opening {filename}, Sir."
        except Exception as e:
            return False, f"Error opening file: {str(e)}, Sir."
    
    def _handle_read_file(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle reading a file."""
        filename = params.get('filename', '')
        
        # Check if file exists in current directory
        if os.path.exists(filename):
            file_path = os.path.abspath(filename)
        else:
            # Search for the file
            results = self.files.search_files(filename, limit=1)
            if results:
                file_path = results[0]['path']
            else:
                return False, f"I couldn't find '{filename}', Sir."
        
        # Read file contents
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Limit output for very large files
            if len(content) > 1000:
                content = content[:1000] + "\n...(file truncated)"
            
            return True, f"Contents of {filename}:\n\n{content}"
        except Exception as e:
            return False, f"Error reading file: {str(e)}, Sir."
    
    def _handle_edit_file(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle editing a file."""
        filename = params.get('filename', '')
        
        # Check if file exists in current directory
        if os.path.exists(filename):
            file_path = os.path.abspath(filename)
        else:
            # Search for the file
            results = self.files.search_files(filename, limit=1)
            if results:
                file_path = results[0]['path']
            else:
                return False, f"I couldn't find '{filename}', Sir."
        
        # Open in VS Code or default editor
        try:
            import subprocess
            # Try VS Code first
            try:
                subprocess.run(['code', file_path], check=True)
                return True, f"Opening {filename} in VS Code, Sir."
            except:
                # Fallback to default editor
                if os.name == 'nt':  # Windows
                    os.startfile(file_path)
                else:  # macOS/Linux
                    subprocess.run(['xdg-open', file_path])
                return True, f"Opening {filename} in default editor, Sir."
        except Exception as e:
            return False, f"Error opening file for editing: {str(e)}, Sir."
    
    # Application Control
    
    def _handle_open_app(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle opening an application."""
        app_name = params.get('app_name', '')
        return self.desktop.open_application(app_name)
    
    def _handle_close_app(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle closing an application."""
        app_name = params.get('app_name', '')
        return self.desktop.close_application(app_name)
    
    def _handle_open_website(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle opening a website."""
        url = params.get('url', '')
        return self.desktop.open_website(url)
    
    def _handle_open_folder(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle opening a system folder."""
        folder = params.get('folder', 'desktop')
        return self.desktop.open_folder(folder)
    
    # System Operations
    
    def _handle_list_apps(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle listing running applications."""
        apps = self.desktop.list_running_applications()
        
        if apps:
            displayed_apps = apps[:15]
            app_list = ', '.join(displayed_apps)
            if len(apps) > 15:
                return True, f"Currently running applications: {app_list}, and {len(apps) - 15} more, Sir."
            return True, f"Currently running applications: {app_list}, Sir."
        
        return True, "No applications are currently running, Sir."
    
    def _handle_organize_downloads(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle organizing the Downloads folder."""
        return self.files.organize_downloads()
    
    def _handle_run_python(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle running a Python file."""
        filename = params.get('filename', '')
        
        if not os.path.exists(filename):
            # Try searching for it
            results = self.files.search_files(filename, limit=1)
            if results:
                filename = results[0]['path']
            else:
                return False, f"I couldn't find '{filename}', Sir."
        
        try:
            import subprocess
            result = subprocess.run(
                ['python', filename],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    return True, f"Executed successfully, Sir. Output:\n{output}"
                else:
                    return True, "Executed successfully, Sir."
            else:
                error = result.stderr.strip()
                return False, f"Execution failed, Sir. Error:\n{error}"
                
        except subprocess.TimeoutExpired:
            return False, "The script took too long to execute, Sir."
        except Exception as e:
            return False, f"Error running Python file: {str(e)}, Sir."
