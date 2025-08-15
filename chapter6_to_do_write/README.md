# QuickStar - Smart Context Agent

[中文版本](./README_zh.md)

A ReAct (Reasoning and Acting) based AI agent system supporting **real-time streaming output**, **intelligent history management**, **cost tracking**, **smart context cropping**, tool calling, and user interaction.

## 🚀 Chapter5 Major Updates

### 1. Smart Context Cropping Feature **[NEW]**

Chapter5's core new feature is **Smart Context Cropping**, providing advanced users with fine-grained message management control:
- 🎯 **Precise Cropping**: Supports cropping specified number of messages from TOP or BOTTOM
- 🔒 **Safety Guarantee**: Strictly protects latest user messages and system messages from accidental cropping
- 📝 **Cropping Summary**: Supports providing concise summaries for cropped content to maintain context continuity
- 🛠️ **New Tool**: SmartContextCropper tool, seamlessly integrated with existing tool chain
- ⚡ **Immediate Effect**: Cropping operations take effect immediately, optimizing long conversation performance

#### 🎛️ Cropping Strategies
```python
# Crop from top - remove oldest N messages (preserve system messages)
crop_direction: "top", crop_amount: 3

# Crop from bottom - remove most recent N messages (protect latest user message)  
crop_direction: "bottom", crop_amount: 2
```

### 2. Enhanced User Interaction Experience **[NEW]**

#### 🗣️ Smart Rejection Reason Capture
- **Reason Collection**: When users reject tool execution, actively asks and records specific reasons
- **Context Understanding**: AI can understand rejection reasons and make more appropriate follow-up responses
- **Interaction Optimization**: From simple "user rejected" to detailed rejection reasons and suggestions

#### 💬 User Experience Comparison

**Chapter4 (Simple Rejection):**
```
🤖 Need to execute command: rm important_file.txt
❌ User rejected tool execution
```

**Chapter5 (Smart Reason Capture):**
```
🤖 Need to execute command: rm important_file.txt  
❌ User rejected: "This file is still needed, please use backup file instead"
🤖 Understood, I'll help you operate the backup file instead of the original file
```

### 3. Architecture Optimization and Stability Improvements

#### 🏗️ HistoryManager Singleton Pattern
- **State Consistency**: Global single history manager instance, avoiding state conflicts
- **Memory Optimization**: Reduces duplicate instance creation, improves performance
- **Thread Safety**: Ensures data consistency in multi-threaded environments

#### 🛡️ Enhanced Error Handling
- **Unified Tool Exception Handling**: ToolManager uniformly catches and handles tool execution exceptions
- **Clear Error Identification**: CmdRunner error messages add "cmd_runner" prefix for easier debugging
- **Defensive Programming**: Prevents single tool exceptions from causing entire system crashes

#### 🔧 Code Quality Improvements
- **Abstract Method Enforcement**: BaseAgent adds abstract method constraints to ensure tool implementation standards
- **Type Safety**: New Crop_Direction enum provides type-safe cropping direction control
- **Boundary Checking**: Strict cropping parameter validation and boundary protection

### 4. Developer Experience Improvements

#### 🐛 Enhanced Debug Support
- **VSCode Configuration**: New chapter5-specific debug launch configuration
- **Error Message Optimization**: More detailed and specific error prompt messages
- **Tool Description Completion**: Improved tool description documentation for better development efficiency

### 5. New Core Tool: SmartContextCropper

#### 🔧 SmartContextCropper - Smart Context Cropping Tool

[`SmartContextCropper`](src/tools/smart_context_cropper.py) is Chapter5's flagship new tool:

**🎯 Core Functions**:
```python
def act(self, crop_direction: Crop_Direction, crop_amount: int, deleted_messages_summary: str)
```

**🛡️ Safety Guarantees**:
- Automatically protects latest user messages from being cropped
- Preserves all system messages (system role)
- Strict boundary checking prevents over-cropping

**📋 Tool Parameters**:
- `crop_direction`: "top" | "bottom" - Cropping direction
- `crop_amount`: Positive integer - Number of messages to crop  
- `deleted_messages_summary`: Brief summary of deleted content
- `need_user_approve`: Whether user approval needed (default: true)

#### ⚡ Usage Scenarios

**1. Debug Conversation Cleanup**:
```bash
# Keep problem description and final solution, clean up intermediate failed attempts
smart_context_cropper(crop_direction="bottom", crop_amount=5, 
    deleted_messages_summary="Cleared 5 failed debug attempts, keeping core problem and solution")
```

**2. Long Conversation Optimization**:
```bash  
# Clean up early unrelated conversations, focus on current task
smart_context_cropper(crop_direction="top", crop_amount=8,
    deleted_messages_summary="Removed early data analysis conversations, currently focused on API development")
```

**3. Performance Optimization**:
```bash
# Proactively clean when context window approaches limit
smart_context_cropper(crop_direction="top", crop_amount=3,
    deleted_messages_summary="Cleaned history messages to optimize performance, keeping current project core discussion")
```

#### 🔍 Smart Judgment Logic

Tool has built-in smart judgment mechanism:
- **Auto Assessment**: Analyzes relevance between cropped content and current task
- **User Confirmation**: Proactively requests user approval when uncertain
- **Summary Generation**: Generates concise summaries for important deleted content
- **Context Protection**: Ensures key context information is not lost

## 🎯 Version Comparison

| Feature | Chapter3 | Chapter4 | Chapter5 |
|---------|----------|----------|----------|
| Response Mode | ✅ Real-time streaming | ✅ Real-time streaming | ✅ Real-time streaming |
| History Management | ❌ Unlimited accumulation | 🆕 Intelligent compression | 🆕 Intelligent compression |
| **Smart Cropping** | ❌ Not supported | ❌ Not supported | 🆕 **Precise cropping** |
| **User Interaction** | ❌ Simple rejection | ❌ Simple rejection | 🆕 **Reason capture** |
| **Architecture Stability** | ❌ Basic architecture | ✅ History management | 🆕 **Singleton pattern** |
| **Error Handling** | ❌ Basic handling | ✅ Improved handling | 🆕 **Unified exceptions** |

## 🧪 Test Coverage

Chapter5 includes complete smart cropping and history management test suite:

```bash
# Run history compression tests
python test/test_history_compress.py

# Run smart cropping tests [NEW]
python test/test_crop_message.py
```

Test coverage:
- ✅ Auto compression trigger conditions
- ✅ Multi-session compression logic
- ✅ Single-session compression logic
- ✅ Token usage updates
- ✅ **Smart cropping functionality** **[NEW]**
- ✅ **TOP/BOTTOM cropping strategies** **[NEW]**
- ✅ **User message protection mechanism** **[NEW]**
- ✅ **Boundary check validation** **[NEW]**

## Summary

The core idea of this framework is to let AI "think" (through conversation) and "act" (through tool calls), and require user confirmation when executing potentially risky operations. Chapter5's smart cropping functionality provides users with fine-grained context control capabilities, enhanced user interaction experience enables AI to better understand user intentions, through singleton pattern and unified exception handling, the system architecture is more stable and reliable, laying a solid foundation for building truly practical AI assistants.
