"""
travel_checker.py

Given a latitude/longitude, determine:
  - what the location is (country name, or ocean/sea name if it's water)
  - whether it can be "travelled" to (False for oceans and restricted countries)

Design:
  1. Offline land/water check -> global_land_mask (fast, no internet, no rate limits)
  2. If water   -> identify the ocean via rough bounding-box regions (offline)
  3. If land    -> reverse-geocode via OpenStreetMap Nominatim to get the country
                   name, then check it against a restricted-country list

Dependencies:
    pip install global-land-mask geopy

Note: reverse geocoding (step 3) needs internet access, since it calls
Nominatim's public API (nominatim.openstreetmap.org). The ocean-name lookup
does NOT need internet.
"""

from global_land_mask import globe
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# ---------------------------------------------------------------------------
# 1. Countries considered "cannot travel" -- adjust this list to match
#    whatever policy/travel-advisory source you actually want to follow.
#    This is just a starting point (commonly cited as heavily restricted
#    or off-limits for casual/tourist travel).
# ---------------------------------------------------------------------------
RESTRICTED_COUNTRIES = {
    "North Korea",
    "Syria",
    "Afghanistan",
    "Yemen",
    "Somalia",
    "South Sudan",
    "Iran",
    "Russia",           # example only -- edit to your actual policy
    "Belarus",          # example only -- edit to your actual policy
}

# ---------------------------------------------------------------------------
# 2. Very rough ocean bounding boxes for offline naming. Good enough for a
#    "which ocean is this point roughly in" answer; not survey-grade.
#    Order matters -- first match wins.
# ---------------------------------------------------------------------------
_OCEAN_REGIONS = [
    ("Arctic Ocean",   lambda lat, lon: lat >= 66.5),
    ("Southern Ocean", lambda lat, lon: lat <= -60),
    ("Indian Ocean",   lambda lat, lon: -60 < lat < 30 and 20 <= lon <= 147),
    ("Atlantic Ocean", lambda lat, lon: -60 < lat < 66.5 and (-70 <= lon <= 20)),
    ("Pacific Ocean",  lambda lat, lon: -60 < lat < 66.5 and (lon > 147 or lon < -70)),
]


def _guess_ocean_name(lat: float, lon: float) -> str:
    for name, in_region in _OCEAN_REGIONS:
        if in_region(lat, lon):
            return name
    return "Unknown ocean/sea"


def _reverse_geocode_country(lat: float, lon: float) -> str:
    """Reverse-geocode a land point to a country name using Nominatim.
    Falls back to 'Unknown' if the network call fails."""
    geolocator = Nominatim(user_agent="travel_checker_app")
    try:
        location = geolocator.reverse((lat, lon), language="en", timeout=10)
        if location and "country" in location.raw.get("address", {}):
            return location.raw["address"]["country"]
        return "Unknown"
    except (GeocoderTimedOut, GeocoderUnavailable, Exception):
        return "Unknown"


def check_location(lat: float, lon: float) -> dict:
    """
    Main function.

    Args:
        lat: latitude  (-90 to 90)
        lon: longitude (-180 to 180)

    Returns:
        {"location": <name>, "canTravel": <bool>}
    """
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError("lat must be in [-90, 90] and lon must be in [-180, 180]")

    is_land = globe.is_land(lat, lon)

    if not is_land:
        ocean_name = _guess_ocean_name(lat, lon)
        return {"location": ocean_name, "canTravel": False}

    country = _reverse_geocode_country(lat, lon)
    if country == "Unknown":
        return {"location": country, "canTravel": True}
    can_travel = country not in RESTRICTED_COUNTRIES

    return {"location": country, "canTravel": can_travel}


if __name__ == "__main__":
    samples = [
        ("Middle of Pacific", 0.0, -160.0),
        ("Pyongyang, North Korea", 39.0392, 125.7625),
        ("London, UK", 51.5074, -0.1278),
        ("Middle of Atlantic", 10.0, -40.0),
    ]
    for label, lat, lon in samples:
        print(label, "->", check_location(lat, lon))