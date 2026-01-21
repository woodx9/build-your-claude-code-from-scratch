# Chapter 7: Sub-Agent Architecture

[中文版本](./README_zh.md)

## What's New in Chapter 7

Chapter 7 implements a sub-agent architecture that allows the main agent to delegate complex tasks to specialized sub-agents:

### 🤖 Key Components Added

#### 1. Task Tool (`src/tools/task.py`)
- **Purpose**: Delegates complex tasks to specialized sub-agents
- **Function**: `async def act(self, description, prompt, subagent_type)`
- **Sub-agent types**: `general-purpose` for research, code search, multi-step analysis
- **Usage**: Main agent calls Task tool → Sub-agent executes autonomously → Returns results

#### 2. SubagentManager (`src/tools/subagent/subagent_manager.py`)
- **Purpose**: Manages sub-agent lifecycle and execution
- **Function**: `async def create_and_run_subagent(self, system_prompt, user_input)`
- **Features**: Creates isolated conversation context, manages execution, collects results

#### 3. Conversation Updates (`src/core/conversation.py`)
- **New method**: `async def start_task(self, task_system_prompt, user_input)`
- **Task depth tracking**: `_task_depth` counter tracks nesting level for nested sub-agent support
- **Integration**: Sub-agents run in isolated conversation sessions

#### 4. HistoryManager Extensions (`src/core/history/history_manager.py`)
- **New methods**: `start_new_chat()` and `finish_chat_get_response()`
- **Function**: Manages separate conversation histories for each sub-agent
- **Isolation**: Each sub-agent gets its own message history stack

### 🔄 Architecture Changes

#### Async Tool System
- **BaseAgent → BaseTool**: Renamed for clarity
- **All tools converted to async**: `async def act(...)` for proper concurrency
- **Tools updated**: CmdRunner, SmartContextCropper, TodoWrite, Task
- **ToolManager**: Updated to handle async tool execution

#### Task Delegation Flow
```
User Request → Main Agent → Task Tool → SubagentManager → New Conversation → Sub-Agent Execution → Result Collection → Main Agent
```

### 💡 How It Works

1. **Task Creation**: Main agent identifies complex tasks requiring delegation
2. **Sub-agent Spawn**: Task tool creates new conversation context with specialized system prompt
3. **Autonomous Execution**: Sub-agent runs independently with full tool access
4. **Result Return**: Sub-agent completes task and returns structured response
5. **Integration**: Main agent receives results and continues workflow

### 🔗 Nested Sub-Agent Support

Sub-agents can delegate tasks to their own sub-agents, creating a hierarchy:

```
Main Agent (_task_depth = 0)
  └─► Sub-agent (_task_depth = 1)
       └─► Sub-sub-agent (_task_depth = 2)
       ◄─┘ returns (_task_depth = 1)
  ◄─┘ returns (_task_depth = 0)
```

**Implementation Details**:
- `_task_depth` counter replaces simple boolean flag for proper nesting
- Incremented when entering a task, decremented when exiting
- Prevents user input prompts in nested scenarios
- History stack (`messages_history`) maintains separate context for each nesting level

### 🚀 Benefits

- **Specialization**: Sub-agents focus on specific task domains
- **Concurrency**: Multiple sub-agents can run simultaneously
- **Isolation**: Each task gets dedicated context and resources
- **Scalability**: Complex workflows decomposed into manageable units
