# QuickStar - History Control Agent

[中文版本](./README_zh.md)

A ReAct (Reasoning and Acting) based AI agent system supporting **real-time streaming output**, **intelligent history management**, **cost tracking**, tool calling, and user interaction.

## 🚀 Chapter4 Major Updates

### 1. Intelligent History Management and Compression

Chapter4's core upgrade is the **intelligent history management and compression** functionality:
- 🧠 **Auto Compression**: Automatically compresses conversation history when context window usage exceeds threshold
- 📊 **Token Usage Monitoring**: Real-time display of current context window usage percentage
- 🔄 **Multi-session Compression**: Intelligently removes oldest complete conversation sessions, preserving system messages and recent conversations
- ✂️ **Single-session Compression**: Removes some intermediate assistant/tool responses within a single conversation
- 💾 **History Record Management**: Unified conversation history management with layered storage

### 2. 💰 Cost Tracking System **[NEW]**

#### 📈 Intelligent Cost Monitoring
- **Total Cost Tracking**: Automatically accumulates costs for all API calls
- **Real-time Display**: Shows total cost of current session after each interaction
- **Cost Visibility**: Helps users understand API usage costs in real-time
- **Precise Calculation**: Based on accurate cost information returned by the model

#### 🎯 User Experience Comparison

**Chapter4 (Context window info following, intelligent cost tracking) ✨**
```
🤖 (context window: 45.2%, total cost: $0.05) Optimized context, continuing conversation...
```

### 3. Enhanced Message Format **[NEW]**

#### 🔧 Multi-modal Content Format Support
- **Unified Message Structure**: All message content uses array format, supporting multiple content types
- **Cache Control**: Adds cache markers for latest messages to optimize performance
- **Forward Compatibility**: Maintains full compatibility with existing tools and systems

#### 📝 New Message Format Example
```python
# Old format
{"role": "user", "content": "Hello"}

# New format (supports multi-modal and cache control)
{
    "role": "user", 
    "content": [
        {"type": "text", "text": "Hello", "cache_control": {"type": "ephemeral"}}
    ]
}
```

### 4. Enhanced Token Usage Tracking

#### 📊 Real-time Monitoring Features
- **Intelligent Threshold Management**: Configurable compression trigger threshold (default 80%)
- **Usage Rate Display**: Shows current context window usage percentage and total cost after each API call
- **Cost Control**: Helps users understand and control API usage costs
- **Performance Optimization**: Avoids response delays caused by overly long context

#### 🔧 Configuration Options
```env
# Maximum model tokens (in k)
MODEL_MAX_TOKENS=200
# Compression trigger threshold (0.8 = 80%)
COMPRESS_THRESHOLD=0.8
```

### 5. History Manager Architecture

#### 🏗️ New Components
- **HistoryManager**: Core history management class
  - `add_message()` - Add message to history record
  - `update_token_usage()` - Update token usage
  - `auto_messages_compression()` - Automatically execute compression
  - `get_current_messages()` - Get current message list
  - `current_context_window` - Get current context window usage rate **[NEW]**

#### 🎨 Compression Strategies
1. **Multi-session Compression**:
   - Preserve system messages
   - Remove oldest complete conversation sessions
   - Keep recent conversation content
   - Add compression notification messages

2. **Single-session Compression**:
   - Preserve user input and system messages
   - Remove some intermediate assistant/tool responses
   - Keep latest few messages
   - Add compression explanation

### 6. Enhanced API Client

#### ⚡ Cost Tracking Integration **[NEW]**
- **Cost Accumulation**: Automatically accumulates cost for each API call
- **Total Cost Property**: Access cumulative cost through `total_cost` property
- **Streaming Mode Enhancement**: Includes cost statistics in streaming responses
- **Return Value Extension**: API calls return tuple of message and token usage

```python
# New cost tracking property
api_client.total_cost  # Get total cost

# API return format remains unchanged
message, token_usage = api_client.get_completion(params)
```

The ReAct (Reasoning and Acting) architecture implements intelligent agents through the following core workflow:

1. **Think**: AI model receives input and performs reasoning
2. **Act**: Calls appropriate tools based on reasoning results
3. **Observe**: Gets tool execution results as feedback
4. **Manage**: Intelligently compress and manage conversation history **[Chapter4 New]**
5. **Monitor**: Real-time tracking and display of usage costs **[Chapter4 New]**
6. **Iterate**: Feeds observation results into the next round of thinking, forming a complete reasoning-action loop

This architecture enables AI agents to maintain coherent reasoning chains in complex tasks, interact with external environments through tool calls, ensure efficient handling of long conversations through intelligent history management, help users control usage costs through cost monitoring, and lay a solid foundation for building truly practical AI assistants.

## Core Components

### 🧠 HistoryManager - Intelligent History Manager

[`HistoryManager`](src/core/history/history_manager.py) is Chapter4's core new component:

**Core Functions**:
```python
class HistoryManager:
    def add_message(self, message) -> None
    def update_token_usage(self, token_usage) -> None  
    def auto_messages_compression(self) -> None
    def get_current_messages(self) -> List[Message]
    
    @property
    def current_context_window(self) -> str  # [NEW] Get current window usage rate
```

**Intelligent Compression Logic**:
- Monitors token usage rate, automatically triggers compression when threshold exceeded
- Multi-session scenarios: Remove oldest complete conversation sessions
- Single-session scenarios: Remove some intermediate responses, preserve key information
- Add compression notifications to ensure context continuity

### 🌊 APIClient - Enhanced Streaming API Client

