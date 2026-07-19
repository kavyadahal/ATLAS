"""
Command Router Module
Routes user commands to appropriate automation modules and handles confirmations.
"""

import re
from typing import Tuple, Optional, Dict, Any
import logging
from .desktop_controller import DesktopController
from .file_manager import FileManager

logger = logging.getLogger(__name__)


class CommandRouter:
    """Routes natural language commands to appropriate automation modules."""
    
    def __init__(self):
        """Initialize the CommandRouter with automation modules."""
        self.desktop = DesktopController()
        self.files = FileManager()
        self.logger = logging.getLogger(__name__)
        self.pending_confirmation = None
    
    def route_command(self, message: str) -> Tuple[bool, Optional[str]]:
        """
        Route a user command to the appropriate handler.
        
        Args:
            message: User's message/command
            
        Returns:
            Tuple of (handled, response) where handled is True if command was processed
        """
        message_lower = message.lower()
        
        # Desktop Control Commands
        if self._is_open_app_command(message_lower):
            return True, self._handle_open_app(message_lower)
        
        if self._is_close_app_command(message_lower):
            return True, self._handle_close_app(message_lower)
        
        if self._is_open_website_command(message_lower):
            return True, self._handle_open_website(message_lower)
        
        if self._is_open_folder_command(message_lower):
            return True, self._handle_open_folder(message_lower)
        
        if self._is_list_apps_command(message_lower):
            return True, self._handle_list_apps()
        
        if self._is_minimize_command(message_lower):
            return True, self._handle_minimize(message_lower)
        
        if self._is_maximize_command(message_lower):
            return True, self._handle_maximize(message_lower)
        
        if self._is_focus_command(message_lower):
            return True, self._handle_focus(message_lower)
        
        # File Management Commands
        if self._is_search_files_command(message_lower):
            return True, self._handle_search_files(message_lower)
        
        if self._is_rename_file_command(message_lower):
            return True, self._handle_rename_file(message)
        
        if self._is_move_file_command(message_lower):
            return True, self._handle_move_file(message)
        
        if self._is_copy_file_command(message_lower):
            return True, self._handle_copy_file(message)
        
        if self._is_delete_file_command(message_lower):
            return True, self._handle_delete_file(message)
        
        if self._is_create_folder_command(message_lower):
            return True, self._handle_create_folder(message)
        
        if self._is_compress_command(message_lower):
            return True, self._handle_compress(message)
        
        if self._is_extract_command(message_lower):
            return True, self._handle_extract(message)
        
        if self._is_organize_downloads_command(message_lower):
            return True, self._handle_organize_downloads()
        
        if self._is_recent_files_command(message_lower):
            return True, self._handle_recent_files(message_lower)
        
        # Not a system command
        return False, None
    
    # ==================== Desktop Control Handlers ====================
    
    def _is_open_app_command(self, message: str) -> bool:
        """Check if message is an open application command."""
        patterns = [
            r'\bopen\s+(\w+)',
            r'\blaunch\s+(\w+)',
            r'\bstart\s+(\w+)',
            r'\brun\s+(\w+)',
        ]
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _handle_open_app(self, message: str) -> str:
        """Handle opening an application."""
        # Extract app name
        patterns = [
            r'\bopen\s+(\w+(?:\s+\w+)?)',
            r'\blaunch\s+(\w+(?:\s+\w+)?)',
            r'\bstart\s+(\w+(?:\s+\w+)?)',
            r'\brun\s+(\w+(?:\s+\w+)?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                app_name = match.group(1).strip()
                success, msg = self.desktop.open_application(app_name)
                return msg
        
        return "I couldn't understand which application to open, Sir."
    
    def _is_close_app_command(self, message: str) -> bool:
        """Check if message is a close application command."""
        patterns = [
            r'\bclose\s+(\w+)',
            r'\bquit\s+(\w+)',
            r'\bkill\s+(\w+)',
            r'\bstop\s+(\w+)',
        ]
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _handle_close_app(self, message: str) -> str:
        """Handle closing an application."""
        patterns = [
            r'\bclose\s+(\w+(?:\s+\w+)?)',
            r'\bquit\s+(\w+(?:\s+\w+)?)',
            r'\bkill\s+(\w+(?:\s+\w+)?)',
            r'\bstop\s+(\w+(?:\s+\w+)?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                app_name = match.group(1).strip()
                success, msg = self.desktop.close_application(app_name)
                return msg
        
        return "I couldn't understand which application to close, Sir."
    
    def _is_open_website_command(self, message: str) -> bool:
        """Check if message is an open website command."""
        patterns = [
            r'\bopen\s+(?:website\s+)?(?:www\.)?[\w\.-]+\.(?:com|org|net|io|edu|gov)',
            r'\bgo\s+to\s+(?:www\.)?[\w\.-]+\.(?:com|org|net|io|edu|gov)',
            r'\bvisit\s+(?:www\.)?[\w\.-]+\.(?:com|org|net|io|edu|gov)',
        ]
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _handle_open_website(self, message: str) -> str:
        """Handle opening a website."""
        # Extract URL
        url_match = re.search(r'(?:www\.)?[\w\.-]+\.(?:com|org|net|io|edu|gov)(?:/[\w\.-]*)*', message)
        if url_match:
            url = url_match.group(0)
            success, msg = self.desktop.open_website(url)
            return msg
        
        return "I couldn't understand which website to open, Sir."
    
    def _is_open_folder_command(self, message: str) -> bool:
        """Check if message is an open folder command."""
        folders = ['desktop', 'downloads', 'documents', 'pictures', 'videos', 'music']
        return any(f'open {folder}' in message or f'open my {folder}' in message for folder in folders)
    
    def _handle_open_folder(self, message: str) -> str:
        """Handle opening a folder."""
        folders = ['desktop', 'downloads', 'documents', 'pictures', 'videos', 'music']
        
        for folder in folders:
            if folder in message:
                success, msg = self.desktop.open_folder(folder)
                return msg
        
        return "I couldn't understand which folder to open, Sir."
    
    def _is_list_apps_command(self, message: str) -> bool:
        """Check if message is a list applications command."""
        patterns = [
            r'what.*applications.*running',
            r'list.*running.*apps',
            r'show.*running.*applications',
            r'which.*apps.*running',
        ]
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _handle_list_apps(self) -> str:
        """Handle listing running applications."""
        apps = self.desktop.list_running_applications()
        if apps:
            # Show only first 15 to avoid overwhelming the user
            displayed_apps = apps[:15]
            app_list = ', '.join(displayed_apps)
            if len(apps) > 15:
                return f"Currently running applications: {app_list}, and {len(apps) - 15} more, Sir."
            return f"Currently running applications: {app_list}, Sir."
        return "No applications are currently running, Sir."
    
    def _is_minimize_command(self, message: str) -> bool:
        """Check if message is a minimize window command."""
        return 'minimize' in message
    
    def _handle_minimize(self, message: str) -> str:
        """Handle minimizing a window."""
        match = re.search(r'minimize\s+(\w+(?:\s+\w+)?)', message)
        if match:
            app_name = match.group(1).strip()
            success, msg = self.desktop.minimize_window(app_name)
            return msg
        return "I couldn't understand which window to minimize, Sir."
    
    def _is_maximize_command(self, message: str) -> bool:
        """Check if message is a maximize window command."""
        return 'maximize' in message
    
    def _handle_maximize(self, message: str) -> str:
        """Handle maximizing a window."""
        match = re.search(r'maximize\s+(\w+(?:\s+\w+)?)', message)
        if match:
            app_name = match.group(1).strip()
            success, msg = self.desktop.maximize_window(app_name)
            return msg
        return "I couldn't understand which window to maximize, Sir."
    
    def _is_focus_command(self, message: str) -> bool:
        """Check if message is a focus window command."""
        return 'focus' in message or 'switch to' in message
    
    def _handle_focus(self, message: str) -> str:
        """Handle focusing a window."""
        patterns = [
            r'focus\s+(?:on\s+)?(\w+(?:\s+\w+)?)',
            r'switch\s+to\s+(\w+(?:\s+\w+)?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                app_name = match.group(1).strip()
                success, msg = self.desktop.focus_window(app_name)
                return msg
        
        return "I couldn't understand which window to focus, Sir."
    
    # ==================== File Management Handlers ====================
    
    def _is_search_files_command(self, message: str) -> bool:
        """Check if message is a search files command."""
        patterns = [
            r'\bfind\s+(?:my\s+)?(?:file\s+)?',
            r'\bsearch\s+(?:for\s+)?',
            r'\bwhere\s+is\s+',
            r'\blocate\s+',
        ]
        return any(re.search(pattern, message) for pattern in patterns) and 'file' in message or 'document' in message
    
    def _handle_search_files(self, message: str) -> str:
        """Handle searching for files."""
        # Extract search query
        patterns = [
            r'\bfind\s+(?:my\s+)?(?:file\s+)?(.+)',
            r'\bsearch\s+(?:for\s+)?(.+)',
            r'\bwhere\s+is\s+(.+)',
            r'\blocate\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                query = match.group(1).strip()
                # Remove common words
                query = re.sub(r'\b(file|document|folder)\b', '', query).strip()
                
                results = self.files.search_files(query, limit=5)
                
                if results:
                    response = f"I found {len(results)} file(s), Sir:\n"
                    for i, file in enumerate(results, 1):
                        response += f"{i}. {file['name']} ({file['path']})\n"
                    return response.strip()
                else:
                    return f"I couldn't find any files matching '{query}', Sir."
        
        return "I couldn't understand what to search for, Sir."
    
    def _is_rename_file_command(self, message: str) -> bool:
        """Check if message is a rename file command."""
        return 'rename' in message
    
    def _handle_rename_file(self, message: str) -> str:
        """Handle renaming a file."""
        # This is a simplified handler - in practice, you'd need more sophisticated parsing
        return "File renaming requires specific file paths, Sir. Please provide the full path of the file you want to rename."
    
    def _is_move_file_command(self, message: str) -> bool:
        """Check if message is a move file command."""
        return 'move' in message and ('file' in message or 'to' in message)
    
    def _handle_move_file(self, message: str) -> str:
        """Handle moving a file."""
        return "File moving requires specific file paths, Sir. Please provide the source and destination paths."
    
    def _is_copy_file_command(self, message: str) -> bool:
        """Check if message is a copy file command."""
        return 'copy' in message and 'file' in message
    
    def _handle_copy_file(self, message: str) -> str:
        """Handle copying a file."""
        return "File copying requires specific file paths, Sir. Please provide the source and destination paths."
    
    def _is_delete_file_command(self, message: str) -> bool:
        """Check if message is a delete file command."""
        return 'delete' in message and ('file' in message or 'folder' in message)
    
    def _handle_delete_file(self, message: str) -> str:
        """Handle deleting a file (requires confirmation)."""
        # Extract filename if possible
        match = re.search(r'delete\s+(.+)', message)
        if match:
            filename = match.group(1).strip()
            # Search for the file
            results = self.files.search_files(filename, limit=1)
            if results:
                file_path = results[0]['path']
                return f"I found '{results[0]['name']}' at {file_path}. Are you sure you want to delete it, Sir? Please confirm by saying 'yes, delete it'."
            else:
                return f"I couldn't find a file named '{filename}', Sir."
        
        return "Please specify which file to delete, Sir."
    
    def _is_create_folder_command(self, message: str) -> bool:
        """Check if message is a create folder command."""
        patterns = [
            r'create.*folder',
            r'make.*folder',
            r'new.*folder',
            r'create.*directory',
        ]
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _handle_create_folder(self, message: str) -> str:
        """Handle creating a folder."""
        # Extract folder name
        patterns = [
            r'create\s+(?:a\s+)?folder\s+(?:called\s+|named\s+)?(.+)',
            r'make\s+(?:a\s+)?folder\s+(?:called\s+|named\s+)?(.+)',
            r'new\s+folder\s+(?:called\s+|named\s+)?(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                folder_name = match.group(1).strip()
                # Create in Downloads by default
                from pathlib import Path
                folder_path = str(Path.home() / 'Downloads' / folder_name)
                success, msg = self.files.create_folder(folder_path)
                return msg
        
        return "Please specify a name for the folder, Sir."
    
    def _is_compress_command(self, message: str) -> bool:
        """Check if message is a compress folder command."""
        return 'compress' in message or 'zip' in message
    
    def _handle_compress(self, message: str) -> str:
        """Handle compressing a folder."""
        return "Folder compression requires a specific folder path, Sir. Please provide the full path of the folder you want to compress."
    
    def _is_extract_command(self, message: str) -> bool:
        """Check if message is an extract ZIP command."""
        return 'extract' in message or 'unzip' in message
    
    def _handle_extract(self, message: str) -> str:
        """Handle extracting a ZIP file."""
        return "ZIP extraction requires a specific file path, Sir. Please provide the full path of the ZIP file you want to extract."
    
    def _is_organize_downloads_command(self, message: str) -> bool:
        """Check if message is an organize downloads command."""
        patterns = [
            r'organize.*downloads',
            r'clean.*downloads',
            r'sort.*downloads',
        ]
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _handle_organize_downloads(self) -> str:
        """Handle organizing the Downloads folder."""
        success, msg = self.files.organize_downloads()
        return msg
    
    def _is_recent_files_command(self, message: str) -> bool:
        """Check if message is a recent files command."""
        patterns = [
            r'recent.*files',
            r'files.*modified.*today',
            r'show.*recent',
            r'what.*files.*changed',
        ]
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _handle_recent_files(self, message: str) -> str:
        """Handle showing recent files."""
        # Determine number of days
        days = 1
        if 'week' in message:
            days = 7
        elif 'yesterday' in message:
            days = 2
        
        results = self.files.get_recent_files(days=days)
        
        if results:
            # Limit to 10 most recent
            shown = results[:10]
            response = f"I found {len(results)} file(s) modified in the last {days} day(s), Sir. Here are the most recent:\n"
            for i, file in enumerate(shown, 1):
                response += f"{i}. {file['name']} - {file['modified']}\n"
            return response.strip()
        else:
            return f"No files were modified in the last {days} day(s), Sir."
