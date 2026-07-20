"""
Command Registry Module
Implements command registry pattern to replace if/elif chains.
"""

from typing import Dict, Any, Tuple, Callable


class CommandRegistry:
    """Registry pattern for command execution."""
    
    def __init__(self):
        """Initialize the command registry."""
        self._commands: Dict[str, Callable] = {}
    
    def register(self, intent_name: str):
        """
        Decorator to register a command handler.
        
        Args:
            intent_name: The intent name to register
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable):
            self._commands[intent_name] = func
            return func
        return decorator
    
    def execute(self, intent: str, params: Dict[str, Any]) -> Tuple[bool, str] | Tuple[None, str, str]:
        """
        Execute a command based on intent.
        
        Args:
            intent: The intent name
            params: Parameters for the command
            
        Returns:
            Tuple of (success, message) or (None, message, 'needs_confirmation')
        """
        if intent in self._commands:
            try:
                return self._commands[intent](params)
            except Exception as e:
                return False, f"Error executing command: {str(e)}, Sir."
        else:
            return False, f"I don't know how to handle '{intent}' yet, Sir."
    
    def has_command(self, intent: str) -> bool:
        """Check if a command is registered."""
        return intent in self._commands
    
    def list_commands(self) -> list:
        """List all registered commands."""
        return list(self._commands.keys())
