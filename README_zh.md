# Agent 学习项目

## 🚀 体验 Quick Star CLI 的强大功能！

![Quick Star CLI](resources/images/quick_star_cli.png)

**✨ 立即尝试 Quick Star CLI！** 一个具有优雅命令行界面、实时流式响应和强大代码生成能力的智能AI助手。

## 🎮 看看AI能做什么：AI创造的贪吃蛇游戏！

![贪吃蛇游戏](resources/images/snake_game.jpg)

**🎯 来玩贪吃蛇游戏！** 这个功能完整的游戏完全通过与 Quick Star CLI 的自然语言对话创建，展示了：
- 🧠 **智能代码生成** - 从简单描述生成完整游戏逻辑
- 🔧 **实时调试** - 即时迭代和改进代码
- 📁 **智能文件管理** - 处理复杂项目结构
- 🎨 **交互式应用** - 创建引人入胜的用户体验

**准备创造令人惊叹的作品了吗？** 按照下面的安装指南开始使用 Quick Star CLI 创造吧！

---


本项目展示了AI智能体的渐进式开发过程，从基础的工具调用到具有历史记录控制的高级流式智能体。每个章节都在前一章的基础上构建，展示渐进式改进和新功能。

## 项目结构

```
├── .env                          # 环境配置（所有章节共享）
├── .env.example                  # 环境配置模板
├── requirements.txt              # Python 依赖包
├── chapter1_tool_call_api/       # 基础工具调用示例（原生函数调用 & XML 工具调用）
├── chapter2_ReAct_agent/         # 基础 ReAct 智能体实现
├── chapter3_stream_agent/        # 具有实时响应的流式智能体
├── chapter4_history_control/     # 具有对话历史管理的高级智能体
├── chapter5_smart_context/       # 具有智能裁剪的智能上下文管理
└── chapter6_to_do_write/         # 使用TodoWrite工具的任务管理 [新增]
```

## 各章节功能特性

### 第1章：工具调用 API
- **原生函数调用（Native Function Call）**：使用 JSON Schema 的标准 OpenAI 函数调用接口
- **XML 工具调用（XML Tool Call）**：在自然语言中使用 XML 格式的灵活工具调用
- 两种不同工具调用方法的比较
- 基础 API 客户端设置和工具执行
- 理解工具调用模式的基础

### 第2章：ReAct 智能体
- 基础 ReAct（推理和行动）模式实现
- 基于第1章概念构建的工具调用能力
- 带有环境变量配置的 API 客户端
- 缺失环境变量的错误处理

### 第3章：流式智能体
- 包含第2章的所有功能
- **新增**：实时流式响应
- **新增**：渐进式输出显示
- 通过实时反馈增强用户体验

### 第4章：历史记录控制
- 包含第3章的所有功能
- **新增**：对话历史管理
- **新增**：达到令牌限制时的上下文压缩
- **新增**：长对话的内存优化

### 第5章：智能上下文管理
- 包含第4章的所有功能
- **新增**：支持 TOP/BOTTOM 策略的智能上下文裁剪
- **新增**：智能用户拒绝原因捕获
- **新增**：统一异常管理的增强错误处理
- **新增**：确保状态一致性的 HistoryManager 单例模式
- **新增**：用于精确消息管理的 SmartContextCropper 工具
- **新增**：带有 VSCode 配置的高级调试支持
- **新增**：保护用户消息的全面安全保障

### 第6章：TodoWrite工具 - 任务管理 [新增]
- 包含第5章的所有功能
- **新增**：TodoWrite工具用于结构化任务管理和进度跟踪
- **新增**：智能任务组织和自动待办事项列表创建
- **新增**：实时进度监控和状态更新
- **新增**：任务复杂度分析的智能决策引擎
- **新增**：主动检测的上下文感知任务管理
- **新增**：测试验证的质量保证集成
- **新增**：待处理任务管理的自动提醒系统
- **新增**：可视化进度指示器和完成验证


## 系统要求

- Python 3.8 或更高版本
- Conda（推荐）或 pip
- OpenAI 兼容的 API 访问权限（OpenRouter、OpenAI 等）

## 安装说明

### 1. 克隆仓库

```bash
https://github.com/woodx9/build-your-claude-code-from-scratch.git
cd build-your-claude-code-from-scratch
```

### 2. 创建并激活 Conda 环境

```bash
# 创建新的 conda 环境
conda create -n agentLearning python=3.11

# 激活环境
conda activate agentLearning
```

### 3. 安装依赖包

您可以使用以下任一方法安装依赖包：

#### 一：从 requirements.txt 安装
```bash
# 安装所有必需的包
pip install -r requirements.txt
```

#### 二：以开发模式安装（推荐用于开发）
```bash
# 或者其他chapter
cd chapter5_smart_context

pip install -e .
```

#### 三：运行
```bash
quickstar
```


#### 四：运行成功
```bash
❯ quickstar

 ══════════════════════════════════════════════════
  ✦ ✦ ✦ ✦ ✦ ✧ ✧ ✧ ✧ ✧ 

★ Welcome to Quick Star ★

  ✧ ✧ ✧ ✧ ✧ ✦ ✦ ✦ ✦ ✦ 
 ══════════════════════════════════════════════════

👤
请输入: hello, relpy one
🤖
Hello! Nice to meet you. How can I help you today?                                                
👤
请输入: 
```


### 4. 环境配置

