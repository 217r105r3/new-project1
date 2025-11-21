import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def geocode_city(city: str):
    """
    Convert city name to latitude/longitude using Open-Meteo geocoding API.
    """
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }
    r = requests.get(GEOCODE_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    if "results" not in data or not data["results"]:
        return None

    first = data["results"][0]
    return {
        "name": first.get("name"),
        "country": first.get("country"),
        "lat": first["latitude"],
        "lon": first["longitude"],
    }


def get_forecast(lat: float, lon: float, days: int = 15):
    """
    Get 15-day daily forecast (temp + rain) for given coordinates.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ",".join(
            [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",  # total rain+snow per day (mm)
            ]
        ),
        "current": "temperature_2m,precipitation,wind_speed_10m",
        "timezone": "auto",
        "forecast_days": days,  # up to 16 supported
    }

    r = requests.get(FORECAST_URL, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def describe_rain(mm: float) -> str:
    """
    Turn rain amount in mm into a simple human sentence.
    """
    if mm == 0:
        return "No rain expected"
    elif mm < 2:
        return "Very light rain possible"
    elif mm < 10:
        return "Light to moderate rain"
    elif mm < 30:
        return "Heavy rain likely"
    else:
        return "Very heavy rain / possible storm"


def print_current(city_info: dict, data: dict):
    current = data.get("current", {})

    temp = current.get("temperature_2m")
    precip = current.get("precipitation")
    wind = current.get("wind_speed_10m")

    print("\n========= CURRENT WEATHER =========")
    print(f"Location   : {city_info['name']}, {city_info['country']}")
    if temp is not None:
        print(f"Temperature: {temp}°C")
    if wind is not None:
        print(f"Wind Speed : {wind} km/h")
    if precip is not None:
        if precip > 0:
            print(f"Now       : It is currently raining ({precip} mm/h approx.)")
        else:
            print("Now       : No rain at the moment")
    print("===================================\n")


def print_15_day_forecast(data: dict):
    daily = data["daily"]
    dates = daily["time"]
    max_t = daily["temperature_2m_max"]
    min_t = daily["temperature_2m_min"]
    rain = daily["precipitation_sum"]

    print("========= 15-DAY FORECAST =========")
    for date, tmax, tmin, r in zip(dates, max_t, min_t, rain):
        rain_text = describe_rain(r)
        print(f"\nDate       : {date}")
        print(f"Max / Min  : {tmax}°C / {tmin}°C")
        print(f"Rain (mm)  : {r}")
        print(f"Prediction : {rain_text}")
    print("\n===================================\n")


def main():
    print("🌦 Advanced Weather App (Python + Open-Meteo)")
    print("Shows current weather + 15-day forecast with rain prediction.")
    print("Type 'q' to quit.\n")

    while Tru

