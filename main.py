import json
import schedule
import time
import sys
from match_fetcher import load_match_config, fetch_matches
from email_sender import send_email_now

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
        body = "\n".join([f"{match['home_team']} vs {match['away_team']} - {match['time']}" for match in matches])
        send_email_now(config_path)
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def main():
    # Check for "now" argument
    if len(sys.argv) > 1 and sys.argv[1] == "now":
        print("Anlık e-posta gönderimi başlatılıyor...")
        send_email_now("config.json")
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
