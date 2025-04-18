import requests
from bs4 import BeautifulSoup
import difflib

# Function to fetch a page's response
def fetch_response(url, payload=None):
    try:
        if payload:
            # Send a GET request with the payload (as query param for demo)
            response = requests.get(f"{url}?input={payload}")
        else:
            # Normal request
            response = requests.get(url)

        return response.text
    except Exception as e:
        print(f"Error fetching response: {e}")
        return ""

# Function to clean HTML and extract meaningful content (optional)
def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Get text
    text = soup.get_text(separator=' ')

    # Clean whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    return text

# Function to compare two responses
def compare_responses(response1, response2):
    diff = difflib.unified_diff(
        response1.splitlines(),
        response2.splitlines(),
        lineterm=''
    )
    return '\n'.join(diff)

# Main execution function
def detect_xss_deviation(url, test_payload):
    print(f"\n[+] Fetching normal response from {url}...")
    normal_response = fetch_response(url)
    cleaned_normal = clean_html(normal_response)

    print(f"\n[+] Fetching response with payload '{test_payload}'...")
    injected_response = fetch_response(url, payload=test_payload)
    cleaned_injected = clean_html(injected_response)

    print(f"\n[+] Comparing responses for deviations...")
    differences = compare_responses(cleaned_normal, cleaned_injected)

    if differences:
        print("\n[!] Deviations detected:")
        print(differences)
    else:
        print("\n[+] No significant deviations detected.")

# Example Usage:
if __name__ == "__main__":
    target_url = "http://example.com"  # Replace with your testing target URL
    xss_test_payload = "<script>alert('XSS')</script>"
    detect_xss_deviation(target_url, xss_test_payload)
