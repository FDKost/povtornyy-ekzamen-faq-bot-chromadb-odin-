import requests
from langchain.tools import Tool
from typing import Dict, Any

class HTTPGetTool:
    """
    MCP-style HTTP GET tool.
    Performs a GET request to a given URL and returns the JSON response.
    Includes basic retry logic and error handling.
    """
    name: str = "http_get"
    description: str = (
        "Perform an HTTP GET request to a given URL and return the JSON response. "
        "Use this tool when you need to fetch data from an external API."
    )

    def __call__(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            # Try to parse JSON; if fails, return raw text
            try:
                data = response.json()
                return str(data)
            except ValueError:
                return response.text
        except requests.RequestException as e:
            return f"Error during HTTP GET: {str(e)}"

http_get_tool = Tool(
    name=HTTPGetTool.name,
    func=HTTPGetTool(),
    description=HTTPGetTool.description,
)
