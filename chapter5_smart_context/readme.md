# QuickStar - History Control Agent

一个基于 ReAct（Reasoning and Acting）模式的 AI 代理系统，支持**实时流式输出**、**智能历史管理**、**成本跟踪**、工具调用和用户交互。

## 🚀 Chapter5 主要更新

### 1. 智能上下文裁剪功能 **[NEW]**

Chapter5 的核心新特性是**智能上下文裁剪**，为高级用户提供精细的消息管理控制：
- 🎯 **精准裁剪**：支持从顶部(TOP)或底部(BOTTOM)裁剪指定数量的消息
- 🔒 **安全保证**：严格保护最新用户消息和系统消息不被意外裁剪
- 📝 **裁剪总结**：支持为被裁剪内容提供简洁总结，保持上下文连贯性
- 🛠️ **新增工具**：SmartContextCropper工具，与现有工具链无缝集成
- ⚡ **即时生效**：裁剪操作立即生效，优化长对话性能

#### 🎛️ 裁剪策略
```python
# 从顶部裁剪 - 删除最早的N条消息(保留系统消息)
crop_direction: "top", crop_amount: 3

# 从底部裁剪 - 删除最近的N条消息(保护最新用户消息)  
crop_direction: "bottom", crop_amount: 2
```

### 2. 增强的用户交互体验 **[NEW]**

#### 🗣️ 智能拒绝原因捕获
- **原因收集**：当用户拒绝工具执行时，主动询问并记录具体原因
- **上下文理解**：AI能理解拒绝原因，做出更合适的后续响应
- **交互优化**：从简单的"用户拒绝"到详细的拒绝理由和建议

#### 💬 用户体验对比

**Chapter4（简单拒绝）:**
```
🤖 需要执行命令: rm important_file.txt
❌ 用户拒绝了工具执行
```

**Chapter5（智能原因捕获）:**
```
🤖 需要执行命令: rm important_file.txt  
❌ 用户拒绝: "这个文件还需要，请改用备份文件"
🤖 理解了，我会帮您操作备份文件而不是原文件
```

### 4. 开发者体验改进

#### 🐛 调试支持增强

### 4. 新增核心工具：SmartContextCropper **[Chapter5 重要特性]**

#### 🔧 SmartContextCropper - 智能上下文裁剪工具

[`SmartContextCropper`](src/tools/smart_context_cropper.py) 是 Chapter5 的标志性新工具：

**🎯 核心功能**：
```python
def act(self, crop_direction: Crop_Direction, crop_amount: int, deleted_messages_summary: str)
```

**🛡️ 安全保证**：
- 自动保护最新用户消息，绝不被裁剪
- 保留所有系统消息(system role)
- 严格边界检查，防止过度裁剪

**📋 工具参数**：
- `crop_direction`: "top" | "bottom" - 裁剪方向
- `crop_amount`: 正整数 - 裁剪消息数量  
- `deleted_messages_summary`: 被删除内容的简要总结
- `need_user_approve`: 是否需要用户确认 (默认: true)

#### 🎨 裁剪策略详解

**TOP 裁剪（从顶部开始）**：
```python
# 原始对话
[system] 你是一个编程助手
[user] 写一个Python函数
[assistant] 这里是基本版本...
[user] 请优化性能
[assistant] 这里是优化版本...

# crop_direction="top", crop_amount=2 执行后
[system] 你是一个编程助手  # 系统消息保留
[user] 请优化性能            # 最新用户消息保留  
[assistant] 这里是优化版本...
```

**BOTTOM 裁剪（从底部开始）**：
```python
# 原始对话
[system] 你是调试专家
[user] 诊断API延迟问题
[assistant] 我会探索几个假设...
[assistant] 尝试1: GC调优无效...
[assistant] 尝试2: 数据库索引无改善...
[assistant] 尝试3: 批处理作业相关性不确定...

# crop_direction="bottom", crop_amount=3 执行后
[system] 你是调试专家
[user] 诊断API延迟问题      # 最新用户消息保护
[assistant] 我会探索几个假设...
# deleted_messages_summary: "失败总结：(1)GC调优无效...(2)数据库假设错误...(3)批处理作业结论不确定。下一步：检查00:00定时任务和数据库维护窗口"
```

#### ⚡ 使用场景

**1. 调试对话清理**：
```bash
# 保留问题描述和最终解决方案，清理中间失败尝试
smart_context_cropper(crop_direction="bottom", crop_amount=5, 
    deleted_messages_summary="清理了5次失败的调试尝试，保留核心问题和解决方案")
```

