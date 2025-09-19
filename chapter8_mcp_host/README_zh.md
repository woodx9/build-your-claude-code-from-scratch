# 第七章：子智能体架构

[English Version](./README.md)

## 第七章新增功能

第七章实现了子智能体架构，允许主智能体将复杂任务委托给专门的子智能体：

### 🤖 新增核心组件

#### 1. Task 工具 (`src/tools/task.py`)
- **用途**：将复杂任务委托给专门的子智能体
- **函数**：`async def act(self, description, prompt, subagent_type)`
- **子智能体类型**：`general-purpose` 用于研究、代码搜索、多步骤分析
- **使用流程**：主智能体调用Task工具 → 子智能体自主执行 → 返回结果

#### 2. SubagentManager (`src/tools/subagent/subagent_manager.py`)
- **用途**：管理子智能体生命周期和执行
- **函数**：`async def create_and_run_subagent(self, system_prompt, user_input)`
- **功能**：创建隔离的对话上下文，管理执行过程，收集结果

#### 3. Conversation 更新 (`src/core/conversation.py`)
- **新方法**：`async def start_task(self, task_system_prompt, user_input)`
- **任务模式**：`_is_in_task` 标志防止子智能体执行期间的用户输入
- **集成**：子智能体在隔离的对话会话中运行

#### 4. HistoryManager 扩展 (`src/core/history/history_manager.py`)
- **新方法**：`start_new_chat()` 和 `finish_chat_get_response()`
- **功能**：为每个子智能体管理独立的对话历史
- **隔离**：每个子智能体获得自己的消息历史堆栈

### 🔄 架构变更

#### 异步工具系统
- **BaseAgent → BaseTool**：重命名以提高清晰度
- **所有工具转换为异步**：`async def act(...)` 实现适当的并发
- **更新的工具**：CmdRunner、SmartContextCropper、TodoWrite、Task
- **ToolManager**：更新以处理异步工具执行

#### 任务委托流程
```
用户请求 → 主智能体 → Task工具 → SubagentManager → 新对话 → 子智能体执行 → 结果收集 → 主智能体
```

### 💡 工作原理

1. **任务创建**：主智能体识别需要委托的复杂任务
2. **子智能体生成**：Task工具使用专门的系统提示创建新的对话上下文
3. **自主执行**：子智能体独立运行，具有完整的工具访问权限
4. **结果返回**：子智能体完成任务并返回结构化响应
5. **集成**：主智能体接收结果并继续工作流程

### 🚀 优势

- **专业化**：子智能体专注于特定任务领域
- **并发性**：多个子智能体可以同时运行
- **隔离性**：每个任务获得专用的上下文和资源
- **可扩展性**：复杂工作流程分解为可管理的单元
