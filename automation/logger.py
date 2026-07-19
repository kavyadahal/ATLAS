"""
Logging Configuration for ATLAS Automation
Logs all desktop and file operations with timestamps and status
"""

import logging
import os
from pathlib import Path
from datetime import datetime


class AutomationLogger:
    """Configure and manage logging for automation operations."""
    
    def __init__(self, log_dir: str = None):
        """
        Initialize the automation logger.
        
        Args:
            log_dir: Directory to store log files (defaults to logs/ in project root)
        """
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        
        # Create logs directory if it doesn't exist
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        # Create log file with current date
        log_filename = f"atlas_automation_{datetime.now().strftime('%Y%m%d')}.log"
        log_path = os.path.join(log_dir, log_filename)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler()  # Also log to console
            ]
        )
        
        self.logger = logging.getLogger('ATLAS.Automation')
        self.logger.info("=" * 50)
        self.logger.info("ATLAS Automation Logger Initialized")
        self.logger.info("=" * 50)
    
    def log_desktop_action(self, action: str, target: str, success: bool, error: str = None):
        """
        Log a desktop control action.
        
        Args:
            action: Type of action (open, close, minimize, etc.)
            target: Target application or window
            success: Whether the action succeeded
            error: Error message if action failed
        """
        status = "SUCCESS" if success else "FAILED"
        message = f"Desktop Action: {action.upper()} | Target: {target} | Status: {status}"
        
        if error:
            message += f" | Error: {error}"
        
        if success:
            self.logger.info(message)
        else:
            self.logger.error(message)
    
    def log_file_action(self, action: str, source: str, destination: str = None, success: bool = True, error: str = None):
        """
        Log a file management action.
        
        Args:
            action: Type of action (search, move, copy, delete, etc.)
            source: Source file or folder path
            destination: Destination path (if applicable)
            success: Whether the action succeeded
            error: Error message if action failed
        """
        status = "SUCCESS" if success else "FAILED"
        message = f"File Action: {action.upper()} | Source: {source}"
        
        if destination:
            message += f" | Destination: {destination}"
        
        message += f" | Status: {status}"
        
        if error:
            message += f" | Error: {error}"
        
        if success:
            self.logger.info(message)
        else:
            self.logger.error(message)
    
    def log_command(self, command: str, handled: bool):
        """
        Log a user command.
        
        Args:
            command: The user's command
            handled: Whether the command was handled by automation
        """
        if handled:
            self.logger.info(f"Command Handled: {command}")
        else:
            self.logger.debug(f"Command Not Handled: {command}")
    
    def log_error(self, error: str, context: str = None):
        """
        Log an error.
        
        Args:
            error: Error message
            context: Additional context about the error
        """
        message = f"Error: {error}"
        if context:
            message += f" | Context: {context}"
        
        self.logger.error(message)
    
    def log_warning(self, warning: str):
        """
        Log a warning.
        
        Args:
            warning: Warning message
        """
        self.logger.warning(f"Warning: {warning}")
    
    def log_info(self, info: str):
        """
        Log general information.
        
        Args:
            info: Information message
        """
        self.logger.info(info)


# Global logger instance
_global_logger = None


def get_logger():
    """Get the global automation logger instance."""
    global _global_logger
    if _global_logger is None:
        _global_logger = AutomationLogger()
    return _global_logger


def setup_logging():
    """Initialize the global logger."""
    global _global_logger
    _global_logger = AutomationLogger()
    return _global_logger
