from fastapi import APIRouter

from internal.schemas.itinerary import LocationResponse, SearchResult
from internal.schemas.location import LocationRequest
from internal.service.itinerary import search_locations

router = APIRouter(prefix="/location")


@router.post("/group", response_model=LocationResponse)
async def find_group_tours(body: LocationRequest) -> LocationResponse:
    results = await search_locations(body.latitude, body.longitude, "group tours")
    return LocationResponse(
        results=[SearchResult(title=r["title"], url=r["url"], snippet=r.get("content", "")) for r in results]
    )


@router.post("/places", response_model=LocationResponse)
async def find_places(body: LocationRequest) -> LocationResponse:
    results = await search_locations(body.latitude, body.longitude, "places to see")
    return LocationResponse(
        results=[SearchResult(title=r["title"], url=r["url"], snippet=r.get("content", "")) for r in results]
    )


@router.post("/activities", response_model=LocationResponse)
async def find_activities(body: LocationRequest) -> LocationResponse:
    results = await search_locations(body.latitude, body.longitude, "activities")
    return LocationResponse(
        results=[SearchResult(title=r["title"], url=r["url"], snippet=r.get("content", "")) for r in results]
    )
