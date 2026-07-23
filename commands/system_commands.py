"""
System Commands Module
Implements system-level commands.
"""

from typing import Dict, Any, Tuple
import os
import subprocess
from tools.system_tools import SystemTimer


def register_system_commands(registry, desktop_controller, file_manager):
    """
    Register all system-related commands.
    
    Args:
        registry: CommandRegistry instance
        desktop_controller: DesktopController instance
        file_manager: FileManager instance
    """
    
    # Initialize system timer
    system_timer = SystemTimer()
    
    @registry.register('list_apps')
    def list_apps(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle listing running applications."""
        apps = desktop_controller.list_running_applications()
        
        if apps:
            displayed_apps = apps[:15]
            app_list = ', '.join(displayed_apps)
            if len(apps) > 15:
                return True, f"Currently running applications: {app_list}, and {len(apps) - 15} more, Sir."
            return True, f"Currently running applications: {app_list}, Sir."
        
        return True, "No applications are currently running, Sir."
    
    @registry.register('organize_downloads')
    def organize_downloads(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle organizing the Downloads folder."""
        return file_manager.organize_downloads()
    
    @registry.register('run_python')
    def run_python(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle running a Python file."""
        filename = params.get('filename', '')
        
        if not os.path.exists(filename):
            results = file_manager.search_files(filename, limit=1)
            if results:
                filename = results[0]['path']
            else:
                return False, f"I couldn't find '{filename}', Sir."
        
        try:
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
    
    @registry.register('schedule_shutdown')
    def schedule_shutdown(params: Dict[str, Any]) -> Tuple[bool, str] | Tuple[None, str, str]:
        """Handle scheduling system shutdown."""
        minutes = params.get('minutes', 30)
        
        # Check if this is a confirmation (already confirmed by user)
        if params.get('confirmed', False):
            # Execute the shutdown
            return system_timer.schedule_shutdown(minutes)
        else:
            # Ask for confirmation
            if minutes == 1:
                time_str = "1 minute"
            elif minutes < 60:
                time_str = f"{minutes} minutes"
            elif minutes == 60:
                time_str = "1 hour"
            else:
                hours = minutes / 60
                time_str = f"{hours:.1f} hours"
            
            return None, f"Your computer will shut down in {time_str}. Should I continue, Sir?", 'needs_confirmation'
    
    @registry.register('cancel_shutdown')
    def cancel_shutdown(params: Dict[str, Any]) -> Tuple[bool, str]:
        """Handle cancelling shutdown timer."""
        return system_timer.cancel_shutdown()
    
    @registry.register('schedule_sleep')
    def schedule_sleep(params: Dict[str, Any]) -> Tuple[bool, str] | Tuple[None, str, str]:
        """Handle scheduling system sleep."""
        minutes = params.get('minutes', 30)
        
        # Check if this is a confirmation (already confirmed by user)
        if params.get('confirmed', False):
            # Execute the sleep timer
            return system_timer.schedule_sleep(minutes)
        else:
            # Ask for confirmation
            if minutes == 1:
                time_str = "1 minute"
            elif minutes < 60:
                time_str = f"{minutes} minutes"
            elif minutes == 60:
                time_str = "1 hour"
            else:
                hours = minutes / 60
                time_str = f"{hours:.1f} hours"
            
            return None, f"Your computer will sleep in {time_str}. Should I continue, Sir?", 'needs_confirmation'
