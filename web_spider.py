import requests
from bs4 import BeautifulSoup
import argparse

# Importing from your other file
from Code_tracer import lexical_analyzer, parse_js, generate_cfg

def crawl_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        print(f"\n Fetched URL: {url}")

        print("\n Extracted <script> tags and analyzing each:")
        scripts = soup.find_all('script')
        for idx, script in enumerate(scripts):
            js_code = script.string
            if js_code:
                print(f"\nScript #{idx + 1}:\n", js_code)

                # Tokenization
                tokens = lexical_analyzer(js_code)
                print("\n Tokens:", tokens)

                # AST
                parsed_ast = parse_js(js_code)
                print("\n Parsed AST:")
                print(parsed_ast["body"])

                # CFG
                cfg = generate_cfg(parsed_ast)
                print("\n Control Flow Graph:")
                print(cfg)

        print("\nExtracted links:")
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                print(href)

    except Exception as e:
        print(f" Error fetching {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Spider with JS Analysis")
    parser.add_argument("url", help="URL of the website to crawl and analyze scripts")

    args = parser.parse_args()
    crawl_website(args.url)
