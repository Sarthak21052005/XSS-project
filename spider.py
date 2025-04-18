import requests
from bs4 import BeautifulSoup
import argparse

def crawl_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        print(f"\n📥 Fetched URL: {url}")

        print("\n📜 Extracted <script> tags:")
        scripts = soup.find_all('script')
        for script in scripts:
            print(script)

        print("\n🔗 Extracted links:")
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                print(href)

    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Web Spider to extract scripts and links from a website.")
    parser.add_argument("url", help="URL of the website to crawl")

    args = parser.parse_args()
    crawl_website(args.url)
