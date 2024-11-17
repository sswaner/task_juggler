import schedule
import time
import requests

def scrape():
    print("Scraping data...")
    response = requests.get("https://example.com")
    if response.status_code == 200:
        print("Scraped successfully!")
    else:
        print("Failed to scrape.")

# Schedule scraper to run every hour
schedule.every().hour.do(scrape)

# Keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(1)