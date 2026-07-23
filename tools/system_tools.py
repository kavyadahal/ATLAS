"""
System Tools Module
Provides system-level utilities like shutdown and sleep timers.
"""

import subprocess
from typing import Tuple


class SystemTimer:
    """Handles system shutdown and sleep timer operations."""
    
    def __init__(self):
        """Initialize system timer."""
        pass
    
    def schedule_shutdown(self, minutes: int) -> Tuple[bool, str]:
        """
        Schedule Windows shutdown after specified minutes.
        
        Args:
            minutes: Number of minutes until shutdown
            
        Returns:
            Tuple of (success, message)
        """
        try:
            seconds = minutes * 60
            
            # Schedule shutdown using Windows shutdown command
            result = subprocess.run(
                ['shutdown', '/s', '/t', str(seconds)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                if minutes == 1:
                    return True, f"Shutdown scheduled for 1 minute from now, Sir."
                elif minutes < 60:
                    return True, f"Shutdown scheduled for {minutes} minutes from now, Sir."
                else:
                    hours = minutes / 60
                    if hours == 1:
                        return True, f"Shutdown scheduled for 1 hour from now, Sir."
                    else:
                        return True, f"Shutdown scheduled for {hours:.1f} hours from now, Sir."
            else:
                error = result.stderr.strip() if result.stderr else "Unknown error"
                return False, f"Failed to schedule shutdown: {error}, Sir."
                
        except Exception as e:
            return False, f"Error scheduling shutdown: {str(e)}, Sir."
    
    def cancel_shutdown(self) -> Tuple[bool, str]:
        """
        Cancel pending shutdown timer.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Cancel shutdown using Windows shutdown command
            result = subprocess.run(
                ['shutdown', '/a'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return True, "Shutdown timer cancelled, Sir."
            else:
                # Check if there was no shutdown scheduled
                error_msg = result.stderr.strip() if result.stderr else ""
                if "1116" in error_msg or "no logoff" in error_msg.lower():
                    return False, "There is no shutdown scheduled to cancel, Sir."
                else:
                    return False, f"Failed to cancel shutdown: {error_msg}, Sir."
                    
        except Exception as e:
            return False, f"Error cancelling shutdown: {str(e)}, Sir."
    
    def schedule_sleep(self, minutes: int) -> Tuple[bool, str]:
        """
        Schedule Windows sleep after specified minutes.
        Note: This schedules sleep using a delayed command.
        
        Args:
            minutes: Number of minutes until sleep
            
        Returns:
            Tuple of (success, message)
        """
        try:
            seconds = minutes * 60
            
            # Schedule sleep using rundll32 with timeout
            # We use PowerShell to schedule the sleep command
            powershell_cmd = f'Start-Sleep -Seconds {seconds}; Add-Type -Assembly System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState("Suspend", $false, $false)'
            
            # Start the PowerShell command in the background
            subprocess.Popen(
                ['powershell', '-WindowStyle', 'Hidden', '-Command', powershell_cmd],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if minutes == 1:
                return True, f"Sleep scheduled for 1 minute from now, Sir."
            elif minutes < 60:
                return True, f"Sleep scheduled for {minutes} minutes from now, Sir."
            else:
                hours = minutes / 60
                if hours == 1:
                    return True, f"Sleep scheduled for 1 hour from now, Sir."
                else:
                    return True, f"Sleep scheduled for {hours:.1f} hours from now, Sir."
                    
        except Exception as e:
            return False, f"Error scheduling sleep: {str(e)}, Sir."
