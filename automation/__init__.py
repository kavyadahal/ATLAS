"""
ATLAS Automation Module
Provides desktop control and file management capabilities
"""

from .desktop_controller import DesktopController
from .file_manager import FileManager
from .command_router import CommandRouter

__all__ = ['DesktopController', 'FileManager', 'CommandRouter']
