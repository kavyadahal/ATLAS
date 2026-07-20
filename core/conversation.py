"""
Conversation State Module
Manages conversation mode and timeout logic.
"""

import time


class ConversationState:
    """Manages conversation mode state and timeouts."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize conversation state.
        
        Args:
            timeout: Seconds of inactivity before exiting conversation mode
        """
        self.active = False
        self.last_interaction_time = None
        self.timeout = timeout
    
    def activate(self):
        """Activate conversation mode."""
        self.active = True
        self.last_interaction_time = time.time()
    
    def deactivate(self):
        """Deactivate conversation mode."""
        self.active = False
        self.last_interaction_time = None
    
    def is_active(self) -> bool:
        """Check if conversation mode is active."""
        return self.active
    
    def update_interaction(self):
        """Update the last interaction timestamp."""
        self.last_interaction_time = time.time()
    
    def check_timeout(self) -> bool:
        """
        Check if conversation has timed out.
        
        Returns:
            True if timed out (and deactivates), False otherwise
        """
        if self.active and self.last_interaction_time:
            if time.time() - self.last_interaction_time > self.timeout:
                self.deactivate()
                return True
        return False