1. 复制示例环境文件：
   ```bash
   cp .env.example .env
   ```

2. 使用您的 API 凭据编辑 `.env` 文件：
   ```bash
   # OpenAI API 配置
   OPENAI_API_KEY=your_api_key_here
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   OPENAI_MODEL=anthropic/claude-sonnet-4
   # 单位是 k（千）
   MODEL_MAX_TOKENS=200
   COMPRESS_THRESHOLD=0.8
   ```

### 5. 必需的环境变量

| 变量 | 描述 | 示例 |
|------|------|------|
| `OPENAI_API_KEY` | 您的 API 密钥 | `sk-or-v1-...` |
| `OPENAI_BASE_URL` | API 端点 URL | `https://openrouter.ai/api/v1` |
| `OPENAI_MODEL` | 要使用的模型 | `anthropic/claude-sonnet-4` |
| `MODEL_MAX_TOKENS` | 响应的最大令牌数（以千为单位） | `200` |
| `COMPRESS_THRESHOLD` | 历史压缩阈值（0.0-1.0） | `0.8` |


## API 提供商

本项目支持任何 OpenAI 兼容的 API。经过测试的提供商包括：

- **OpenRouter**（推荐）：提供对多种模型的访问
- **OpenAI**：官方 OpenAI API
- **本地 LLM 服务器**：任何实现 OpenAI API 格式的服务器

### OpenRouter 设置

1. 在 [openrouter.ai](https://openrouter.ai) 注册
2. 从仪表板获取您的 API 密钥
3. 使用 `https://openrouter.ai/api/v1` 作为基础 URL
4. 从可用模型中选择，如：
   - `anthropic/claude-sonnet-4`
   - `openai/gpt-4`
   - `meta-llama/llama-3.1-70b-instruct`

### OpenAI 设置

1. 从 [platform.openai.com](https://platform.openai.com) 获取 API 密钥
2. 使用 `https://api.openai.com/v1` 作为基础 URL
3. 使用如 `gpt-4`、`gpt-3.5-turbo` 等模型

## 开发指南

### 项目结构（每个章节）

```
chapter_X/
├── src/
│   ├── core/
│   │   ├── api_client.py      # 带环境配置的 API 客户端
│   │   └── conversation.py    # 对话管理
│   ├── tools/
│   │   ├── base_agent.py      # 基础智能体实现
│   │   ├── tool_manager.py    # 工具管理
│   │   └── cmd_runner.py      # 命令执行工具
│   └── main.py                # 入口点
├── pyproject.toml             # 项目配置
└── readme.md                  # 章节特定文档
```

**注意**：第1章具有更简单的结构，直接使用 Python 文件演示工具调用概念。

### 核心组件

- **APIClient**：带环境变量配置的单例模式客户端
- **BaseAgent**：实现 ReAct 模式的核心智能体逻辑
- **ToolManager**：管理可用工具及其执行
- **ConversationManager**：处理对话历史和上下文

### 错误处理

项目包含全面的错误处理：

- 缺失环境变量会抛出描述性错误
- API 失败会被捕获并报告
- 工具执行错误会被优雅地处理

## 故障排除

### 常见问题

1. **未找到环境变量**
   ```
   ValueError: 环境变量 OPENAI_API_KEY 未设置或为空。请检查 .env 文件中的配置。
   ```
   **解决方案**：确保 `.env` 文件存在并包含所有必需的变量

2. **API 连接失败**
   ```
   API请求失败: Connection error
   ```
   **解决方案**：检查您的网络连接和 API 端点 URL

3. **无效的 API 密钥**
   ```
   API请求失败: Unauthorized
   ```
   **解决方案**：验证您的 API 密钥是否正确且有足够的余额

### 测试环境设置

```bash
# 测试环境变量是否正确加载
python -c "
import sys
sys.path.append('chapter2_ReAct_agent/src')
from core.api_client import APIClient
client = APIClient()
print('✅ 环境加载成功！')
print(f'使用模型: {client.model}')
"
```

## 贡献指南

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 彻底测试
5. 提交 Pull Request

## 许可证

本项目仅用于教育目的。请遵守您选择的 API 提供商的服务条款。

## 支持

如有问题和疑问：
1. 查看故障排除部分
2. 查看章节特定的 README 文件
3. 在仓库中提出 issue

---

**注意**：本项目演示了渐进式 AI 智能体开发。从第1章开始了解基础工具调用概念，然后进入第2章学习 ReAct 模式，第3章学习流式处理能力，最后第4章学习高级历史记录管理。

## 章节对比：功能演进

| 功能特性 | 第1章 | 第2章 | 第3章 | 第4章 | 第5章 |
|---------|-------|-------|-------|-------|-------|
| 工具调用 | ✅ 基础 | ✅ ReAct | ✅ ReAct | ✅ ReAct | ✅ ReAct |
| 实时流式 | ❌ | ❌ | ✅ 新增 | ✅ | ✅ |
| 历史管理 | ❌ | ❌ | ❌ | ✅ 新增 | ✅ |
| 自动压缩 | ❌ | ❌ | ❌ | ✅ 新增 | ✅ |
| 成本跟踪 | ❌ | ❌ | ❌ | ✅ 新增 | ✅ |
| **智能裁剪** | ❌ | ❌ | ❌ | ❌ | ✅ **新增** |
| **增强用户体验** | ❌ | ❌ | ❌ | ❌ | ✅ **新增** |
