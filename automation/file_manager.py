"""
File Manager Module
Handles file operations like searching, moving, copying, organizing, etc.
"""

import os
import shutil
import zipfile
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class FileManager:
    """Manages file operations like search, copy, move, delete, etc."""
    
    # File type categories for organization
    FILE_CATEGORIES = {
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp'],
        'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
        'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        'code': ['.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.html', '.css', '.json', '.xml'],
        'executables': ['.exe', '.msi', '.bat', '.sh', '.app'],
    }
    
    def __init__(self):
        """Initialize the FileManager."""
        self.logger = logging.getLogger(__name__)
    
    def search_files(self, query: str, search_path: Optional[str] = None, limit: int = 20) -> List[Dict[str, str]]:
        """
        Search for files by name.
        
        Args:
            query: Search query (file name or pattern)
            search_path: Path to search in (defaults to user's home directory)
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries containing file information
        """
        try:
            if search_path is None:
                search_path = str(Path.home())
            
            results = []
            query_lower = query.lower()
            
            # Common locations to search
            common_paths = [
                Path.home() / 'Desktop',
                Path.home() / 'Downloads',
                Path.home() / 'Documents',
                Path.home() / 'Pictures',
            ]
            
            search_paths = common_paths if search_path == str(Path.home()) else [Path(search_path)]
            
            for base_path in search_paths:
                if not base_path.exists():
                    continue
                    
                try:
                    for root, dirs, files in os.walk(base_path):
                        # Skip system and hidden directories
                        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['AppData', 'System32']]
                        
                        for file in files:
                            if query_lower in file.lower():
                                file_path = os.path.join(root, file)
                                try:
                                    stat = os.stat(file_path)
                                    results.append({
                                        'name': file,
                                        'path': file_path,
                                        'size': stat.st_size,
                                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                                    })
                                    
                                    if len(results) >= limit:
                                        return results
                                except Exception:
                                    continue
                except PermissionError:
                    continue
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching files: {e}")
            return []
    
    def search_folders(self, query: str, search_path: Optional[str] = None, limit: int = 20) -> List[str]:
        """
        Search for folders by name.
        
        Args:
            query: Search query (folder name or pattern)
            search_path: Path to search in (defaults to user's home directory)
            limit: Maximum number of results to return
            
        Returns:
            List of folder paths
        """
        try:
            if search_path is None:
                search_path = str(Path.home())
            
            results = []
            query_lower = query.lower()
            
            for root, dirs, files in os.walk(search_path):
                # Skip system and hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['AppData', 'System32']]
                
                for dir_name in dirs:
                    if query_lower in dir_name.lower():
                        results.append(os.path.join(root, dir_name))
                        
                        if len(results) >= limit:
                            return results
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching folders: {e}")
            return []
    
    def rename_file(self, old_path: str, new_name: str) -> Tuple[bool, str]:
        """
        Rename a file.
        
        Args:
            old_path: Current file path
            new_name: New file name (not full path)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if not os.path.exists(old_path):
                return False, "I couldn't find that file, Sir."
            
            directory = os.path.dirname(old_path)
            new_path = os.path.join(directory, new_name)
            
            if os.path.exists(new_path):
                return False, f"A file named '{new_name}' already exists in that location, Sir. Would you like me to overwrite it?"
            
            os.rename(old_path, new_path)
            self.logger.info(f"Renamed file: {old_path} -> {new_path}")
            return True, f"Successfully renamed to '{new_name}', Sir."
            
        except Exception as e:
            self.logger.error(f"Error renaming file: {e}")
            return False, f"I couldn't rename that file, Sir. Error: {str(e)}"
    
    def copy_file(self, source_path: str, dest_path: str) -> Tuple[bool, str]:
        """
        Copy a file to a new location.
        
        Args:
            source_path: Source file path
            dest_path: Destination path (file or directory)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if not os.path.exists(source_path):
                return False, "I couldn't find that file, Sir."
            
            # If dest is a directory, keep the original filename
            if os.path.isdir(dest_path):
                filename = os.path.basename(source_path)
                dest_path = os.path.join(dest_path, filename)
            
            if os.path.exists(dest_path):
                return False, "A file already exists at that location, Sir. Would you like me to overwrite it?"
            
            shutil.copy2(source_path, dest_path)
            self.logger.info(f"Copied file: {source_path} -> {dest_path}")
            return True, f"Successfully copied the file, Sir."
            
        except Exception as e:
            self.logger.error(f"Error copying file: {e}")
            return False, f"I couldn't copy that file, Sir. Error: {str(e)}"
    
    def move_file(self, source_path: str, dest_path: str) -> Tuple[bool, str]:
        """
        Move a file to a new location.
        
        Args:
            source_path: Source file path
            dest_path: Destination path (file or directory)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if not os.path.exists(source_path):
                return False, "I couldn't find that file, Sir."
            
            # If dest is a directory, keep the original filename
            if os.path.isdir(dest_path):
                filename = os.path.basename(source_path)
                dest_path = os.path.join(dest_path, filename)
            
            if os.path.exists(dest_path):
                return False, "A file already exists at that location, Sir. Would you like me to overwrite it?"
            
            shutil.move(source_path, dest_path)
            self.logger.info(f"Moved file: {source_path} -> {dest_path}")
            return True, f"Successfully moved the file, Sir."
            
        except Exception as e:
            self.logger.error(f"Error moving file: {e}")
            return False, f"I couldn't move that file, Sir. Error: {str(e)}"
    
    def delete_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Delete a file.
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if not os.path.exists(file_path):
                return False, "I couldn't find that file, Sir."
            
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                self.logger.info(f"Deleted directory: {file_path}")
            else:
                os.remove(file_path)
                self.logger.info(f"Deleted file: {file_path}")
            
            return True, "Successfully deleted, Sir."
            
        except Exception as e:
            self.logger.error(f"Error deleting file: {e}")
            return False, f"I couldn't delete that file, Sir. Error: {str(e)}"
    
    def create_folder(self, path: str) -> Tuple[bool, str]:
        """
        Create a new folder.
        
        Args:
            path: Path for the new folder
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if os.path.exists(path):
                return False, "A folder with that name already exists, Sir."
            
            os.makedirs(path, exist_ok=True)
            self.logger.info(f"Created folder: {path}")
            return True, f"Successfully created the folder, Sir."
            
        except Exception as e:
            self.logger.error(f"Error creating folder: {e}")
            return False, f"I couldn't create that folder, Sir. Error: {str(e)}"
    
    def create_file(self, path: str) -> Tuple[bool, str]:
        """
        Create a new empty file.
        
        Args:
            path: Path for the new file
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if os.path.exists(path):
                return False, "A file with that name already exists, Sir."
            
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            # Create empty file
            Path(path).touch()
            self.logger.info(f"Created file: {path}")
            return True, f"Successfully created the file, Sir."
            
        except Exception as e:
            self.logger.error(f"Error creating file: {e}")
            return False, f"I couldn't create that file, Sir. Error: {str(e)}"
    
    def compress_folder(self, folder_path: str, output_path: Optional[str] = None) -> Tuple[bool, str]:
        """
        Compress a folder into a ZIP file.
        
        Args:
            folder_path: Path to the folder to compress
            output_path: Path for the output ZIP file (optional)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if not os.path.exists(folder_path):
                return False, "I couldn't find that folder, Sir."
            
            if not os.path.isdir(folder_path):
                return False, "That's not a folder, Sir."
            
            if output_path is None:
                output_path = f"{folder_path}.zip"
            
            if os.path.exists(output_path):
                return False, "A ZIP file with that name already exists, Sir."
            
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                        zipf.write(file_path, arcname)
            
            self.logger.info(f"Compressed folder: {folder_path} -> {output_path}")
            return True, f"Successfully compressed to '{os.path.basename(output_path)}', Sir."
            
        except Exception as e:
            self.logger.error(f"Error compressing folder: {e}")
            return False, f"I couldn't compress that folder, Sir. Error: {str(e)}"
    
    def extract_zip(self, zip_path: str, extract_to: Optional[str] = None) -> Tuple[bool, str]:
        """
        Extract a ZIP file.
        
        Args:
            zip_path: Path to the ZIP file
            extract_to: Path to extract to (optional)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if not os.path.exists(zip_path):
                return False, "I couldn't find that ZIP file, Sir."
            
            if extract_to is None:
                extract_to = os.path.splitext(zip_path)[0]
            
            if os.path.exists(extract_to):
                return False, "A folder with that name already exists, Sir."
            
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(extract_to)
            
            self.logger.info(f"Extracted ZIP: {zip_path} -> {extract_to}")
            return True, f"Successfully extracted to '{os.path.basename(extract_to)}', Sir."
            
        except Exception as e:
            self.logger.error(f"Error extracting ZIP: {e}")
            return False, f"I couldn't extract that ZIP file, Sir. Error: {str(e)}"
    
    def organize_downloads(self) -> Tuple[bool, str]:
        """
        Organize files in the Downloads folder by file type.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            downloads_path = Path.home() / 'Downloads'
            
            if not downloads_path.exists():
                return False, "I couldn't find the Downloads folder, Sir."
            
            organized_count = 0
            
            # Create category folders
            for category in self.FILE_CATEGORIES.keys():
                category_path = downloads_path / category.title()
                category_path.mkdir(exist_ok=True)
            
            # Move files to appropriate categories
            for item in downloads_path.iterdir():
                if item.is_file():
                    file_ext = item.suffix.lower()
                    
                    for category, extensions in self.FILE_CATEGORIES.items():
                        if file_ext in extensions:
                            dest_folder = downloads_path / category.title()
                            dest_path = dest_folder / item.name
                            
                            # Handle duplicates
                            counter = 1
                            while dest_path.exists():
                                name_without_ext = item.stem
                                dest_path = dest_folder / f"{name_without_ext}_{counter}{file_ext}"
                                counter += 1
                            
                            shutil.move(str(item), str(dest_path))
                            organized_count += 1
                            break
            
            self.logger.info(f"Organized {organized_count} files in Downloads")
            
            if organized_count > 0:
                return True, f"Successfully organized {organized_count} files in Downloads, Sir."
            else:
                return True, "The Downloads folder is already organized, Sir."
                
        except Exception as e:
            self.logger.error(f"Error organizing downloads: {e}")
            return False, f"I couldn't organize the Downloads folder, Sir. Error: {str(e)}"
    
    def get_recent_files(self, days: int = 1, search_path: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Get files modified within the last N days.
        
        Args:
            days: Number of days to look back
            search_path: Path to search in (defaults to common locations)
            
        Returns:
            List of dictionaries containing file information
        """
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            results = []
            
            if search_path:
                search_paths = [Path(search_path)]
            else:
                search_paths = [
                    Path.home() / 'Desktop',
                    Path.home() / 'Downloads',
                    Path.home() / 'Documents',
                ]
            
            for base_path in search_paths:
                if not base_path.exists():
                    continue
                
                try:
                    for root, dirs, files in os.walk(base_path):
                        # Skip system directories
                        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['AppData']]
                        
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                stat = os.stat(file_path)
                                modified_time = datetime.fromtimestamp(stat.st_mtime)
                                
                                if modified_time >= cutoff_time:
                                    results.append({
                                        'name': file,
                                        'path': file_path,
                                        'size': stat.st_size,
                                        'modified': modified_time.strftime('%Y-%m-%d %H:%M:%S')
                                    })
                            except Exception:
                                continue
                except PermissionError:
                    continue
            
            # Sort by modified time (newest first)
            results.sort(key=lambda x: x['modified'], reverse=True)
            return results
            
        except Exception as e:
            self.logger.error(f"Error getting recent files: {e}")
            return []
    
    def get_file_info(self, file_path: str) -> Optional[Dict[str, str]]:
        """
        Get detailed information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file information or None
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'size': stat.st_size,
                'size_readable': self._format_size(stat.st_size),
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'extension': os.path.splitext(file_path)[1],
                'is_directory': os.path.isdir(file_path)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            return None
    
    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