[`APIClient`](src/core/api_client.py) now supports cost tracking:

**Standard Mode** (returns message and usage):
```python
def get_completion(self, request_params) -> Tuple[Message, TokenUsage]
```

**🆕 Streaming Mode** (includes cost statistics):
```python
def get_completion_stream(self, request_params) -> Generator[str, None, None]
# Finally yields complete message object, including token usage and cost info
```

**🆕 Cost Tracking Features**:
- Automatically accumulates all API call costs
- Access total cost through `total_cost` property
- Supports cost statistics for both streaming and standard modes
- Based on accurate cost data returned by the model

### 💬 Conversation - History-aware Conversation Manager

[`Conversation`](src/core/conversation.py) integrates history management and cost display:

**🆕 History Management Integration**:
- `messages` property now provided through HistoryManager
- `add_message()` unified handling through history manager
- Automatic compression checks executed before and after each message processing
- Token usage and cost automatically updated to history manager

**🆕 Message Format Upgrade**:
- All message content uses array format
- Supports multi-modal content (text, images, etc.)
- Automatically adds cache control markers
- Maintains forward compatibility

**Enhanced Core Workflow**:
1. 🔄 Send message to AI model (streaming)
2. 📺 Real-time display of AI reply content
3. 📊 Display token usage rate and total cost **[NEW]**
4. 🧠 Check if history compression needed
5. 🔍 Check if response contains tool calls
6. ☝️ If approval needed, wait for user confirmation
7. ⚡ Execute tool and feed results back to AI
8. 🔁 Recursively continue conversation

### ToolManager

[`ToolManager`](src/tools/tool_manager.py) remains unchanged, fully compatible with history management:

- **Tool Registration**: Unified management of all available tools
- **Description Generation**: Provides JSON Schema descriptions of tools for AI
- **Execution Proxy**: Dispatches execution requests based on tool names

### Tool System

All tools inherit from [`BaseAgent`](src/tools/base_agent.py), currently implementing:

- **CmdRunner**: Executes system commands with timeout control and user approval

## Quick Start

```bash
# Install dependencies
pip install -e .

# Configure environment variables
cp .env.example .env
# Edit .env file, fill in actual API configuration and history management parameters

# Run the program
quickstar

# Test history compression functionality
python test/test_history_compress.py
```

## 🔧 Technical Implementation Details

### Cost Tracking Algorithm **[NEW]**
```python
def get_completion_stream(self, request_params):
    for chunk in stream:
        if hasattr(chunk, 'usage') and chunk.usage:
            cost = getattr(chunk.usage, 'model_extra', {})
            if isinstance(cost, dict):
                self._total_cost += cost.get("cost", 0)
```

### History Compression Algorithm
```python
def _compress_current_message(self):
    current_messages = self.messages_history[-1]
    user_indices = self._get_user_message_indices(current_messages)
    
    if len(user_indices) > 1:
        # Multi-session: Remove oldest session
        self._compress_multiple_sessions(current_messages, user_indices)
    elif len(user_indices) == 1:
        # Single-session: Remove intermediate responses
        self._compress_single_session(current_messages, user_indices[0])
```

### Token Usage Monitoring
```python
@property
def current_context_window(self):
    if not self.history_token_usage or self._model_max_tokens == 0:
        return "0.0"
    return f"{100 * self.history_token_usage[-1].total_tokens / self._model_max_tokens:.1f}"
```

### Cache Control Implementation **[NEW]**
```python
def _get_messages_with_cache_mark(self):
    messages = self._history_manager.get_current_messages()
    if messages and "content" in messages[-1] and messages[-1]["content"]:
        messages[-1]["content"][-1]["cache_control"] = {"type": "ephemeral"}
    return messages
```

## 🎯 Chapter4 vs Chapter3

| Feature | Chapter3 | Chapter4 |
|---------|----------|----------|
| Response Mode | ✅ Real-time streaming | ✅ Real-time streaming |
| User Experience | ✅ Instant feedback | ✅ Instant feedback |
| Tool Calling | ✅ Streaming support | ✅ Streaming support |
| Error Handling | ✅ Graceful degradation | ✅ Graceful degradation |
| History Management | ❌ Unlimited accumulation | 🆕 Intelligent compression |
| Token Monitoring | ❌ No tracking | 🆕 Real-time display |
| Cost Tracking | ❌ No awareness | 🆕 Total cost display |
| Long Conversation Support | ❌ Easy to exceed limits | 🆕 Auto optimization |
| Cost Control | ❌ No awareness | 🆕 Usage visibility |
| Context Optimization | ❌ Manual restart | 🆕 Auto compression |
| Cache Optimization | ❌ No cache | 🆕 Intelligent cache |

## 🧪 Test Coverage

Chapter4 includes complete history management test suite:

```bash
# Run history compression tests
python test/test_history_compress.py
```

Test coverage:
- ✅ Auto compression trigger conditions
- ✅ Multi-session compression logic
- ✅ Single-session compression logic
- ✅ Token usage updates
- ✅ Compression threshold judgment
- ✅ Cost tracking accuracy **[NEW]**
- ✅ Message format conversion **[NEW]**

The core idea of this framework is to let AI "think" (through conversation) and "act" (through tool calls), and require user confirmation when executing potentially risky operations. Chapter4's intelligent history management further solves the context management challenges in long conversations, cost tracking functionality helps users understand API usage costs in real-time, and the new message format lays the foundation for future multi-modal feature expansion, enabling AI agents to effectively control costs and performance while maintaining conversation continuity, laying a solid foundation for building truly practical AI assistants.
