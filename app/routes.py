from flask import Blueprint, render_template, request

from .data import LOCATIONS
from .services.weather_service import fetch_live_data


main = Blueprint("main", __name__)


def filter_locations(search_query):
    if not search_query:
        return LOCATIONS

    normalized = search_query.strip().lower()
    filtered = {
        key: location
        for key, location in LOCATIONS.items()
        if normalized in key
        or normalized in location["name"].lower()
        or normalized in location["state"].lower()
        or normalized in location["tagline"].lower()
    }
    return filtered or LOCATIONS


@main.route("/")
def index():
    search_query = request.args.get("search", "").strip()
    visible_locations = filter_locations(search_query)
    selected_key = request.args.get("city", "delhi").lower()
    if selected_key not in LOCATIONS or selected_key not in visible_locations:
        selected_key = next(iter(visible_locations))

    selected_location = LOCATIONS[selected_key]
    live_data = fetch_live_data(selected_location["lat"], selected_location["lon"])
    status_message = "Unable to fetch live weather and AQI right now. Please try again in a moment."

    return render_template(
        "index.html",
        locations=visible_locations,
        total_locations=len(LOCATIONS),
        visible_count=len(visible_locations),
        selected_key=selected_key,
        selected_location=selected_location,
        live_data=live_data,
        search_query=search_query,
        status_message=status_message,
    )
