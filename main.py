from src.server import mcp

if __name__ == "__main__":
    # You can switch to "stdio" if running via Claude Desktop
    mcp.run(transport="sse")