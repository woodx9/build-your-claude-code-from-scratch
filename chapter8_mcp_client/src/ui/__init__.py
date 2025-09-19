"""
UI module for handling user interactions and display functionality.

This module provides a clean separation between UI concerns and business logic,
making the application more maintainable and testable.

Main Components:
- InputHandler: Handles all user input operations
- DisplayManager: Manages all display and output operations  
- UIManager: Unified interface that coordinates input and display
- Base classes: Abstract interfaces for extensibility
"""

from .input_handler import InputHandler
from .display_manager import DisplayManager
from .ui_manager import UIManager
from .base import BaseInputHandler, BaseDisplayManager, UIConfig

__all__ = [
    'InputHandler', 
    'DisplayManager', 
    'UIManager',
    'BaseInputHandler',
    'BaseDisplayManager', 
    'UIConfig'
]

# Version information
__version__ = '1.0.0'
__author__ = 'Quick Star Team'
