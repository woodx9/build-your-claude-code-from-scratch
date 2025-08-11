# QuickStar - History Control Agent

一个基于 ReAct（Reasoning and Acting）模式的 AI 代理系统，支持**实时流式输出**、**智能历史管理**、工具调用和用户交互。

## 🚀 Chapter4 主要更新

### 1. 智能历史管理与压缩

Chapter4 的核心升级是**智能历史管理和压缩**功能：
- 🧠 **自动压缩**：当上下文窗口使用率超过阈值时，自动压缩历史对话
- 📊 **Token 使用监控**：实时显示当前上下文窗口使用率百分比
- 🔄 **多会话压缩**：智能删除最旧的对话会话，保留系统消息和最新对话
- ✂️ **单会话压缩**：在单个会话中删除部分中间的助手和工具响应
- 💾 **历史记录管理**：统一管理对话历史，支持分层存储

#### 🎯 使用体验对比

**Chapter3（无历史管理）**
```
🤖 [长对话后] 抱歉，上下文过长，请重新开始对话...
```

**Chapter4（智能历史管理）✨**
```
🤖 历史上下文过长，正在压缩中...
🤖 (context window: 45.2%) 已优化上下文，继续对话...
```

### 2. Token 使用量跟踪

#### 📈 实时监控功能
- **智能阈值管理**：可配置的压缩触发阈值（默认80%）
- **使用率显示**：每次API调用后显示当前上下文窗口使用百分比
- **成本控制**：帮助用户了解和控制API使用成本
- **性能优化**：避免因上下文过长导致的响应延迟

#### 🔧 配置选项
```env
# 模型最大token数（单位：k）
MODEL_MAX_TOKENS=200
# 压缩触发阈值（0.8 = 80%）
COMPRESS_THRESHOLD=0.8
```

### 3. 历史管理器架构

#### 🏗️ 新增组件
- **HistoryManager**：核心历史管理类
  - `add_message()` - 添加消息到历史记录
  - `update_token_usage()` - 更新token使用情况
  - `auto_messages_compression()` - 自动执行压缩
  - `get_current_messages()` - 获取当前消息列表

#### 🎨 压缩策略
1. **多会话压缩**：
   - 保留系统消息
   - 删除最旧的完整对话会话
   - 保留最近的对话内容
   - 添加压缩通知消息

2. **单会话压缩**：
   - 保留用户输入和系统消息
   - 删除部分中间的助手/工具响应
   - 保留最新的几条消息
   - 添加压缩说明

### 4. API 客户端增强

#### ⚡ Token 使用量集成
- **流式模式增强**：在流式响应中包含token使用统计
- **返回值扩展**：API调用返回消息和token使用情况的元组
- **使用量追踪**：自动收集并传递token使用数据

```python
# 新的API返回格式
message, token_usage = api_client.get_completion(params)
```

## 系统架构

![ReAct架构图](./images/ReAct_architect.png)

ReAct（Reasoning and Acting）架构通过以下核心流程实现智能代理：

1. **思考（Think）**：AI 模型接收输入并进行推理
2. **行动（Act）**：基于推理结果调用相应工具
3. **观察（Observe）**：获取工具执行结果作为反馈
4. **历史管理（Manage）**：智能压缩和管理对话历史 **[Chapter4 新增]**
5. **循环迭代**：将观察结果输入下一轮思考，形成完整的推理-行动循环

这种架构使 AI 代理能够在复杂任务中保持连贯的推理链，并通过工具调用与外部环境交互，同时通过智能历史管理确保长对话的高效处理。

## 核心组件

### 🧠 HistoryManager - 智能历史管理器

[`HistoryManager`](src/core/history/history_manager.py) 是 Chapter4 的核心新组件：

**核心功能**：
```python
class HistoryManager:
    def add_message(self, message) -> None
    def update_token_usage(self, token_usage) -> None  
    def auto_messages_compression(self) -> None
    def get_current_messages(self) -> List[Message]
```

**智能压缩逻辑**：
- 监控token使用率，超过阈值自动触发压缩
- 多会话场景：删除最旧的完整对话会话
- 单会话场景：删除部分中间响应，保留关键信息
- 添加压缩通知，确保上下文连贯性

### 🌊 APIClient - 增强版流式API客户端

[`APIClient`](src/core/api_client.py) 现在支持Token追踪：

**标准模式**（返回消息和使用量）：
```python
def get_completion(self, request_params) -> Tuple[Message, TokenUsage]
```

