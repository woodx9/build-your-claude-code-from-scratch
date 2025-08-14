# QuickStar - ReAct Agent

[中文版本](./README_zh.md)

A ReAct (Reasoning and Acting) based AI agent system supporting tool calling and user interaction.

## System Architecture

![ReAct Architecture](./images/ReAct_architect.png)

The ReAct (Reasoning and Acting) architecture implements intelligent agents through the following core workflow:

1. **Think**: AI model receives input and performs reasoning
2. **Act**: Calls appropriate tools based on reasoning results
3. **Observe**: Gets tool execution results as feedback
4. **Iterate**: Feeds observation results into the next round of thinking, forming a complete reasoning-action loop

This architecture enables AI agents to maintain coherent reasoning chains in complex tasks and interact with external environments through tool calls.

## Core Components

### Conversation Manager

![Conversation Sequence](./images/conversation.png)

[`Conversation`](src/core/conversation.py) is the core controller of the system, designed with singleton pattern:

- **Recursive Message Handling**: Implements continuous conversation loops through `recursive_message_handling()`
- **Tool Call Detection**: Automatically identifies tool call requests in AI responses
- **User Approval Mechanism**: Dangerous operations require explicit user confirmation
- **Error Handling**: Complete exception catching and recovery mechanisms

Key workflow:
1. Send message to AI model
2. Check if response contains tool calls
3. If approval needed, wait for user confirmation
4. Execute tool and feed results back to AI
5. Recursively continue conversation

### ToolManager

[`ToolManager`](src/tools/tool_manager.py) handles tool registration, description, and execution:

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

# Run the program
quickstar
```

## Configuration

API configuration in [`APIClient`](src/core/api_client.py):
- Uses OpenRouter as API gateway
- Default model: Claude Sonnet 4
- Supports custom API Key and Base URL

The core idea of this framework is to let AI "think" (through conversation) and "act" (through tool calls), and require user confirmation when executing potentially risky operations, implementing a safe and controllable AI agent system.
