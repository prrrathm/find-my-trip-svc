import httpx

from internal.core.config import settings

_BRAVE_API_URL = "https://api.search.brave.com/res/v1/web/search"
_BRAVE_HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
}

_TAVILY_API_URL = "https://api.tavily.com/search"


class Search:
    @staticmethod
    async def SearchXNG(query: str, max_results: int = 10, **kwargs) -> list[dict]:
        try:
            results = await _search_searxng(query, max_results)
            if results:
                return results
        except Exception:
            results = []

        if settings.brave_api_key:
            try:
                return await _search_brave(query, max_results)
            except Exception:
                pass
        if settings.tavily_api_key:
            return await _search_tavily(query, max_results)
        return results

    @staticmethod
    async def brave(query: str, max_results: int = 10, **kwargs) -> list[dict]:
        return await _search_brave(query, max_results)

    @staticmethod
    async def tavily(query: str, max_results: int = 10, **kwargs) -> list[dict]:
        return await _search_tavily(query, max_results)


async def _search_searxng(query: str, max_results: int = 10) -> list[dict]:
    params = {"q": query, "format": "json", "language": "en"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.search_xng_url.rstrip("/") + "/search",
            params=params,
            timeout=15,
        )
        response.raise_for_status()

    data = response.json()
    results = []
    for item in data.get("results", []):
        if len(results) >= max_results:
            break
        url = item.get("url", "")
        title = item.get("title", "")
        content = item.get("content", "")
        if not title or not url:
            continue
        results.append({
            "title": title,
            "url": url,
            "content": content,
        })

    return results


async def _search_brave(query: str, max_results: int = 10) -> list[dict]:
    headers = {**_BRAVE_HEADERS, "X-Subscription-Token": settings.brave_api_key}
    params = {"q": query, "count": min(max_results, 20), "safesearch": "off"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            _BRAVE_API_URL,
            headers=headers,
            params=params,
            timeout=15,
        )
        response.raise_for_status()

    data = response.json()
    results = []
    for item in data.get("web", {}).get("results", []):
        if len(results) >= max_results:
            break
        url = item.get("url", "")
        title = item.get("title", "")
        description = item.get("description", "")
        if not title or not url:
            continue
        results.append({
            "title": title,
            "url": url,
            "content": description,
        })

    return results


async def _search_tavily(query: str, max_results: int = 10) -> list[dict]:
    payload = {
        "api_key": settings.tavily_api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            _TAVILY_API_URL,
            json=payload,
            timeout=15,
        )
        response.raise_for_status()

    data = response.json()
    results = []
    for item in data.get("results", []):
        if len(results) >= max_results:
            break
        url = item.get("url", "")
        title = item.get("title", "")
        content = item.get("content", "")
        if not title or not url:
            continue
        results.append({
            "title": title,
            "url": url,
            "content": content,
        })

    return results


search = Search()
web_search = search.SearchXNG
