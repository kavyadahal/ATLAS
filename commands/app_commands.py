"""
Application Commands Module
Implements application control commands.
"""

from typing import Dict, Any, Tuple


def register_app_commands(registry, desktop_controller):
    """
    Register all application-related commands.
    
    Args:
        registry: CommandRegistry instance
        desktop_controller: DesktopController instance
    """
    
    @registry.register('open_app')
    def open_app(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle opening an application."""
        app_name = params.get('app_name', '')
        return desktop_controller.open_application(app_name)
    
    @registry.register('close_app')
    def close_app(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle closing an application."""
        app_name = params.get('app_name', '')
        return desktop_controller.close_application(app_name)
    
    @registry.register('open_website')
    def open_website(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle opening a website."""
        url = params.get('url', '')
        return desktop_controller.open_website(url)
    
    @registry.register('open_folder')
    def open_folder(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle opening a system folder."""
        folder = params.get('folder', 'desktop')
        return desktop_controller.open_folder(folder)
