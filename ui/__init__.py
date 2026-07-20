"""
UI Module
Handles all user interface concerns including console output and input handling.
"""

from .console import Console
from .input_handler import InputThreadManager

__all__ = ['Console', 'InputThreadManager']
