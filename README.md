# Documentation Search MCP Server

A high-performance Model Context Protocol (MCP) server built with Python, designed to fetch and convert official library documentation into clean, LLM-friendly Markdown.

It leverages `DuckDuckGo` for precise searching and `selectolax` for ultra-fast HTML parsing.

## 🚀 Features

- **Parallel Scraping**: Uses `asyncio` and `httpx` to fetch multiple documentation pages simultaneously.
- **Smart Parsing**: Strips headers, footers, and sidebars to provide only the relevant technical content.
- **Markdown Conversion**: Formats HTML into structured Markdown (headings, code blocks, lists).
- **Dynamic Registry**: Support for pre-configured libraries (LangChain, OpenAI, etc.) with the ability to dynamically register new sources at runtime.
- **Auto-Discovery**: Can attempt to find a library's official documentation URL automatically if it's not in the registry.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd mcp_documentation
   ```

2. **Create a virtual environment and install dependencies**:

   Using `python` and `pip`:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Or, using [`uv`](https://docs.astral.sh/uv/) as a faster drop-in replacement:
   ```bash
   # Create a virtual environment (optional if you prefer uv-managed envs)
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install from requirements.txt using uv's pip interface
   uv pip install -r requirements.txt
   ```

## ⚙️ Configuration

### Adding Extra Documentation via Environment
You can add custom documentation sources without modifying the code by setting the `MCP_EXTRA_DOCS` environment variable:

```json
export MCP_EXTRA_DOCS='{"fastapi": "https://fastapi.tiangolo.com", "flask": "https://flask.palletsprojects.com"}'
```
```


### Claude Desktop Integration
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "doc-search": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["/path/to/mcp_documentation/main.py"],
      "env": {
        "MCP_EXTRA_DOCS": "{\"fastapi\": \"https://fastapi.tiangolo.com\"}"
      }
    }
  }
}
```


## 🛠️ Tools

### `search_docs(library, query)`
Searches the specified library for the query.
- **Example**: `search_docs(library="langchain", query="how to use multi-agent systems")`
- **Behavior**: If the library isn't registered, it will attempt to find the documentation URL via DuckDuckGo and auto-register it for the current session.

### `register_new_library(name, base_url)`
Manually add a new documentation site to the server's knowledge during a session.
- **Example**: `register_new_library(name="pytorch", base_url="https://pytorch.org/docs")`

### `list_supported_libraries()`
Returns a list of all libraries currently in the registry.

## 🏗️ Project Structure

- `main.py`: Entry point for the server.
- `src/server.py`: FastMCP server definition and tool implementation.
- `src/parser.py`: Logic for cleaning HTML and converting it to Markdown.
- `src/search.py`: DuckDuckGo search integration.
- `src/config.py`: Registry management and default configurations.

## 📄 License
MIT