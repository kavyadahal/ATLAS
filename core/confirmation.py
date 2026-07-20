"""
Confirmation Manager Module
Handles pending action confirmations and user responses.
"""

from typing import Optional, Dict, Any, Tuple


class ConfirmationManager:
    """Manages confirmation requests for sensitive operations."""
    
    # Confirmation keywords
    YES_WORDS = ["yes", "y", "yeah", "yep", "confirm", "proceed", "do it", "go ahead", "okay", "ok"]
    NO_WORDS = ["no", "n", "cancel", "abort", "stop", "never mind", "nevermind"]
    
    def __init__(self):
        """Initialize confirmation manager."""
        self.pending_confirmation = None
    
    def set_pending(self, intent: str, params: Dict[str, Any]):
        """
        Set a pending confirmation.
        
        Args:
            intent: The intent requiring confirmation
            params: Parameters for the intent
        """
        self.pending_confirmation = {
            'intent': intent,
            'params': {**params, 'confirmed': True}  # Add confirmed flag
        }
    
    def has_pending(self) -> bool:
        """Check if there's a pending confirmation."""
        return self.pending_confirmation is not None
    
    def get_pending(self) -> Optional[Dict[str, Any]]:
        """Get the pending confirmation."""
        return self.pending_confirmation
    
    def clear_pending(self):
        """Clear the pending confirmation."""
        self.pending_confirmation = None
    
    def process_response(self, text: str) -> Optional[str]:
        """
        Process user response to confirmation request.
        
        Args:
            text: User's response text
            
        Returns:
            'confirmed' if user confirmed
            'cancelled' if user cancelled
            'unclear' if response is ambiguous
            None if no pending confirmation
        """
        if not self.has_pending():
            return None
        
        text_lower = text.lower().strip()
        
        if text_lower in self.YES_WORDS:
            return 'confirmed'
        elif text_lower in self.NO_WORDS:
            return 'cancelled'
        else:
            return 'unclear'
