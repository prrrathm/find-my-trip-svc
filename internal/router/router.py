from fastapi import APIRouter

from internal.schemas.itinerary import LocationResponse, SearchResult
from internal.schemas.location import LocationRequest
from internal.service.itinerary import search_locations
from internal.tools.travel_checker import check_location

router = APIRouter(prefix="/location")


def _travel_response(lat: float, lon: float) -> LocationResponse | None:
    travel = check_location(lat, lon)
    if travel["canTravel"]:
        return None
    name = travel["location"]
    if "Ocean" in name or "Sea" in name:
        msg = f"Oops! We can't bathe in the {name} 🫨"
    else:
        msg = f"{name} doesn't seem like a safe place to travel, you know 😐"
    return LocationResponse(results=[], travel_blocked=True, travel_message=msg)


@router.post("/group", response_model=LocationResponse)
async def find_group_tours(body: LocationRequest) -> LocationResponse:
    blocked = _travel_response(body.latitude, body.longitude)
    if blocked:
        return blocked
    results = await search_locations(body.latitude, body.longitude, "group tours")
    return LocationResponse(
        results=[SearchResult(title=r["title"], url=r["url"], snippet=r.get("content", "")) for r in results]
    )


@router.post("/places", response_model=LocationResponse)
async def find_places(body: LocationRequest) -> LocationResponse:
    blocked = _travel_response(body.latitude, body.longitude)
    if blocked:
        return blocked
    results = await search_locations(body.latitude, body.longitude, "places to see")
    return LocationResponse(
        results=[SearchResult(title=r["title"], url=r["url"], snippet=r.get("content", "")) for r in results]
    )


@router.post("/activities", response_model=LocationResponse)
async def find_activities(body: LocationRequest) -> LocationResponse:
    blocked = _travel_response(body.latitude, body.longitude)
    if blocked:
        return blocked
    results = await search_locations(body.latitude, body.longitude, "activities")
    return LocationResponse(
        results=[SearchResult(title=r["title"], url=r["url"], snippet=r.get("content", "")) for r in results]
    )
