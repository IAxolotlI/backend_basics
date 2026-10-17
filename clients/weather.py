from clients.http import get_json, NotFoundError, BadResponseError

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WMO = {
    0: "clear sky", 
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "rime fog",
    51: "light drizzle",
    53: "drizzle",
    55: "dense drizzle",
    61: "light rain",
    63: "rain",
    65: "heavy rain",
    71: "light snow",
    73: "snow",
    75: "heavy snow",
    80: "rain showers",
    81: "rain showers",
    82: "violent rain showers",
    95: "thunderstorm",
    96: "thunderstorm with hail",
    99: "thunderstorm with hail",
}


def get_weather(city):
    geo = get_json(GEO_URL, {"name": city, "count": 1, "language": "en"})
    results = geo.get("results") if isinstance(geo, dict) else None
    if not results:
        raise NotFoundError(f"city not found: {city}")

    lat, lon = results[0]["latitude"], results[0]["longitude"]
    data = get_json(FORECAST_URL, {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weather_code",
    })

    current = data.get("current") if isinstance(data, dict) else None
    if not current or "temperature_2m" not in current:
        raise BadResponseError("weather")

    return {
        "temp_c": float(current["temperature_2m"]),
        "description": WMO.get(current.get("weather_code"), "unknown"),
    }