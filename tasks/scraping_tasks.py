import requests

def run_scraper(url, save_path):
    print(f"Scraping {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'w') as file:
            file.write(response.text)
        print(f"Scraped successfully and saved to {save_path}.")
        requests.post("https://ntfy.sh/lincolnshire_poacher",
            data=f"{url} Scrape Successful".encode(encoding='utf-8'))
    else:
        print(f"Failed to scrape {url}.")
        requests.post("https://ntfy.sh/lincolnshire_poacher",
            data=f"Fail Scrape {url}".encode(encoding='utf-8'))

if __name__ == "__main__":
    run_scraper("https://example.com", "example.html")
