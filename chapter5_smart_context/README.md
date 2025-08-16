# Chapter 5: Smart Context Cropping

[中文版本](./README_zh.md)

## What's New in Chapter 5

Chapter 5 adds **Smart Context Cropping** - a precision tool for advanced conversation management, building on Chapter 4's automatic history compression:

### 🎯 Smart Context Cropper Tool
- **Precision control**: Crop specific number of messages from TOP or BOTTOM
- **Safety guarantees**: Always protects latest user messages and system messages  
- **Summary support**: Optional summaries for cropped content to maintain context continuity
- **Immediate effect**: Cropping operations take effect instantly for performance optimization
- **Integration**: Seamlessly works with existing tool chain and approval system

## Context Cropping vs Auto Compression

| Feature | Auto Compression (Ch4) | Smart Cropping (Ch5) |
|---------|----------------------|---------------------|
| **Trigger** | Automatic (threshold) | Manual (user/AI decision) |
| **Control** | System-driven | User/AI-driven |
| **Precision** | Session-level | Message-level |
| **Use Case** | Performance management | Strategic context control |

## Cropping Strategies

### TOP Cropping
Remove oldest messages while preserving system context:
```python
# Before: [System] [Old-1] [Old-2] [Recent-1] [Recent-2] [Latest-User]
# Crop TOP 2 messages
# After:  [System] [Recent-1] [Recent-2] [Latest-User]
```

### BOTTOM Cropping  
Remove recent messages (except latest user message):
```python
# Before: [System] [Old-1] [Old-2] [Recent-1] [Recent-2] [Latest-User]
# Crop BOTTOM 2 messages  
# After:  [System] [Old-1] [Old-2] [Latest-User]
```

## Smart Context Cropper Tool

### Tool Definition
```python
{
    "name": "smart_context_cropper",
    "description": "Crop conversation history with safety guarantees",
    "parameters": {
        "need_user_approve": "Whether to require user approval",
        "crop_direction": "Direction: 'top' or 'bottom'", 
        "crop_amount": "Number of messages to remove",
        "deleted_messages_summary": "Summary of removed content"
    }
}
```

### Usage Examples

**Scenario 1**: Clean up debugging logs
```
AI: I found the issue after several attempts. Let me clean up the debugging history.
<smart_context_cropper>
  need_user_approve: false
  crop_direction: bottom
  crop_amount: 5
  deleted_messages_summary: "Removed 5 debugging attempts with error logs. Issue was resolved by fixing the database connection string."
</smart_context_cropper>
```

**Scenario 2**: Focus on current task
```
User: Let's crop the discussion about previous features and focus on the current implementation.
AI: I'll crop the previous discussion to focus on your current task.
<smart_context_cropper>
  need_user_approve: true
  crop_direction: top  
  crop_amount: 8
  deleted_messages_summary: "Removed discussion about feature A and B. Current focus: implementing feature C with authentication."
</smart_context_cropper>
```

## Technical Implementation

### SmartContextCropper Tool
[`SmartContextCropper`](src/tools/smart_context_cropper.py):

```python
def execute(self, need_user_approve, crop_direction, crop_amount, deleted_messages_summary):
    """Execute smart context cropping with safety checks"""
    
    # Validate parameters
    # Apply safety protections  
    # Perform cropping operation
    # Update conversation state
```

### Safety Mechanisms
- **User message protection**: Latest user message never removed
- **System message protection**: System prompts always preserved
- **Approval flow**: Dangerous operations require confirmation
- **Validation**: Parameter validation prevents invalid operations

## Integration with Existing Features

### Works with Chapter 4 Features
- **Auto compression**: Smart cropping works alongside automatic compression
- **Cost tracking**: Cropped messages still counted for cost calculation
- **History management**: Integrates with existing history management system

### Enhanced User Experience
```
🎯 Smart cropping: Removed 3 messages from TOP
📝 Summary: Cleaned up initial setup discussion. Focus: deployment configuration
💬 Context: 2,100/8,192 tokens (26%) 💰 Session: $0.018
```

## Use Cases

- **Long debugging sessions**: Remove resolved issues to focus on current problems
- **Topic transitions**: Clean context when switching to unrelated topics  
- **Performance optimization**: Strategic removal for faster processing
- **Context focus**: Maintain relevant information while removing distractions

## Benefits

- **Precision**: Exact control over what gets removed
- **Safety**: Built-in protections prevent accidental data loss
- **Flexibility**: Works for both automated and manual context management
- **Performance**: Immediate optimization without restarting conversations

## Next Steps

→ **Chapter 6**: Add structured task management with the TodoWrite tool for complex workflow organization.
