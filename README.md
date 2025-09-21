# Agent Learning Project

**[中文版本 / Chinese Version](README_zh.md)**

## 🚀 Experience Quick Star CLI in Action!

![Quick Star CLI](resources/images/quick_star_cli.png)

**✨ Try Quick Star CLI now!** An intelligent AI agent with elegant command-line interface, real-time streaming responses, and powerful code generation capabilities.

## 🎮 See What's Possible: Snake Game Created by AI!
![Snake Game](resources/images/snake_game.jpg)

**🎯 Play the snake game!** This fully functional game was created entirely through natural language conversations with Quick Star CLI, showcasing:
- 🧠 **Intelligent Code Generation** - Complete game logic from simple descriptions
- 🔧 **Real-time Debugging** - Iterate and improve code instantly  
- 📁 **Smart File Management** - Handle complex project structures
- 🎨 **Interactive Applications** - Create engaging user experiences

**Ready to build something amazing?** Follow the installation guide below and start creating with Quick Star CLI!

---


This project demonstrates the progressive development of AI agents, from basic tool calling to advanced streaming agents with history control. Each chapter builds upon the previous one, showing incremental improvements and new features.

## Project Structure

```
├── .env                          # Environment configuration (shared by all chapters)
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
├── chapter1_tool_call_api/       # Basic tool calling examples (Native Function Call & XML Tool Call)
├── chapter2_ReAct_agent/         # Basic ReAct agent implementation
├── chapter3_stream_agent/        # Streaming agent with real-time responses
├── chapter4_history_control/     # Advanced agent with conversation history management
├── chapter5_smart_context/       # Smart context management with intelligent cropping
├── chapter6_to_do_write/         # Task management with TodoWrite tool
└── chapter7_sub_agent/           # Sub-agent architecture with task delegation
└── chapter8_mcp_client/         # MCP (Model Context Protocol) client implementation [NEW]
```

### Chapter 1: Tool Call API Fundamentals
- **Native Function Call**: Standard OpenAI JSON Schema interface with type safety
- **XML Tool Call**: Universal XML format compatible with any text model
- Comparison and use cases for both approaches
- Foundation for understanding tool calling patterns

### Chapter 2: ReAct Agent Architecture
- **ReAct pattern**: Think-Act-Observe cycle for intelligent agents
- **Recursive conversation handling** for continuous AI interactions
- **User approval system** for dangerous operations with safety controls
- **Singleton conversation manager** for consistent state management
- Complete tool execution framework with error handling

### Chapter 3: Real-Time Streaming Agent
- **Character-by-character streaming** for immediate AI response visibility
- **Streaming tool calls** that work seamlessly with tool execution
- **Configuration externalization** with .env file management
- Graceful degradation with auto-fallback to standard mode
- Improved user experience with no waiting for complete responses

### Chapter 4: Intelligent History Management
- **Auto history compression** with smart multi-session and single-session strategies
- **Real-time token monitoring** with context usage percentage display
- **Comprehensive cost tracking** with model-specific pricing and session summaries
- **Preservation guarantees** for system messages and recent context
- Performance optimization for long-running conversations

### Chapter 5: Smart Context Cropping
- **Precision context control** with TOP/BOTTOM message cropping strategies
- **Smart Context Cropper tool** for manual conversation management
- **Safety guarantees** protecting latest user messages and system prompts
- **Summary support** for cropped content to maintain context continuity
- **Integration** with existing auto-compression and cost tracking systems

### Chapter 6: Structured Task Management
- **TodoWrite tool** for automated task organization and progress tracking
- **Intelligent workflow breakdown** converting complex requests into structured lists
- **Real-time state management** with pending/in_progress/completed lifecycle
- **Quality assurance gates** preventing premature task completion
- **Context awareness** deciding when todo lists add value vs. simple execution

### Chapter 7: Sub-Agent Architecture
- **Task Tool** for delegating complex tasks to specialized sub-agents
- **SubagentManager** with isolated conversation contexts and lifecycle management
- **Autonomous execution** where sub-agents run independently with full tool access
- **Async tool system** converting all tools to support proper concurrency
- **Task delegation flow** for decomposing complex workflows into manageable units
- **Specialization benefits** with concurrent execution and resource isolation

### Chapter 8: MCP Client Implementation
- **MCP Protocol Support** for connecting to external Model Context Protocol servers
- **Dynamic Tool Loading** with automatic discovery and integration of MCP tools
- **Multi-Server Support** connecting to multiple MCP servers simultaneously
- **Unified Tool Interface** seamlessly integrating external MCP tools with built-in tools
- **Configuration-Driven Setup** easy management of MCP servers via JSON configuration
- **Sample MCP Servers** including weather forecasting and calculator implementations


## Prerequisites

