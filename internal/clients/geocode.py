import httpx

_NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
_HEADERS = {"User-Agent": "find-my-trip/1.0"}


async def get_location_name(latitude: float, longitude: float) -> str:
    params = {"lat": latitude, "lon": longitude, "format": "json", "zoom": 10}
    async with httpx.AsyncClient() as client:
        response = await client.get(_NOMINATIM_URL, params=params, headers=_HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

    address = data.get("address", {})
    specific = None
    for key in ("city", "town", "village", "county", "state"):
        if key in address:
            specific = address[key]
            break

    country = address.get("country")
    if specific and country:
        return f"{specific}, {country}".lower()
    if country:
        return country.lower()

    # fallback: first segment of display_name
    return data.get("display_name", "unknown location").split(",")[0].strip().lower()
