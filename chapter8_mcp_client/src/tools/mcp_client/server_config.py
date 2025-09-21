import json
from pathlib import Path
from typing import List, Dict, Optional

class MCPServer:
    def __init__(self, name: str, type_: str, command: str, args: List[str]):
        self.name = name
        self.type = type_
        self.command = command
        self.args = args

    def __repr__(self):
        return f"<MCPServer name={self.name}, type={self.type}, command={self.command}, args={self.args}>"

class MCPConfig:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path).expanduser()
        self.servers: Dict[str, MCPServer] = {}
        self._load_config()

    def _load_config(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"MCP config file not found: {self.config_path}")

        with self.config_path.open("r", encoding="utf-8") as f:
            raw_config = json.load(f)

        mcp_servers = raw_config.get("mcpServers", {})
        for name, info in mcp_servers.items():
            type_ = info.get("type")
            if not (type_ == "stdio" or type_ is None):
                # only handle stdio type
                continue

            command = info.get("command")
            args = info.get("args", [])
            if not command or not args:
                raise ValueError(f"Invalid stdio mcp server config for {name}: {info}, Please reset src/tools/mcp_client/mcp.json")

            self.servers[name] = MCPServer(name=name, type_=type_, command=command, args=args)

    def get_server(self, name: str) -> Optional[MCPServer]:
        return self.servers.get(name)

    def list_servers(self) -> List[str]:
        return list(self.servers.keys())


