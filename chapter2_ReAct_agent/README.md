# Chapter 2: ReAct Agent Architecture

[中文版本](./README_zh.md)

## What's New in Chapter 2

Building on Chapter 1's tool calling foundations, Chapter 2 introduces a complete **ReAct (Reasoning and Acting) agent system** with:

- **Recursive conversation handling** for continuous AI interactions
- **Tool execution framework** with safety controls
- **User approval system** for dangerous operations
- **Singleton conversation manager** for state management

## ReAct Architecture

![ReAct Architecture](./images/ReAct_architect.png)

The ReAct pattern implements intelligent agents through:

1. **Think**: AI receives input and performs reasoning
2. **Act**: Calls tools based on reasoning results  
3. **Observe**: Gets tool execution feedback
4. **Iterate**: Feeds observations into next reasoning cycle

## Conversation Flow Architecture

![Conversation Sequence](./images/conversation.png)

The conversation flow diagram illustrates the sophisticated message handling mechanism that powers the ReAct agent system. This architecture enables seamless integration between human users, AI reasoning, and tool execution through a carefully orchestrated sequence of interactions.

### Detailed Flow Analysis

**Phase 1: User Initiation**
- User submits a message through the interface
- [`Conversation`](src/core/conversation.py) singleton receives and validates the input
- Message is added to conversation history for context preservation

**Phase 2: AI Processing & Decision Making**
- User message sent to AI model via [`APIClient`](src/core/api_client.py)
- AI performs reasoning and determines if tool calling is required
- If tools needed: AI generates structured tool call requests
- If no tools: AI provides direct response to user

**Phase 3: Tool Call Detection & Execution**
- [`ToolManager`](src/tools/tool_manager.py) detects tool calls in AI response
- System checks if tool requires user approval (safety mechanism)
- If approved: Tool execution via appropriate [`BaseAgent`](src/tools/base_agent.py) implementation
- Tool results captured and formatted for AI consumption

**Phase 4: Result Integration & Iteration**
- Tool results added to conversation context as "tool" role messages
- Enhanced context sent back to AI for result interpretation
- AI processes tool outputs and provides final user-facing response
- **Recursive continuation**: If AI determines more tools needed, cycle repeats

**Phase 5: Response Delivery**
- Final AI response presented to user
- Conversation state updated and preserved for next interaction
- System ready for subsequent user inputs

### Key Implementation Features

- **Singleton Pattern**: Ensures consistent conversation state across interactions
- **Recursive Message Handling**: Enables complex multi-step tool chains
- **Safety Controls**: User approval gates for potentially dangerous operations
- **Context Preservation**: Complete conversation history maintained for coherent interactions
- **Error Recovery**: Robust exception handling at each phase

This architecture forms the foundation for all advanced features introduced in subsequent chapters.


## Core Components

### Conversation Manager
[`Conversation`](src/core/conversation.py) - Controls the ReAct loop:

```python
def recursive_message_handling(self, user_message):
    """Implements continuous Think-Act-Observe cycles"""
    # Send message to AI → Check for tool calls → Execute → Repeat
```

**Key Features**:
- Recursive message processing for multi-turn interactions
- Automatic tool call detection in AI responses
- Safety controls requiring user approval for dangerous operations
- Complete error handling and recovery

### Tool Management System
[`ToolManager`](src/tools/tool_manager.py) - Handles tool lifecycle:

- **Registration**: Centralized tool inventory
- **Schema Generation**: Provides JSON Schema for AI consumption
- **Execution Proxy**: Routes tool calls to implementations

### Tool Implementation
All tools inherit from [`BaseAgent`](src/tools/base_agent.py):

- **CmdRunner**: System command execution with timeout and approval controls

## Example Interaction Flow

```
User: "List files in the current directory"
     ↓
AI: "I'll list the files using the ls command"
     ↓
System: [Detects tool call] → [Requests approval] → [Executes command]
     ↓
AI: "Here are the files: [results]"
```

## Architecture Benefits

- **Safety**: User approval prevents dangerous operations
- **Extensibility**: Easy to add new tools via inheritance
- **Reliability**: Comprehensive error handling and state management
- **Transparency**: Clear reasoning chain visibility

## Next Steps

→ **Chapter 3**: Add real-time streaming output to enhance user experience during AI interactions.
