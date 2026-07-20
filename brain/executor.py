"""
Command Executor Module
Executes detected commands using command registry pattern.
"""

from typing import Tuple, Dict, Any
from commands.registry import CommandRegistry
from commands.file_commands import register_file_commands
from commands.app_commands import register_app_commands
from commands.system_commands import register_system_commands


class CommandExecutor:
    """Executes commands based on detected intent using registry pattern."""
    
    def __init__(self):
        """Initialize the command executor with automation modules and registry."""
        from automation.desktop_controller import DesktopController
        from automation.file_manager import FileManager
        from automation.file_writer import FileWriter
        
        # Initialize automation modules
        self.desktop = DesktopController()
        self.files = FileManager()
        self.file_writer = FileWriter()
        
        # Initialize command registry
        self.registry = CommandRegistry()
        
        # Register all commands
        register_file_commands(self.registry, self.files, self.file_writer)
        register_app_commands(self.registry, self.desktop)
        register_system_commands(self.registry, self.desktop, self.files)
    
    def execute(self, intent: str, params: Dict[str, Any]) -> Tuple[bool, str] | Tuple[None, str, str]:
        """
        Execute a command based on intent and parameters.
        
        Args:
            intent: The detected intent name
            params: Dictionary of parameters for the command
            
        Returns:
            Tuple of (success, message) or (None, message, 'needs_confirmation')
        """
        return self.registry.execute(intent, params)
