from flask import Blueprint, render_template, request

from .data import LOCATIONS
from .services.weather_service import fetch_live_data


main = Blueprint("main", __name__)


@main.route("/")
def index():
    selected_key = request.args.get("city", "delhi").lower()
    if selected_key not in LOCATIONS:
        selected_key = "delhi"

    selected_location = LOCATIONS[selected_key]
    live_data = fetch_live_data(selected_location["lat"], selected_location["lon"])
    status_message = "Unable to fetch live weather and AQI right now. Please try again in a moment."

    return render_template(
        "index.html",
        locations=LOCATIONS,
        selected_key=selected_key,
        selected_location=selected_location,
        live_data=live_data,
        status_message=status_message,
    )
