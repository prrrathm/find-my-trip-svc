# tool schemas
from internal.clients.search import web_search

WEB_SEARCH_SCHEMA = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Searches the web for travel info. Returns ",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search Query"},
                "max_results": {"type": "integer", "default": 10},
            },
            "required": ["query"],
        },
    },
}

REGISTRY = {"web_search": web_search}
TOOL_SCHEMA = [WEB_SEARCH_SCHEMA]