**2. 长对话优化**：
```bash  
# 清理早期不相关的对话，专注当前任务
smart_context_cropper(crop_direction="top", crop_amount=8,
    deleted_messages_summary="移除了早期关于数据分析的对话，当前专注于API开发")
```

**3. 性能优化**：
```bash
# 当上下文窗口接近限制时主动清理
smart_context_cropper(crop_direction="top", crop_amount=3,
    deleted_messages_summary="清理历史消息以优化性能，保留当前项目核心讨论")
```

#### 🔍 智能判断逻辑

工具内置智能判断机制：
- **自动评估**：分析被裁剪内容与当前任务的相关性
- **用户确认**：不确定时主动请求用户批准
- **总结生成**：为重要被删内容生成简洁总结
- **上下文保护**：确保关键上下文信息不丢失

- **VSCode配置**：新增chapter5专用的调试启动配置
- **错误信息优化**：更详细和具体的错误提示信息
- **工具描述完善**：改进工具描述文档，提升开发效率

### 3. 架构优化与稳定性提升

#### 🏗️ HistoryManager 单例模式
- **状态一致性**：全局单一历史管理器实例，避免状态冲突
- **内存优化**：减少重复实例创建，提高性能
- **线程安全**：确保多线程环境下的数据一致性

#### 🛡️ 增强的错误处理
- **工具异常统一处理**：ToolManager中统一捕获和处理工具执行异常
- **明确的错误标识**：CmdRunner错误信息添加"cmd_runner"前缀便于调试
- **防御性编程**：防止单个工具异常导致整个系统崩溃

#### 🔧 代码质量提升
- **抽象方法强化**：BaseAgent添加抽象方法约束，确保工具实现规范
- **类型安全**：新增Crop_Direction枚举，提供类型安全的裁剪方向控制
- **边界检查**：严格的裁剪参数验证和边界保护

### 4. 开发者体验改进

#### 🐛 调试支持增强

### 4. 新增核心工具：SmartContextCropper **[Chapter5 重要特性]**

#### 🔧 SmartContextCropper - 智能上下文裁剪工具

[`SmartContextCropper`](src/tools/smart_context_cropper.py) 是 Chapter5 的标志性新工具：

**🎯 核心功能**：
```python
def act(self, crop_direction: Crop_Direction, crop_amount: int, deleted_messages_summary: str)
```

**🛡️ 安全保证**：
- 自动保护最新用户消息，绝不被裁剪
- 保留所有系统消息(system role)
- 严格边界检查，防止过度裁剪

**📋 工具参数**：
- `crop_direction`: "top" | "bottom" - 裁剪方向
- `crop_amount`: 正整数 - 裁剪消息数量  
- `deleted_messages_summary`: 被删除内容的简要总结
- `need_user_approve`: 是否需要用户确认 (默认: true)

#### 🎨 裁剪策略详解

**TOP 裁剪（从顶部开始）**：
```python
# 原始对话
[system] 你是一个编程助手
[user] 写一个Python函数
[assistant] 这里是基本版本...
[user] 请优化性能
[assistant] 这里是优化版本...

# crop_direction="top", crop_amount=2 执行后
[system] 你是一个编程助手  # 系统消息保留
[user] 请优化性能            # 最新用户消息保留  
[assistant] 这里是优化版本...
```

**BOTTOM 裁剪（从底部开始）**：
```python
# 原始对话
[system] 你是调试专家
[user] 诊断API延迟问题
[assistant] 我会探索几个假设...
[assistant] 尝试1: GC调优无效...
[assistant] 尝试2: 数据库索引无改善...
[assistant] 尝试3: 批处理作业相关性不确定...

# crop_direction="bottom", crop_amount=3 执行后
[system] 你是调试专家
[user] 诊断API延迟问题      # 最新用户消息保护
[assistant] 我会探索几个假设...
# deleted_messages_summary: "失败总结：(1)GC调优无效...(2)数据库假设错误...(3)批处理作业结论不确定。下一步：检查00:00定时任务和数据库维护窗口"
```

#### ⚡ 使用场景

**1. 调试对话清理**：
```bash
# 保留问题描述和最终解决方案，清理中间失败尝试
smart_context_cropper(crop_direction="bottom", crop_amount=5, 
    deleted_messages_summary="清理了5次失败的调试尝试，保留核心问题和解决方案")
```

**2. 长对话优化**：
```bash  
# 清理早期不相关的对话，专注当前任务
smart_context_cropper(crop_direction="top", crop_amount=8,
    deleted_messages_summary="移除了早期关于数据分析的对话，当前专注于API开发")
```

