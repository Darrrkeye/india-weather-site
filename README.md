# India Travel Climate Guide

This project is a Flask site that shows:

- current weather
- AQI
- a 5-day forecast
- places to visit in selected Indian cities

## Run locally

```powershell
pip install -r requirements.txt
python Weather.py
```

Open `http://127.0.0.1:5000/` in your browser.

## Project structure

```text
Weather.py
app/
  __init__.py
  data.py
  routes.py
  services/
    weather_service.py
templates/
  layout.html
  index.html
static/
  css/
    style.css
  js/
    app.js
```

## Deploy

This project includes a `Procfile` for services like Render or Railway.
