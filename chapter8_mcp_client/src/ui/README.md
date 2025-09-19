# UI Module

This module provides a clean separation of UI concerns from business logic, making the application more maintainable and testable.

## Quick Start

```python
from ui.ui_manager import UIManager

# Create UI manager instance
ui = UIManager()

# Display messages
ui.print_assistant_message("Hello **world**!")
ui.print_error("Something went wrong")
ui.print_success("Operation completed")

# Get user input
user_input = await ui.get_user_input()
approval = await ui.wait_for_user_approval("Delete file?")

# Streaming display
ui.start_stream_display()
ui.print_streaming_content("Streaming...")
ui.stop_stream_display()
```

## Module Structure

### `UIManager`
Main coordinator that provides a unified interface to all UI operations. Implements singleton pattern.

### `InputHandler` 
Handles all user input operations:
- `get_user_input()` - Basic input with prompt
- `wait_for_user_approval()` - Yes/no confirmation
- `get_choice_input()` - Input with predefined choices

### `DisplayManager`
Manages all display operations:
- `print_assistant_message()` - Markdown formatted messages
- `print_error/success/info()` - Styled status messages
- `start/stop_stream_display()` - Streaming content
- `print_streaming_content()` - Stream chunks

### `Base Classes`
Abstract interfaces for extensibility:
- `BaseInputHandler` - Input handler interface
- `BaseDisplayManager` - Display manager interface
- `UIConfig` - Configuration settings

## Features

- **Markdown Support**: Rich text formatting with Rich library
- **Streaming Display**: Real-time content updates
- **Emoji Indicators**: Visual feedback for different message types
- **Async Input**: Non-blocking user input handling
- **Singleton Pattern**: Consistent state across application
- **Type Hints**: Full type annotation support
- **Extensible**: Easy to add new UI backends

## Benefits

1. **Separation of Concerns**: UI logic separated from business logic
2. **Maintainability**: Clear interfaces and organized code
3. **Testability**: Easy to mock UI for testing
4. **Reusability**: UI components can be used across modules
5. **Configurability**: Customizable UI behavior
6. **Future-Proof**: Easy to add new UI features

## Migration from Old Code

### Before:
```python
# In Conversation class
user_input = await self.get_user_input()
self.print_assistant_messages("Hello")
```

### After:
```python
# Using UI module
ui = UIManager()
user_input = await ui.get_user_input()
ui.print_assistant_message("Hello")
```

## Configuration

```python
from ui.base import UIConfig
from ui.ui_manager import UIManager

config = UIConfig(
    default_emoji_user="👨‍💻",
    default_emoji_assistant="🤖",
    stream_refresh_rate=15
)
```