**3. 性能优化**：
```bash
# 当上下文窗口接近限制时主动清理
smart_context_cropper(crop_direction="top", crop_amount=3,
    deleted_messages_summary="清理历史消息以优化性能，保留当前项目核心讨论")
```

#### 🔍 智能判断逻辑

工具内置智能判断机制：
- **自动评估**：分析被裁剪内容与当前任务的相关性
- **用户确认**：不确定时主动请求用户批准
- **总结生成**：为重要被删内容生成简洁总结
- **上下文保护**：确保关键上下文信息不丢失

- **VSCode配置**：新增chapter5专用的调试启动配置
- **错误信息优化**：更详细和具体的错误提示信息
- **工具描述完善**：改进工具描述文档，提升开发效率


## 🚀 Chapter5 主要更新

### 1. 智能上下文裁剪功能

Chapter5 新增了**智能上下文裁剪功能**，为高级用户提供更精细的上下文管理控制：
- 🎯 **精准裁剪**：支持从顶部或底部裁剪指定数量的消息
- 🔒 **安全保证**：保证最新用户消息和系统消息不被裁剪
- 📝 **裁剪总结**：支持为裁剪掉的内容提供简洁总结
- 📦 **单例模式**：历史管理器采用单例模式，确保状态一致性
- 🔧 **工具集成**：新增 SmartContextCropper 工具，与现有工具链无缝集成

### 2. 增强的错误处理 **[NEW]**

#### 🔧 工具执行错误处理
- **统一异常捕获**：在 ToolManager 中统一处理工具执行异常
- **错误信息强化**：CmdRunner 添加明确的错误前缀标识
- **防御性编程**：防止工具执行异常导致系统崩溃

### 4. 开发者体验改进

#### 🐛 调试支持增强

### 4. 新增核心工具：SmartContextCropper **[Chapter5 重要特性]**

#### 🔧 SmartContextCropper - 智能上下文裁剪工具

[`SmartContextCropper`](src/tools/smart_context_cropper.py) 是 Chapter5 的标志性新工具：

**🎯 核心功能**：
```python
def act(self, crop_direction: Crop_Direction, crop_amount: int, deleted_messages_summary: str)
```

**🛡️ 安全保证**：
- 自动保护最新用户消息，绝不被裁剪
- 保留所有系统消息(system role)
- 严格边界检查，防止过度裁剪

**📋 工具参数**：
- `crop_direction`: "top" | "bottom" - 裁剪方向
- `crop_amount`: 正整数 - 裁剪消息数量  
- `deleted_messages_summary`: 被删除内容的简要总结
- `need_user_approve`: 是否需要用户确认 (默认: true)

#### 🎨 裁剪策略详解

**TOP 裁剪（从顶部开始）**：
```python
# 原始对话
[system] 你是一个编程助手
[user] 写一个Python函数
[assistant] 这里是基本版本...
[user] 请优化性能
[assistant] 这里是优化版本...

# crop_direction="top", crop_amount=2 执行后
[system] 你是一个编程助手  # 系统消息保留
[user] 请优化性能            # 最新用户消息保留  
[assistant] 这里是优化版本...
```

**BOTTOM 裁剪（从底部开始）**：
```python
# 原始对话
[system] 你是调试专家
[user] 诊断API延迟问题
[assistant] 我会探索几个假设...
[assistant] 尝试1: GC调优无效...
[assistant] 尝试2: 数据库索引无改善...
[assistant] 尝试3: 批处理作业相关性不确定...

# crop_direction="bottom", crop_amount=3 执行后
[system] 你是调试专家
[user] 诊断API延迟问题      # 最新用户消息保护
[assistant] 我会探索几个假设...
# deleted_messages_summary: "失败总结：(1)GC调优无效...(2)数据库假设错误...(3)批处理作业结论不确定。下一步：检查00:00定时任务和数据库维护窗口"
```

#### ⚡ 使用场景

**1. 调试对话清理**：
```bash
# 保留问题描述和最终解决方案，清理中间失败尝试
smart_context_cropper(crop_direction="bottom", crop_amount=5, 
    deleted_messages_summary="清理了5次失败的调试尝试，保留核心问题和解决方案")
```

**2. 长对话优化**：
```bash  
# 清理早期不相关的对话，专注当前任务
smart_context_cropper(crop_direction="top", crop_amount=8,
    deleted_messages_summary="移除了早期关于数据分析的对话，当前专注于API开发")
```

