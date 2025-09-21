from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("caculator", log_level="WARNING")


@mcp.tool()
async def adder(number1: int, number2: int) -> int:
    """Add two numbers together and return the sum.
    
    Args:
        number1: The first number to add
        number2: The second number to add
        
    Returns:
        The sum of number1 and number2
    """
    return number1 + number2

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')