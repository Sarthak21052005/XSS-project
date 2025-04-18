import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define safe test payloads
TEST_PAYLOADS = [
    "<b>test</b>",
    "'safe'",
    "\"harmless\"",
    "<script>alert('test')</script>",
    "1234567890",
    "admin@example.com"
]

def inject_features_into_forms(url):
    try:
        session = requests.Session()
        res = session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        forms = soup.find_all("form")
        print(f"\n📝 Found {len(forms)} form(s) on the page.")

        for i, form in enumerate(forms):
            print(f"\n🔍 Testing Form #{i+1}")

            action = form.get("action")
            method = form.get("method", "get").lower()
            form_url = urljoin(url, action)

            # Create data dictionary for input fields
            data = {}
            inputs = form.find_all("input")
            for input_tag in inputs:
                name = input_tag.get("name")
                input_type = input_tag.get("type", "text")

                if name:
                    if input_type == "email":
                        data[name] = "user@example.com"
                    elif input_type == "password":
                        data[name] = "SafePassword123"
                    else:
                        data[name] = TEST_PAYLOADS[i % len(TEST_PAYLOADS)]

            print(f"📤 Injecting data: {data}")

            # Submit the form
            if method == "post":
                response = session.post(form_url, data=data)
            else:
                response = session.get(form_url, params=data)

            # Check if test payload appears in response
            if any(payload in response.text for payload in TEST_PAYLOADS):
                print("⚠️ Test payload reflected in response! Might be vulnerable.")
            else:
                print("✅ Input seems sanitized or not reflected.")

    except Exception as e:
        print(f"❌ Error during feature injection: {e}")

if __name__ == "__main__":
    url = input("🔗 Enter the target URL: ")
    inject_features_into_forms(url)
