"""
Desktop Controller Module
Handles desktop operations like opening/closing applications, window management, etc.
"""

import subprocess
import os
import webbrowser
import psutil
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DesktopController:
    """Controls desktop operations like opening apps, managing windows, etc."""
    
    # Common folder paths
    COMMON_FOLDERS = {
        'desktop': str(Path.home() / 'Desktop'),
        'downloads': str(Path.home() / 'Downloads'),
        'documents': str(Path.home() / 'Documents'),
        'pictures': str(Path.home() / 'Pictures'),
        'videos': str(Path.home() / 'Videos'),
        'music': str(Path.home() / 'Music'),
    }
    
    # Common applications (Windows)
    # Maps app aliases to (exe_name, possible_paths)
    COMMON_APPS = {
        'google': ['chrome.exe', 'Google\\Chrome\\Application\\chrome.exe'],
        'google chrome': ['chrome.exe', 'Google\\Chrome\\Application\\chrome.exe'],
        'chrome': ['chrome.exe', 'Google\\Chrome\\Application\\chrome.exe'],
        'firefox': ['firefox.exe', 'Mozilla Firefox\\firefox.exe'],
        'edge': ['msedge.exe', 'Microsoft\\Edge\\Application\\msedge.exe'],
        'notepad': ['notepad.exe'],
        'calculator': ['calc.exe'],
        'calc': ['calc.exe'],
        'explorer': ['explorer.exe'],
        'vscode': ['code.exe', 'Microsoft VS Code\\Code.exe'],
        'vs code': ['code.exe', 'Microsoft VS Code\\Code.exe'],
        'visual studio code': ['code.exe', 'Microsoft VS Code\\Code.exe'],
        'code': ['code.exe', 'Microsoft VS Code\\Code.exe'],
        'spotify': ['Spotify.exe', 'Spotify\\Spotify.exe'],
        'discord': ['Discord.exe', 'Discord\\Discord.exe'],
        'teams': ['Teams.exe', 'Microsoft\\Teams\\Teams.exe'],
        'outlook': ['OUTLOOK.EXE', 'Microsoft Office\\root\\Office16\\OUTLOOK.EXE'],
        'word': ['WINWORD.EXE', 'Microsoft Office\\root\\Office16\\WINWORD.EXE'],
        'excel': ['EXCEL.EXE', 'Microsoft Office\\root\\Office16\\EXCEL.EXE'],
        'powerpoint': ['POWERPNT.EXE', 'Microsoft Office\\root\\Office16\\POWERPNT.EXE'],
    }
    
    # Apps that should open as websites instead
    WEBSITE_APPS = {
        'youtube': 'https://www.youtube.com',
        'gmail': 'https://mail.google.com',
        'github': 'https://github.com',
        'reddit': 'https://www.reddit.com',
        'twitter': 'https://twitter.com',
        'facebook': 'https://www.facebook.com',
        'instagram': 'https://www.instagram.com',
    }
    
    def __init__(self):
        """Initialize the DesktopController."""
        self.logger = logging.getLogger(__name__)
    
    def open_application(self, app_name: str) -> Tuple[bool, str]:
        """
        Open an application by name.
        
        Args:
            app_name: Name of the application to open
            
        Returns:
            Tuple of (success, message)
        """
        try:
            app_name_lower = app_name.lower().strip()
            
            # Check if it's a website app (like "open youtube")
            if app_name_lower in self.WEBSITE_APPS:
                url = self.WEBSITE_APPS[app_name_lower]
                return self.open_website(url)
            
            # Check common apps first
            if app_name_lower in self.COMMON_APPS:
                executables = self.COMMON_APPS[app_name_lower]
                
                for exe in executables:
                    try:
                        # Extract just the exe name (first element or split from path)
                        exe_name = exe.split('\\')[-1] if '\\' in exe else exe
                        
                        # Try using shutil.which for system apps
                        import shutil
                        exe_path = shutil.which(exe_name)
                        if exe_path:
                            subprocess.Popen([exe_path], shell=False)
                            self.logger.info(f"Opened application: {app_name} using {exe_path}")
                            return True, f"Successfully opened {app_name}, Sir."
                        
                        # Try in Program Files directories
                        if '\\' in exe:
                            program_files = [
                                os.environ.get('ProgramFiles', 'C:\\Program Files'),
                                os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'),
                                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs'),
                            ]
                            
                            for base_path in program_files:
                                if not base_path:
                                    continue
                                full_path = os.path.join(base_path, exe)
                                if os.path.exists(full_path):
                                    subprocess.Popen([full_path], shell=False)
                                    self.logger.info(f"Opened application: {app_name} from {full_path}")
                                    return True, f"Successfully opened {app_name}, Sir."
                    except Exception as e:
                        self.logger.debug(f"Failed attempt with {exe}: {e}")
                        continue
                
                # If we got here, none of the paths worked
                self.logger.error(f"Could not find {app_name} in any known location")
                return False, f"I couldn't find {app_name}, Sir. Please ensure it's installed."
            
            # Try using shutil.which for unknown apps
            import shutil
            exe_path = shutil.which(app_name)
            if exe_path:
                subprocess.Popen([exe_path], shell=False)
                self.logger.info(f"Opened application: {app_name}")
                return True, f"Successfully opened {app_name}, Sir."
            
            # Try with .exe extension
            if not app_name.endswith('.exe'):
                exe_path = shutil.which(f"{app_name}.exe")
                if exe_path:
                    subprocess.Popen([exe_path], shell=False)
                    self.logger.info(f"Opened application: {app_name}")
                    return True, f"Successfully opened {app_name}, Sir."
            
            # Last resort: try as direct command (for system commands like notepad, calc)
            try:
                result = subprocess.run(
                    [app_name],
                    shell=False,
                    capture_output=True,
                    timeout=1
                )
                # If it didn't error immediately, assume it worked
                self.logger.info(f"Opened application: {app_name}")
                return True, f"Successfully opened {app_name}, Sir."
            except subprocess.TimeoutExpired:
                # Process is running, that's good
                self.logger.info(f"Opened application: {app_name}")
                return True, f"Successfully opened {app_name}, Sir."
            except Exception as e:
                self.logger.error(f"Failed to open {app_name}: {e}")
                return False, f"I couldn't find or open {app_name}, Sir. Please ensure it's installed."
                
        except Exception as e:
            self.logger.error(f"Error opening application {app_name}: {e}")
            return False, f"An error occurred while trying to open {app_name}, Sir."
    
    def close_application(self, app_name: str) -> Tuple[bool, str]:
        """
        Close a running application by name.
        
        Args:
            app_name: Name of the application to close
            
        Returns:
            Tuple of (success, message)
        """
        try:
            app_name_lower = app_name.lower()
            closed_count = 0
            
            # Get the executable name
            exe_names = []
            if app_name_lower in self.COMMON_APPS:
                exe_names = [exe.split('\\')[-1].lower() for exe in self.COMMON_APPS[app_name_lower]]
            else:
                exe_names = [app_name_lower if app_name_lower.endswith('.exe') else f"{app_name_lower}.exe"]
            
            # Find and terminate matching processes
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(exe_name in proc_name for exe_name in exe_names):
                        proc.terminate()
                        closed_count += 1
                        self.logger.info(f"Closed process: {proc.info['name']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed_count > 0:
                return True, f"Successfully closed {app_name}, Sir."
            else:
                return False, f"{app_name} is not currently running, Sir."
                
        except Exception as e:
            self.logger.error(f"Error closing application {app_name}: {e}")
            return False, f"An error occurred while trying to close {app_name}, Sir."
    
    def open_website(self, url: str) -> Tuple[bool, str]:
        """
        Open a website in the default browser.
        
        Args:
            url: URL to open (can be with or without http://)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Add https:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = f"https://{url}"
            
            webbrowser.open(url)
            self.logger.info(f"Opened website: {url}")
            return True, f"Opening {url}, Sir."
            
        except Exception as e:
            self.logger.error(f"Error opening website {url}: {e}")
            return False, f"I couldn't open that website, Sir."
    
    def open_folder(self, folder_name: str) -> Tuple[bool, str]:
        """
        Open a common folder or a specific path.
        
        Args:
            folder_name: Name of folder (desktop, downloads, etc.) or path
            
        Returns:
            Tuple of (success, message)
        """
        try:
            folder_name_lower = folder_name.lower()
            
            # Check if it's a common folder
            if folder_name_lower in self.COMMON_FOLDERS:
                folder_path = self.COMMON_FOLDERS[folder_name_lower]
            else:
                folder_path = folder_name
            
            # Check if path exists
            if not os.path.exists(folder_path):
                return False, f"I couldn't find the {folder_name} folder, Sir."
            
            # Open with explorer
            os.startfile(folder_path)
            self.logger.info(f"Opened folder: {folder_path}")
            return True, f"Opening {folder_name} folder, Sir."
            
        except Exception as e:
            self.logger.error(f"Error opening folder {folder_name}: {e}")
            return False, f"I couldn't open the {folder_name} folder, Sir."
    
    def open_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Open a file with its default application.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if not os.path.exists(file_path):
                return False, f"I couldn't find that file, Sir."
            
            os.startfile(file_path)
            self.logger.info(f"Opened file: {file_path}")
            return True, f"Opening the file, Sir."
            
        except Exception as e:
            self.logger.error(f"Error opening file {file_path}: {e}")
            return False, f"I couldn't open that file, Sir."
    
    def list_running_applications(self) -> List[str]:
        """
        Get a list of currently running applications.
        
        Returns:
            List of application names
        """
        try:
            apps = set()
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name']
                    if name and not name.startswith('svchost'):
                        apps.add(name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return sorted(list(apps))
            
        except Exception as e:
            self.logger.error(f"Error listing applications: {e}")
            return []
    
    def search_applications(self, query: str) -> List[str]:
        """
        Search for installed applications.
        
        Args:
            query: Search query
            
        Returns:
            List of matching application names
        """
        matches = []
        query_lower = query.lower()
        
        # Search in common apps
        for app_name in self.COMMON_APPS.keys():
            if query_lower in app_name:
                matches.append(app_name)
        
        return matches
    
    def minimize_window(self, app_name: str) -> Tuple[bool, str]:
        """
        Minimize an application window.
        
        Args:
            app_name: Name of the application
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # This requires pywin32 which we'll add to requirements
            import win32gui
            import win32con
            
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if app_name.lower() in title.lower():
                        windows.append(hwnd)
            
            windows = []
            win32gui.EnumWindows(callback, windows)
            
            if windows:
                for hwnd in windows:
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                self.logger.info(f"Minimized window: {app_name}")
                return True, f"Minimized {app_name}, Sir."
            else:
                return False, f"I couldn't find a window for {app_name}, Sir."
                
        except ImportError:
            return False, "Window management requires pywin32 package, Sir."
        except Exception as e:
            self.logger.error(f"Error minimizing window {app_name}: {e}")
            return False, f"I couldn't minimize {app_name}, Sir."
    
    def maximize_window(self, app_name: str) -> Tuple[bool, str]:
        """
        Maximize an application window.
        
        Args:
            app_name: Name of the application
            
        Returns:
            Tuple of (success, message)
        """
        try:
            import win32gui
            import win32con
            
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if app_name.lower() in title.lower():
                        windows.append(hwnd)
            
            windows = []
            win32gui.EnumWindows(callback, windows)
            
            if windows:
                for hwnd in windows:
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                self.logger.info(f"Maximized window: {app_name}")
                return True, f"Maximized {app_name}, Sir."
            else:
                return False, f"I couldn't find a window for {app_name}, Sir."
                
        except ImportError:
            return False, "Window management requires pywin32 package, Sir."
        except Exception as e:
            self.logger.error(f"Error maximizing window {app_name}: {e}")
            return False, f"I couldn't maximize {app_name}, Sir."
    
    def focus_window(self, app_name: str) -> Tuple[bool, str]:
        """
        Bring an application window to focus.
        
        Args:
            app_name: Name of the application
            
        Returns:
            Tuple of (success, message)
        """
        try:
            import win32gui
            import win32con
            
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if app_name.lower() in title.lower():
                        windows.append(hwnd)
            
            windows = []
            win32gui.EnumWindows(callback, windows)
            
            if windows:
                hwnd = windows[0]
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                self.logger.info(f"Focused window: {app_name}")
                return True, f"Focused {app_name}, Sir."
            else:
                return False, f"I couldn't find a window for {app_name}, Sir."
                
        except ImportError:
            return False, "Window management requires pywin32 package, Sir."
        except Exception as e:
            self.logger.error(f"Error focusing window {app_name}: {e}")
            return False, f"I couldn't focus {app_name}, Sir."
