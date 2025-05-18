import json
import schedule
import time
import sys
from match_fetcher import load_match_config, fetch_matches
from email_sender import send_email_now
from sofascore_scraper import get_sofascore_link

def send_daily_email():
    # Config dosyasını yükle
    config_path = "config.json"
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Maç bilgilerini çekmek için API yapılandırmasını yükle
    api_url, api_key = load_match_config(config_path)

    # Maç bilgilerini al ve e-posta gönder
    try:
        matches = fetch_matches(api_url, api_key)
        competitions = {}
        for match in matches:
            competition = match["competition"]
            if competition not in competitions:
                competitions[competition] = []
            # Generate the search query
            query = f"{match['home_team']}+{match['away_team']}+sofascore"
            link = get_sofascore_link(query)
            # Print query and link to the terminal
            print(f"Query: {query} | Link: {link if link else 'None'}")
            competitions[competition].append(
                f"{match['home_team']} vs {match['away_team']} - Score: {match['score']} - Sofascore: {link if link else 'No link found'}"
            )
        
        body = "\n\n".join([
            f"{competition}\n" + "\n".join(competitions[competition])
            for competition in competitions
        ])
        send_email_now(config_path, body)
        print("E-posta başarıyla gönderildi.")  # Confirmation message
    except Exception as e:
        print(e)  # Show the full error message without prefix

def main():
    # Check for "now" argument
    if len(sys.argv) > 1 and sys.argv[1] == "now":
        print("Anlık e-posta gönderimi başlatılıyor...")
        config_path = "config.json"
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        # Maç bilgilerini çekmek için API yapılandırmasını yükle
        api_url, api_key = load_match_config(config_path)

        # Maç bilgilerini al ve e-posta gönder
        try:
            matches = fetch_matches(api_url, api_key)
            competitions = {}
            for match in matches:
                competition = match["competition"]
                if competition not in competitions:
                    competitions[competition] = []
                # Generate the search query
                query = f"{match['home_team']} vs {match['away_team']} score {match['score']} sofascore"
                link = get_sofascore_link(query)
                # Print query and link to the terminal
                print(f"Query: {query} | Link: {link if link else 'None'}")
                competitions[competition].append(
                    f"{match['home_team']} vs {match['away_team']} - Score: {match['score']} - Sofascore: {link if link else 'No link found'}"
                )
            
            body = "\n\n".join([
                f"{competition}\n" + "\n".join(competitions[competition])
                for competition in competitions
            ])
            send_email_now(config_path, body)
            print("E-posta başarıyla gönderildi.")  # Confirmation message
        except Exception as e:
            print(e)  # Show the full error message without prefix
        sys.exit()

    # Config dosyasını yükle
    config_path = "config.json"
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Planlama zamanını config dosyasından al
    schedule_time = config["schedule_time"]

    # Belirtilen saatte e-posta gönder
    schedule.every().day.at(schedule_time).do(send_daily_email)

    print(f"Planlama başlatıldı. Her gün saat {schedule_time}'da e-posta gönderilecek. Çıkmak için Ctrl+C.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
