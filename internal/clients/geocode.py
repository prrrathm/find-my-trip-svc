import asyncio

import httpx

_NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
_HEADERS = {"User-Agent": "find-my-trip/1.0"}
_MAX_RETRIES = 3


async def get_location_name(latitude: float, longitude: float) -> str:
    # accept-language=en: without it Nominatim returns place names in the local
    # language (e.g. 東京都), which cascades into non-English search queries
    params = {"lat": latitude, "lon": longitude, "format": "json", "zoom": 10, "accept-language": "en"}
    for attempt in range(_MAX_RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(_NOMINATIM_URL, params=params, headers=_HEADERS, timeout=15)
                response.raise_for_status()
                data = response.json()
            break
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout):
            if attempt == _MAX_RETRIES - 1:
                raise
            await asyncio.sleep(2 ** attempt)

    address = data.get("address", {})
    specific = None
    for key in ("city", "town", "village", "county", "state"):
        if key in address:
            specific = address[key]
            break

    country = address.get("country")
    if specific and country:
        return f"{specific}, {country}"
    if country:
        return country

    # fallback: first segment of display_name
    return data.get("display_name", "unknown location").split(",")[0].strip()
