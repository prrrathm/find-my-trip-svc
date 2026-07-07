import asyncio

from internal.clients.search import search
from internal.core.config import settings


async def run_agent(location_name: str, intent: str) -> list[dict]:
    queries = _build_queries(location_name, intent)
    tasks = [search.SearchXNG(q, max_results=10) for q in queries]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    accumulated: list[dict] = []
    for r in results:
        if isinstance(r, list):
            accumulated.extend(r)

    return _dedup(accumulated)


def _build_queries(location_name: str, intent: str) -> list[str]:
    city = location_name.split(",")[0].strip()
    return [
        f"{city} {intent} travel",
        f"{city} travel {intent}",
    ]


def _dedup(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    unique: list[dict] = []
    for item in items:
        url = item.get("url", "")
        if url not in seen:
            seen.add(url)
            unique.append(item)
    return unique
