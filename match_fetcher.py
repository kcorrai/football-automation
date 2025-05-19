import requests
import json
from datetime import datetime, timedelta

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
        # Sadece 'FINISHED' olan maçları filtrele ve terminalde yazdır
        finished_matches = [
            match for match in data["matches"] if match["status"] == "FINISHED"
        ]
        print("Ham veri (FINISHED maçlar):", json.dumps(finished_matches, indent=4))
        today = datetime.utcnow().date() - timedelta(days=10) # Günün UTC tarihini al
        yesterday = today - timedelta(days=1)  # Dünün tarihini al
        # Maç bilgilerini işleyip sadece dün ve bugün arasındaki 'FINISHED' maçları döndür
        matches = [
            {
                "home_team": match["homeTeam"]["name"],
                "away_team": match["awayTeam"]["name"],
                "time": match["utcDate"],
                "status": match["status"],
                "competition": match["competition"]["name"],
                "venue": match["venue"] if "venue" in match else "Unknown",  # Bazı maçlarda venue olmayabilir
                "score": f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}" 
            }
            for match in finished_matches
            if yesterday <= datetime.fromisoformat(match["utcDate"].split("T")[0]).date() <= today
        ]
        
        # En son skorları yazdır
        print("\nEn Son Skorlar:")
        for match in matches:
            print(f"{match['home_team']} vs {match['away_team']} - Skor: {match['score']}")
        
        return matches
    else:
        raise Exception(f"Failed to fetch matches: {response.status_code}")