import asyncio
import httpx
from mcp.server.fastmcp import FastMCP
from .config import registry, DEFAULT_HEADERS
from .search import ddg_search
from .parser import DocParser

mcp = FastMCP("DocSearch")
parser = DocParser()


async def fetch_url(client: httpx.AsyncClient, url: str) -> str:
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        content = parser.parse(response.text)
        return f"--- SOURCE: {url} ---\n{content}\n"
    except Exception as e:
        return f"--- ERROR: Could not fetch {url}: {str(e)} ---\n"



@mcp.tool()
async def register_new_library(name: str, base_url: str) -> str:
    """
    Dynamically add a new library documentation source to the registry.
    Example: name="fastapi", base_url="https://fastapi.tiangolo.com"
    """
    registry.register(name, base_url)
    return f"Library '{name}' successfully registered at {base_url}."



@mcp.tool()
async def list_supported_libraries() -> list[str]:
    """Return a list of all currently supported library names."""
    return registry.list_supported()

@mcp.tool()
async def search_docs(library: str, query: str):
    """"
    Search the latest official documentations for a given query and library.
    Supports langchain, openai, llama-index.

    Args:
      query: The query to search for (e.g. "Chroma DB")
      library: The library to search in (e.g. "langchain")

    Returns:
      Concatenated text content of top linked pages or list of URLs if fetch fails
    """
    base_url = registry.get_url(library)
    if not base_url:
        # Attempt to "discover" the documentation URL via DuckDuckGo
        discovery_query = f"{library} official documentation"
        potential_urls = ddg_search(discovery_query, "", max_results=1)
        if potential_urls:
            base_url = potential_urls[0]
            # Optionally auto-register it for the session
            registry.register(library, base_url)
        else:
            supported = ", ".join(registry.list_supported())
            return f"Error: '{library}' not found. Supported: {supported}. Use register_new_library to add it."

    urls = ddg_search(query, base_url)
    if not urls:
        return "No results found."

    async with httpx.AsyncClient(headers=DEFAULT_HEADERS, follow_redirects=True) as client:
        tasks = [fetch_url(client, url) for url in urls]
        results = await asyncio.gather(*tasks)

    return "\n\n".join(results)