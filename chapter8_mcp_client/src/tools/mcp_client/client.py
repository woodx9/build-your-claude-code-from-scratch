# adapt from https://modelcontextprotocol.io/docs/develop/build-client

import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters, LoggingLevel
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

from .server_config import MCPConfig

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.sessions: list[ClientSession] = []
        self.exit_stack = AsyncExitStack()
        self.config = MCPConfig("~/.quickstar/mcp.json")

        self.connect_server_task = asyncio.create_task(self.connect_to_server())

    async def connect_to_server(self):
        """Connect to all MCP servers

        """
        mcp_servers = self.config.list_servers()

        for name in mcp_servers:
            server = self.config.get_server(name)

            server_params = StdioServerParameters(
                command=server.command,
                args=server.args,
                env=None
            )

            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            stdio, write = stdio_transport
            session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))

            await session.initialize()
            self.sessions.append(session)

    async def get_sessions(self) -> list[ClientSession]:
        await self.connect_server_task
        return self.sessions