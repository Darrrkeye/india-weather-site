from flask import Blueprint, render_template, request

from .data import LOCATIONS
from .services.weather_service import fetch_live_data


main = Blueprint("main", __name__)


def score_location(key, location, search_query):
    normalized = search_query.strip().lower()
    if not normalized:
        return -1

    name = location["name"].lower()
    state = location["state"].lower()
    tagline = location["tagline"].lower()
    key = key.lower()
    name_words = name.split()
    state_words = state.split()

    if name == normalized:
        return 100
    if state == normalized:
        return 95
    if key == normalized:
        return 92
    if name.startswith(normalized):
        return 90
    if state.startswith(normalized):
        return 82
    if key.startswith(normalized):
        return 80
    if any(word.startswith(normalized) for word in name_words):
        return 72
    if any(word.startswith(normalized) for word in state_words):
        return 66
    if name.find(f" {normalized}") != -1:
        return 58
    if state.find(f" {normalized}") != -1:
        return 54
    if len(normalized) >= 3 and normalized in tagline:
        return 20
    return -1


def filter_locations(search_query):
    if not search_query:
        return LOCATIONS

    matches = [
        (key, location, score_location(key, location, search_query))
        for key, location in LOCATIONS.items()
    ]
    filtered = [(key, location, score) for key, location, score in matches if score >= 0]
    filtered.sort(key=lambda item: (-item[2], item[1]["name"]))

    if not filtered:
        return LOCATIONS

    return {key: location for key, location, _ in filtered}


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
        all_locations=LOCATIONS,
        total_locations=len(LOCATIONS),
        visible_count=len(visible_locations),
        selected_key=selected_key,
        selected_location=selected_location,
        live_data=live_data,
        search_query=search_query,
        status_message=status_message,
    )
