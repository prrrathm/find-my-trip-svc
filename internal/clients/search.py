import primp
from bs4 import BeautifulSoup

_BING_URL = "https://www.bing.com/search"


class Search:
    @staticmethod
    async def SearchXNG(query, max_results=10, **kwargs):
        params = {"q": query}
        async with primp.AsyncClient(
            impersonate="chrome_131", follow_redirects=True
        ) as client:
            response = await client.get(_BING_URL, params=params, timeout=15)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for item in soup.select("li.b_algo"):
            if len(results) >= max_results:
                break
            title_el = item.find("h2")
            if not title_el:
                continue
            a_el = title_el.find("a")
            if not a_el:
                continue
            title = a_el.get_text(strip=True)
            href = a_el.get("href", "")
            if not title or not href:
                continue

            caption = item.find("div", class_="b_caption")
            snippet = ""
            if caption:
                p = caption.find("p")
                if p:
                    snippet = p.get_text(strip=True)

            results.append({
                "title": title,
                "url": href,
                "content": snippet,
            })

        return results


search = Search()
web_search = search.SearchXNG
