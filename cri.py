from flask import Flask, render_template
import requests
import os

API_KEY = "bec257df-01f2-4e83-b70e-2c4d53d95f85"
URL = "https://api.cricapi.com/v1/currentMatches"

app = Flask(__name__)

def get_matches():
    params = {
        "apikey": API_KEY,
        "offset": 0
    }

    try:
        response = requests.get(URL, params=params)
        data = response.json()

        if data.get("status") == "success":
            return data.get("data", [])
        else:
            return []

    except Exception as e:
        return []


@app.route('/')
def index():
    matches = get_matches()
    return render_template('index.html', matches=matches)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)