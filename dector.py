import requests
import difflib
import time

# Load payloads from file
def load_payloads(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Send HTTP GET request
def send_request(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code, response.text, len(response.content)
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None, "", 0

# Compare two responses using difflib and content length
def compare_responses(normal_text, injected_text, normal_len, injected_len):
    diff_ratio = difflib.SequenceMatcher(None, normal_text, injected_text).ratio() * 100
    length_diff = abs(injected_len - normal_len)
    length_percent_change = (length_diff / normal_len) * 100 if normal_len else 0
    return diff_ratio, length_percent_change

# Apply discovery rules
def detect_anomalies(payload, status_code, diff_ratio, length_change):
    findings = []

    if status_code != 200:
        findings.append(f"⚠️ Status code changed to {status_code}")

    if length_change > 30:
        findings.append(f"⚠️ Content length changed by {length_change:.2f}%")

    if diff_ratio < 95:
        findings.append(f"⚠️ HTML similarity dropped to {diff_ratio:.2f}%")

    if findings:
        print(f"\n🚨 Possible XSS detected with payload: {payload}")
        for f in findings:
            print(f"- {f}")

# Main scanning function
def scan(url, payloads):
    print(f"📡 Scanning {url} with {len(payloads)} payloads...")

    base_status, base_text, base_len = send_request(url)

    if base_status is None:
        print("❌ Failed to get base response.")
        return

    for payload in payloads:
        # Inject payload via query parameter 'input'
        test_url = f"{url}?input={payload}"
        print(f"🔍 Testing payload: {payload}")

        status, text, content_len = send_request(test_url)
        if status is None:
            continue

        diff_ratio, length_change = compare_responses(base_text, text, base_len, content_len)
        detect_anomalies(payload, status, diff_ratio, length_change)

        time.sleep(1)  # polite delay

if __name__ == "__main__":
    target_url = input("🌐 Enter target URL (without params, e.g., http://example.com/page): ").strip()
    payloads = load_payloads("payloads.txt")
    scan(target_url, payloads)
