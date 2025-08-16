# 第四章：智能历史管理

[English Version](./README.md)

## 第四章新增功能

第四章在流式智能体基础上增加了**智能对话历史管理**和**全面的成本跟踪**：

### 🧠 自动历史压缩
- **智能压缩**：自动管理上下文窗口使用率
- **令牌监控**：实时显示上下文使用百分比
- **多会话策略**：优先移除最旧的完整对话
- **单会话策略**：需要时移除中间响应
- **保护机制**：始终保留系统消息和近期上下文

### 💰 成本跟踪系统
- **实时监控**：对话过程中跟踪 API 成本
- **基于令牌计算**：根据实际使用量精确估算成本
- **模型专用定价**：支持不同模型的定价层级
- **会话摘要**：每个对话会话的成本分析

## 历史压缩策略

### 多会话压缩
当上下文接近限制时，移除整个对话会话：
```
[系统消息] ← 始终保留
[旧会话 1] ← 首先移除
[旧会话 2] ← 接着移除
[近期会话] ← 始终保留
[当前会话] ← 始终保留
```

### 单会话压缩
在当前会话内，移除中间工具响应：
```
用户："运行命令 X"
助手："我将运行该命令"
[工具结果] ← 可以移除
助手："命令已成功完成"
用户："现在运行命令 Y" ← 近期消息保留
```

## 技术实现

### 历史管理器
[`HistoryManager`](src/core/history_manager.py) - 智能压缩：

```python
def compress_history_if_needed(self, messages, max_tokens):
    """接近上下文限制时自动压缩"""
    
def multi_session_compression(self, messages):
    """移除最旧的完整对话会话"""
    
def single_session_compression(self, messages):  
    """移除当前会话内的中间响应"""
```

### 成本跟踪器
[`CostTracker`](src/core/cost_tracker.py) - 监控 API 费用：

```python
def calculate_cost(self, input_tokens, output_tokens, model_name):
    """基于令牌使用量和模型定价计算成本"""
    
def display_cost_info(self, session_cost, total_cost):
    """向用户显示实时成本信息"""
```

## 用户体验增强

### 上下文监控
```
💬 上下文：3,456/8,192 令牌 (42%) 💰 本次会话：$0.023
```

### 自动压缩通知
```
🧠 上下文快满了 (85%)。正在压缩历史...
✅ 已压缩 2 个旧会话。上下文：2,100/8,192 令牌 (26%)
```

### 成本感知
```
💰 API 成本摘要：
   本次会话：$0.045
   今日总计：$0.156
   模型：Claude 3.5 Sonnet
```

## 配置设置

增强的环境变量：
```env
# API 配置（来自第三章）
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=anthropic/claude-3.5-sonnet

# 历史管理（新增）
MAX_CONTEXT_TOKENS=8192
COMPRESSION_THRESHOLD=0.85

# 成本跟踪（新增）
ENABLE_COST_TRACKING=true
DAILY_COST_LIMIT=10.00
```

## 优势

- **成本控制**：通过实时监控避免意外的 API 费用
- **性能优化**：通过管理上下文大小保持快速响应
- **长期支持**：支持无需手动干预的扩展对话
- **透明度**：清晰地了解资源使用情况和成本

## 下一步

→ **第五章**：添加智能上下文裁剪工具，实现细粒度的对话管理控制。
