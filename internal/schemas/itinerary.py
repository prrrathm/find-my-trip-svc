from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str


class LocationResponse(BaseModel):
    results: list[SearchResult]
    travel_blocked: bool = False
    travel_message: str | None = None
