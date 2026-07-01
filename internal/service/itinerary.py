from internal.agents.orchestrator import run_agent
from internal.clients.geocode import get_location_name
from internal.guardrail.input_guard import guard_location_name


async def search_locations(latitude: float, longitude: float, intent: str) -> list[dict]:
    location_name = await get_location_name(latitude, longitude)
    guard_location_name(location_name)
    return await run_agent(location_name, intent)
