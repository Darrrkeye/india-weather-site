import requests

API_KEY = "bec257df-01f2-4e83-b70e-2c4d53d95f85"
URL = "https://api.cricapi.com/v1/currentMatches"

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
            print("API returned an error:")
            print(data)
            return []

    except Exception as e:
        print("Error connecting to API:", e)
        return []


def show_matches(matches):

    if not matches:
        print("⚠ No matches returned from API")
        return

    print("\n🏏 Matches Found:\n")

    for match in matches:

        name = match.get("name", "Unknown Match")
        status = match.get("status", "No status")
        date = match.get("date", "No date")

        print("Match:", name)
        print("Status:", status)
        print("Date:", date)
        print("-" * 40)


def main():

    print("🏏 Cricket Live Scores App\n")

    matches = get_matches()

    show_matches(matches)


if __name__ == "__main__":
    main()