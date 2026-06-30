# SearXNG / Tavily / Brave behind one interface
import httpx

from internal.core.config import settings

class Search:

    def __init__(self):
        self.search_xng_url = settings.search_xng_url

    async def SearchXNG(self, search_string):
        search_url = (
            self.search_xng_url + "/search?q=" + search_string + "&format=json"
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(search_url)
        return response.json()


# import asyncio
# search = Search()

# print(asyncio.run(search.SearchXNG("bali tour packages")))