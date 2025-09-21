# 第8章：MCP客户端实现

[English Version](./README.md)

## 第8章新功能

第8章实现了模型上下文协议（MCP）客户端功能，允许QuickStar CLI连接并与外部MCP服务器交互，扩展功能能力。

### 🔧 设置说明

运行本章之前，需要配置MCP服务器：

1. **更新mcp.json配置文件：**
   ```bash
   # 编辑 chapter8_mcp_client/src/mcp_servers/mcp.json 中的路径
   # 将Python解释器路径和脚本路径更新为你的环境路径
   ```

2. **将mcp.json复制到quickstar配置目录：**
   ```bash
   mkdir -p ~/.quickstar
   cp chapter8_mcp_client/src/mcp_servers/mcp.json ~/.quickstar/
   ```

### 🤖 新增核心组件

#### 1. MCP客户端 (`src/tools/mcp_client/client.py`)
- **用途**：连接外部MCP服务器的主要MCP客户端
- **功能**：`async def connect_to_server()` - 建立与所有配置服务器的连接
- **特性**：多服务器支持、异步会话管理、自动连接处理

#### 2. MCP服务器配置 (`src/tools/mcp_client/server_config.py`)
- **用途**：从JSON文件管理MCP服务器配置
- **类**：`MCPServer`、`MCPConfig`
- **功能**：从`~/.quickstar/mcp.json`加载并验证服务器配置

#### 3. MCP工具包装器 (`src/tools/mcp_tool.py`)
- **用途**：将外部MCP工具包装到内部工具系统中
- **功能**：`async def act(self, **kwargs)` - 执行MCP工具调用
- **集成**：与现有工具架构无缝集成MCP工具

#### 4. 工具管理器更新 (`src/tools/tool_manager.py`)
- **增强**：添加`_mcp_client`属性用于MCP集成
- **特性**：初始化期间自动加载MCP工具

### 🌐 什么是MCP（模型上下文协议）？

MCP是一个开放协议，使AI应用程序能够与外部数据源和工具集成。它提供：

- **标准化接口**：AI助手连接各种工具和服务的通用方式
- **可扩展性**：无需修改核心应用代码即可轻松添加新功能
- **工具发现**：从MCP服务器自动检测和集成可用工具
- **安全性**：通过定义的协议控制对外部资源的访问

### 🔌 我们在QuickStar CLI中的MCP实现

我们的实现展示了如何将MCP集成到AI助手中：

#### 架构
```
QuickStar CLI → MCP客户端 → MCP服务器（天气、计算器等）
                     ↓
             工具发现与执行
                     ↓
             统一工具接口
```

#### 核心特性

1. **动态工具加载**：MCP服务器暴露的工具被自动发现并集成
2. **统一接口**：外部MCP工具与内置工具无缝协作
3. **配置驱动**：通过JSON配置轻松添加新的MCP服务器
4. **异步支持**：与多个MCP服务器的非阻塞通信

#### 包含的示例MCP服务器

1. **天气服务器** (`src/mcp_servers/weather.py`)
   - 提供天气预报和预警功能
   - 工具：`get_forecast`、`get_alerts`

2. **计算器服务器** (`src/mcp_servers/caculator.py`)
   - 提供数学计算功能
   - 工具：`adder`用于基本算术运算

### 🚀 MCP集成的优势

- **模块化**：无需更改核心代码即可添加新功能
- **可重用性**：MCP服务器可在不同AI应用程序间共享
- **标准化**：遵循行业标准协议进行工具集成
- **灵活性**：轻松启用/禁用特定工具或服务器
- **可扩展性**：支持多个服务器同时连接

### 📁 文件结构变化

```
chapter8_mcp_client/
├── src/
│   ├── tools/
│   │   ├── mcp_client/          # 新增：MCP客户端实现
│   │   │   ├── client.py        # 主要MCP客户端
│   │   │   └── server_config.py # 配置管理
│   │   ├── mcp_tool.py         # 新增：MCP工具包装器
│   │   └── tool_manager.py     # 更新：MCP集成
│   └── mcp_servers/            # 新增：示例MCP服务器
│       ├── mcp.json           # 服务器配置
│       ├── weather.py         # 天气MCP服务器
│       └── caculator.py       # 计算器MCP服务器
```

### 🔄 工作原理

1. **初始化**：CLI启动并从`~/.quickstar/mcp.json`加载MCP配置
2. **服务器连接**：MCP客户端与所有配置的服务器建立连接
3. **工具发现**：每个服务器通过MCP协议暴露其可用工具
4. **工具集成**：外部工具被包装并添加到内部工具注册表中
5. **执行**：当用户请求需要MCP工具时，通过标准化接口调用
6. **响应**：MCP工具的结果被处理并呈现给用户

此实现展示了MCP如何扩展AI助手的功能，同时在核心功能和外部集成之间保持清晰的分离。
