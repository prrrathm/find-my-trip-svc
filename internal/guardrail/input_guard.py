import re

from fastapi import HTTPException

_INJECTION_PATTERNS = [
    r"ignore\s+(?:all\s+)?(?:previous|above)\s+instructions",
    r"system\s+prompt",
    r"you\s+are\s+now",
    r"pretend\s+(?:you\s+are|to\s+be)",
    r"jailbreak",
    r"\bDAN\b",
    r"disregard\s+(?:all\s+)?(?:previous|prior)\s+instructions",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in _INJECTION_PATTERNS]


def guard_location_name(location_name: str) -> None:
    for pattern in _COMPILED:
        if pattern.search(location_name):
            raise HTTPException(status_code=400, detail="invalid location")
