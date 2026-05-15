import requests


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_aqi_label(aqi_value):
    if aqi_value is None:
        return "Unavailable", "Air quality data could not be loaded right now."
    if aqi_value <= 20:
        return "Good", "Air is clean for most people."
    if aqi_value <= 40:
        return "Fair", "Air quality is acceptable for normal outdoor activity."
    if aqi_value <= 60:
        return "Moderate", "Sensitive people may want shorter outdoor exposure."
    if aqi_value <= 80:
        return "Poor", "Limit long outdoor activity if you are sensitive to pollution."
    return "Very Poor", "Outdoor activity should be reduced, especially for sensitive groups."


def fetch_live_data(lat, lon):
    weather_url = "https://api.open-meteo.com/v1/forecast"
    air_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset",
        "timezone": "auto",
        "forecast_days": 5,
    }
    air_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "us_aqi,pm2_5,pm10",
    }

    try:
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        air_response = requests.get(air_url, params=air_params, timeout=10)
        weather_response.raise_for_status()
        air_response.raise_for_status()

        weather_payload = weather_response.json()
        air_payload = air_response.json()
        weather_data = weather_payload.get("current", {})
        air_data = air_payload.get("current", {})
        daily_data = weather_payload.get("daily", {})

        aqi_index = air_data.get("us_aqi")
        aqi_label, aqi_note = get_aqi_label(aqi_index)

        forecast = []
        dates = daily_data.get("time", [])
        max_temps = daily_data.get("temperature_2m_max", [])
        min_temps = daily_data.get("temperature_2m_min", [])

        for index, day in enumerate(dates):
            forecast.append(
                {
                    "date": day,
                    "max": max_temps[index] if index < len(max_temps) else None,
                    "min": min_temps[index] if index < len(min_temps) else None,
                }
            )

        return {
            "temperature": weather_data.get("temperature_2m"),
            "feels_like": weather_data.get("apparent_temperature"),
            "humidity": weather_data.get("relative_humidity_2m"),
            "wind_speed": weather_data.get("wind_speed_10m"),
            "description": WEATHER_CODES.get(weather_data.get("weather_code"), "Condition unavailable"),
            "aqi_index": aqi_index,
            "aqi_label": aqi_label,
            "aqi_note": aqi_note,
            "pm2_5": air_data.get("pm2_5"),
            "pm10": air_data.get("pm10"),
            "sunrise": (daily_data.get("sunrise") or [None])[0],
            "sunset": (daily_data.get("sunset") or [None])[0],
            "forecast": forecast,
        }
    except requests.RequestException:
        return None
