# SearXNG / Tavily / Brave behind one interface
import httpx
import json
from internal.core.config import settings

# TODO - infer the search service using a parameter
class Search:

    def __init__(self):
        self.search_xng_url = settings.search_xng_url

    async def SearchXNG(self, search_string, max_results=10):
        search_url = self.search_xng_url + "/search?q=" + search_string + "&format=json"
        async with httpx.AsyncClient() as client:
            response = await client.get(search_url)
            response.raise_for_status()
            results = response.json().get("results", [])
        return [
            {"title": x.get("title"), "url": x.get("url"), "content": x.get("content")}
            for x in results[:max_results]
        ]



search = Search()
web_search = search.SearchXNG

# * testing search results
# import asyncio
# result = search.SearchXNG("bali tour packages", 20)
# print(asyncio.run(search.SearchXNG("bali tour packages", 20)))