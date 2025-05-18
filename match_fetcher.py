import requests
import json

def load_match_config(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config["api_url"], config["api_key"]

def fetch_matches(api_url, api_key):
    headers = {
        "X-Auth-Token": api_key  # Football-Data.org için gerekli başlık
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Maç bilgilerini işleyip döndür
        matches = [
            {
                "home_team": match["homeTeam"]["name"],
                "away_team": match["awayTeam"]["name"],
                "time": match["utcDate"]
            }
            for match in data.get("matches", [])
        ]
        return matches
    else:
        raise Exception(f"Failed to fetch matches: {response.status_code}")