- Python 3.8 or higher
- Conda (recommended) or pip
- OpenAI-compatible API access (OpenRouter, OpenAI, etc.)

## Installation Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/woodx9/build-your-claude-code-from-scratch.git
cd build-your-claude-code-from-scratch
```

### 2. Create and Activate Conda Environment

```bash
# Create new conda environment
conda create -n agentLearning python=3.11

# Activate environment
conda activate agentLearning
```

### 3. Install Dependencies

You can install dependencies using any of the following methods:

#### Option 1: Install from requirements.txt
```bash
# Install all required packages
pip install -r requirements.txt
```

#### Option 2: Install in Development Mode (Recommended for Development)
```bash
# 或者其他chapter
cd chapter5_smart_context

pip install -e .
```

#### Option 3: Run
```bash
quickstar
```

#### Option 4: Successful Run
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

### 4. Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your API credentials:
   ```bash
   # OpenAI API Configuration
   OPENAI_API_KEY=your_api_key_here
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   OPENAI_MODEL=anthropic/claude-sonnet-4
   # The unit is k
   MODEL_MAX_TOKENS=200
   COMPRESS_THRESHOLD=0.8
   ```

### 5. Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your API key | `sk-or-v1-...` |
| `OPENAI_BASE_URL` | API endpoint URL | `https://openrouter.ai/api/v1` |
| `OPENAI_MODEL` | Model to use | `anthropic/claude-sonnet-4` |
| `MODEL_MAX_TOKENS` | Max tokens for responses (in thousands) | `200` |
| `COMPRESS_THRESHOLD` | History compression threshold (0.0-1.0) | `0.8` |

## Usage

### Running Chapter 1 (Tool Call API Examples)

```bash
cd chapter1_tool_call_api

# Run Native Function Call example
python native_function_call.py

# Run XML Tool Call example  
python xml_tool_call.py
```

## API Providers

This project supports any OpenAI-compatible API. Tested providers include:

- **OpenRouter** (recommended): Provides access to multiple models
- **OpenAI**: Official OpenAI API
- **Local LLM servers**: Any server implementing OpenAI API format

### OpenRouter Setup

1. Sign up at [openrouter.ai](https://openrouter.ai)
2. Get your API key from the dashboard
3. Use `https://openrouter.ai/api/v1` as the base URL
4. Choose from available models like:
   - `anthropic/claude-sonnet-4`
   - `openai/gpt-4`
   - `meta-llama/llama-3.1-70b-instruct`

### OpenAI Setup

1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Use `https://api.openai.com/v1` as the base URL
3. Use models like `gpt-4`, `gpt-3.5-turbo`

## Development

### Project Structure (Each Chapter)

```
chapter_X/
├── src/
│   ├── core/
│   │   ├── api_client.py      # API client with environment config
│   │   └── conversation.py    # Conversation management
│   ├── tools/
│   │   ├── base_agent.py      # Base agent implementation
│   │   ├── tool_manager.py    # Tool management
│   │   └── cmd_runner.py      # Command execution tool
│   └── main.py                # Entry point
├── pyproject.toml             # Project configuration
└── readme.md                  # Chapter-specific documentation
```

**Note**: Chapter 1 has a simpler structure with direct Python files demonstrating tool calling concepts.

### Key Components

- **APIClient**: Singleton pattern client with environment variable configuration
- **BaseAgent**: Core agent logic implementing ReAct pattern
- **ToolManager**: Manages available tools and their execution
- **ConversationManager**: Handles conversation history and context

### Error Handling

The project includes comprehensive error handling:

- Missing environment variables throw descriptive errors
- API failures are caught and reported
- Tool execution errors are handled gracefully

## Troubleshooting

### Common Issues

1. **Environment variables not found**
   ```
   ValueError: 环境变量 OPENAI_API_KEY 未设置或为空。请检查 .env 文件中的配置。
   ```
   **Solution**: Ensure `.env` file exists and contains all required variables

2. **API connection failed**
   ```
   API请求失败: Connection error
   ```
   **Solution**: Check your internet connection and API endpoint URL

3. **Invalid API key**
   ```
   API请求失败: Unauthorized
   ```
   **Solution**: Verify your API key is correct and has sufficient credits

### Testing Environment Setup

```bash
# Test if environment variables are loaded correctly
python -c "
import sys
sys.path.append('chapter2_ReAct_agent/src')
from core.api_client import APIClient
client = APIClient()
print('✅ Environment loaded successfully!')
print(f'Using model: {client.model}')
"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT license

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review chapter-specific README files
3. Open an issue on the repository

---

**Note**: This project demonstrates progressive AI agent development. Start with Chapter 1 to understand basic tool calling concepts, then move to Chapter 2 for ReAct patterns, Chapter 3 for streaming capabilities, and finally Chapter 4 for advanced history management.
