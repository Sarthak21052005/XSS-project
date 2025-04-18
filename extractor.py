import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

def extract_scripts_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <script> tags (inline and external)
        scripts = soup.find_all('script')
        print(f"\n✅ Found {len(scripts)} <script> tags.")

        output_dir = "extracted_js"
        os.makedirs(output_dir, exist_ok=True)

        # Iterate through all the <script> tags
        for idx, script in enumerate(scripts):
            # Check if it's an inline script
            js_code = script.string
            if js_code:
                filename = os.path.join(output_dir, f"inline_script_{idx+1}.js")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(js_code)
                print(f"✅ Saved inline JavaScript to: {filename}")
            
            # Check if it's an external script (with src attribute)
            elif script.get('src'):
                external_url = script['src']
                external_url = urllib.parse.urljoin(url, external_url)  # Handle relative URLs

                # Download the external script
                try:
                    ext_response = requests.get(external_url)
                    ext_filename = os.path.join(output_dir, f"external_script_{idx+1}.js")
                    with open(ext_filename, "wb") as f:
                        f.write(ext_response.content)
                    print(f"✅ Saved external JavaScript to: {ext_filename}")
                except Exception as ex:
                    print(f"❌ Error downloading external script {external_url}: {ex}")

            else:
                print(f"⚠️ Skipped empty or malformed script tag {idx+1}")

    except Exception as e:
        print(f"❌ Error: {e}")

# Example usage:
if __name__ == "__main__":
    url = input("🔗 Enter the website URL: ")
    extract_scripts_from_url(url)