**🆕 流式模式**（包含使用量统计）：
```python
def get_completion_stream(self, request_params) -> Generator[str, None, None]
# 最后yield完整的消息对象，包含token使用量信息
```

流式模式新特性：
- 实时token使用量统计
- 自动包含`stream_options: {"include_usage": True}`
- 在流式响应结束时提供完整的使用量数据

### 💬 Conversation - 历史感知的对话管理器

[`Conversation`](src/core/conversation.py) 集成历史管理：

**🆕 历史管理集成**：
- `messages` 属性现在通过 HistoryManager 提供
- `add_message()` 统一通过历史管理器处理
- 自动压缩检查在每次消息处理前后执行
- Token使用量自动更新到历史管理器

**核心流程增强**：
1. 🔄 发送消息到 AI 模型（流式）
2. 📺 实时显示AI回复内容
3. 📊 显示token使用率
4. 🧠 检查是否需要历史压缩
5. 🔍 检查响应是否包含工具调用
6. ☝️ 如需批准，等待用户确认
7. ⚡ 执行工具并将结果反馈给 AI
8. 🔁 递归继续对话

### ToolManager 工具管理器

[`ToolManager`](src/tools/tool_manager.py) 保持不变，完全兼容历史管理：

- **工具注册**：统一管理所有可用工具
- **描述生成**：为 AI 提供工具的 JSON Schema 描述
- **执行代理**：根据工具名称分发执行请求

### 工具系统

所有工具继承自 [`BaseAgent`](src/tools/base_agent.py)，目前实现了：

- **CmdRunner**：执行系统命令，支持超时控制和用户批准

## 快速开始

```bash
# 安装依赖
pip install -e .

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入实际的API配置和历史管理参数

# 运行程序
quickstar

# 测试历史压缩功能
python test/test_history_compress.py
```

## 🔧 技术实现细节

### 历史压缩算法
```python
def _compress_current_message(self):
    current_messages = self.messages_history[-1]
    user_indices = self._get_user_message_indices(current_messages)
    
    if len(user_indices) > 1:
        # 多会话：删除最旧的会话
        self._compress_multiple_sessions(current_messages, user_indices)
    elif len(user_indices) == 1:
        # 单会话：删除中间响应
        self._compress_single_session(current_messages, user_indices[0])
```

### Token使用量监控
```python
def update_token_usage(self, token_usage):
    usage_percent = 100 * token_usage.total_tokens / self._model_max_tokens
    self._ui_manager.print_info(f"(context window: {usage_percent:.1f}%)")
    
    if usage_percent > self._compress_threshold * 100:
        self.auto_messages_compression()
```

### 流式响应的Token追踪
```python
for chunk in stream:
    if hasattr(chunk, 'usage') and chunk.usage:
        token_usage = chunk.usage  # 收集使用量信息
    elif chunk.choices[0].delta.content:
        yield chunk.choices[0].delta.content  # 流式内容
```

## 🎯 Chapter4 vs Chapter3

| 特性 | Chapter3 | Chapter4 |
|------|----------|----------|
| 响应模式 | ✅ 实时流式 | ✅ 实时流式 |
| 用户体验 | ✅ 即时反馈 | ✅ 即时反馈 |
| 工具调用 | ✅ 流式支持 | ✅ 流式支持 |
| 错误处理 | ✅ 优雅降级 | ✅ 优雅降级 |
| 历史管理 | ❌ 无限制堆积 | 🆕 智能压缩 |
| Token监控 | ❌ 无追踪 | 🆕 实时显示 |
| 长对话支持 | ❌ 容易超限 | 🆕 自动优化 |
| 成本控制 | ❌ 无感知 | 🆕 使用量可见 |
| 上下文优化 | ❌ 手动重启 | 🆕 自动压缩 |

## 🧪 测试覆盖

Chapter4 包含完整的历史管理测试套件：

```bash
# 运行历史压缩测试
python test/test_history_compress.py
```

测试覆盖：
- ✅ 自动压缩触发条件
- ✅ 多会话压缩逻辑
- ✅ 单会话压缩逻辑
- ✅ Token使用量更新
- ✅ 压缩阈值判断

这个框架的核心思想是让 AI 能够"思考"（通过对话）和"行动"（通过工具调用），并且在执行可能有风险的操作时需要用户确认。Chapter4 的智能历史管理进一步解决了长对话中的上下文管理难题，使AI代理能够在保持对话连贯性的同时，有效控制成本和性能，为构建真正实用的AI助手奠定了坚实基础。
