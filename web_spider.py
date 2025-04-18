import requests
from bs4 import BeautifulSoup
import argparse
import os
import urllib.parse

# Import your Code Tracer functions
from Code_tracer import lexical_analyzer, parse_js, generate_cfg
# Import JS Extractor
from js_extractor import extract_js_behavior_types

def save_script(js_code, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(js_code)
    print(f" Saved JS to: {filename}")

def analyze_js(js_code, script_name=""):
    print(f"\n🔍 Analyzing {script_name}:")

    # Tokenization
    tokens = lexical_analyzer(js_code)
    print("  • Tokens:", tokens)

    # AST
    parsed_ast = parse_js(js_code)
    print("  • AST Parsed.")

    # CFG
    cfg = generate_cfg(parsed_ast)
    print("  • Control Flow Graph (CFG):", cfg)

def crawl_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        print(f"\nCrawling URL: {url}")

        scripts = soup.find_all('script')
        print(f" Found {len(scripts)} <script> tags.")

        output_dir = "extracted_js"
        os.makedirs(output_dir, exist_ok=True)

        for idx, script in enumerate(scripts):
            js_code = script.string
            filename = ""

            # Inline JS
            if js_code:
                filename = os.path.join(output_dir, f"inline_script_{idx + 1}.js")
                save_script(js_code, filename)
                analyze_js(js_code, f"Inline Script #{idx + 1}")

            # External JS
            elif script.get('src'):
                script_src = script['src']
                full_url = urllib.parse.urljoin(url, script_src)

                try:
                    ext_response = requests.get(full_url)
                    if ext_response.status_code == 200:
                        js_code = ext_response.text
                        filename = os.path.join(output_dir, f"external_script_{idx + 1}.js")
                        save_script(js_code, filename)
                        analyze_js(js_code, f"External Script #{idx + 1}")
                    else:
                        print(f"  Failed to fetch: {full_url} [Status: {ext_response.status_code}]")
                except Exception as ex:
                    print(f"  Error downloading external JS: {full_url}\n{ex}")
            else:
                print(f"  Skipped malformed/empty script #{idx + 1}")

        #  Run the JavaScript Behavior Extractor
        print("\n Running JavaScript Behavior Extractor:")
        auto_scripts, event_handlers, js_links = extract_js_behavior_types(soup, url)

        print(f"\n Auto-executed Scripts Detected: {len(auto_scripts)}")
        for name, source in auto_scripts:
            print(f"  • {name} ({'URL' if source.startswith('http') else 'inline'})")

        print(f"\n Event-handler Scripts Detected: {len(event_handlers)}")
        for tag, attr, val in event_handlers:
            print(f"  • <{tag}> has '{attr}' event -> JS: {val[:60]}...")

        print(f"\n JavaScript URL Links Detected: {len(js_links)}")
        for href in js_links:
            print(f"  • {href}")

        print("\nCrawling and JS Extraction complete.")

    except Exception as e:
        print(f"\n Error crawling {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Spider + JS Analyzer + Extractor (XSS Framework)")
    parser.add_argument("url", help="Website URL to crawl and analyze")

    args = parser.parse_args()
    crawl_website(args.url)