**3. 性能优化**：
```bash
# 当上下文窗口接近限制时主动清理
smart_context_cropper(crop_direction="top", crop_amount=3,
    deleted_messages_summary="清理历史消息以优化性能，保留当前项目核心讨论")
```

#### 🔍 智能判断逻辑

工具内置智能判断机制：
- **自动评估**：分析被裁剪内容与当前任务的相关性
- **用户确认**：不确定时主动请求用户批准
- **总结生成**：为重要被删内容生成简洁总结
- **上下文保护**：确保关键上下文信息不丢失

- **VSCode配置**：新增chapter5专用的调试启动配置
- **错误信息优化**：更详细和具体的错误提示信息
- **工具描述完善**：改进工具描述文档，提升开发效率

### 3. 架构优化

#### 🏗️ HistoryManager 核心升级
- **单例模式**：确保全局只有一个历史管理器实例
- **裁剪方向枚举**：新增 Crop_Direction 枚举类型
- **柔性裁剪策略**：支持 TOP/BOTTOM 两种裁剪方向
- **边界检查**：严格的裁剪数量验证和边界保护


## 🎯 Chapter5 vs Chapter4 vs Chapter3

| 特性 | Chapter3 | Chapter4 | Chapter5 |
|------|----------|----------|----------|
| 响应模式 | ✅ 实时流式 | ✅ 实时流式 | ✅ 实时流式 |
| 用户体验 | ✅ 即时反馈 | ✅ 即时反馈 | ✅ 即时反馈 |
| 工具调用 | ✅ 流式支持 | ✅ 流式支持 | ✅ 流式支持 |
| 错误处理 | ✅ 优雅降级 | ✅ 优雅降级 | ✅ 优雅降级 |
| 历史管理 | ❌ 无限制堆积 | 🆕 智能压缩 | 🆕 智能压缩 |
| Token监控 | ❌ 无追踪 | 🆕 实时显示 | 🆕 实时显示 |
| 成本跟踪 | ❌ 无感知 | 🆕 总成本显示 | 🆕 总成本显示 |
| 长对话支持 | ❌ 容易超限 | 🆕 自动优化 | 🆕 自动优化 |
| 成本控制 | ❌ 无感知 | 🆕 使用量可见 | 🆕 使用量可见 |
| 上下文优化 | ❌ 手动重启 | 🆕 自动压缩 | 🆕 自动压缩 |
| 缓存优化 | ❌ 无缓存 | 🆕 智能缓存 | 🆕 智能缓存 |
| **智能裁剪** | ❌ 不支持 | ❌ 不支持 | 🆕 **精准裁剪** |
| **用户交互** | ❌ 简单拒绝 | ❌ 简单拒绝 | 🆕 **原因捕获** |
| **架构稳定性** | ❌ 基础架构 | ✅ 历史管理 | 🆕 **单例模式** |
| **错误处理** | ❌ 基础处理 | ✅ 改进处理 | 🆕 **统一异常** |
| **开发体验** | ❌ 基础工具 | ✅ 调试支持 | 🆕 **增强调试** |

## 🧪 测试覆盖

Chapter5 包含完整的智能裁剪和历史管理测试套件：

```bash
# 运行历史压缩测试
python test/test_history_compress.py

# 运行智能裁剪测试 [NEW]
python test/test_crop_message.py
```

测试覆盖：
- ✅ 自动压缩触发条件
- ✅ 多会话压缩逻辑
- ✅ 单会话压缩逻辑
- ✅ Token使用量更新
- ✅ 压缩阈值判断
- ✅ 成本跟踪准确性
- ✅ 消息格式转换
- ✅ **智能裁剪功能** **[NEW]**
- ✅ **TOP/BOTTOM裁剪策略** **[NEW]**
- ✅ **用户消息保护机制** **[NEW]**
- ✅ **边界检查验证** **[NEW]**
- ✅ **错误处理覆盖** **[NEW]**

这个框架的核心思想是让 AI 能够"思考"（通过对话）和"行动"（通过工具调用），并且在执行可能有风险的操作时需要用户确认。Chapter4 的智能历史管理进一步解决了长对话中的上下文管理难题，Chapter5 的智能裁剪功能为用户提供了精细的上下文控制能力。成本跟踪功能帮助用户实时了解API使用费用，增强的用户交互体验使AI能够更好地理解用户意图，新的消息格式为未来的多模态功能扩展奠定了基础。通过单例模式和统一异常处理，系统架构更加稳定可靠，使AI代理能够在保持对话连贯性的同时，提供专业级的上下文管理和用户体验，为构建真正实用的AI助手奠定了坚实基础。
