import re
from html import unescape

# Encoded variants of '<'
ENCODED_VARIANTS = {
    r"\\x3C", r"\\<", r"\\u003c", r"%3C",
    r"&#x3c;", r"&#X3c;", r"&#x03c;", r"&#060;", r"&#0060;",
    "&lt;", "&LT;", "+ADw-"
}

# Rules table (simplified from Table 6, 7)
RULES = {
    'tag_text': {
        'expected': (1, 0),
        'attacks': [
            {'pattern': r"<script>alert\(\"XSS\"\)</script>", 'result': (2, 0)},
        ]
    },
    'attribute_value': {
        'expected': (1, 1),
        'attacks': [
            {'pattern': r"id1\" onfocus=\"foo\(\)\"", 'result': (1, 2)},
        ]
    }
}

def detect_encoded_injection(js_code: str) -> bool:
    """
    Detects if JavaScript code contains obfuscated variants of "<"
    """
    for variant in ENCODED_VARIANTS:
        if re.search(variant, js_code, re.IGNORECASE):
            return True
    return False

def detect_xss_deviation(js_code: str, context_type: str) -> tuple:
    """
    Detects deviations based on rule set
    """
    expected = RULES.get(context_type, {}).get('expected')
    for attack in RULES.get(context_type, {}).get('attacks', []):
        if re.search(attack['pattern'], js_code):
            return attack['result']
    return expected

def analyze_http_response(response_text: str) -> dict:
    """
    Core analysis function for HTTP response content.
    """
    results = {
        "encoded_variants_detected": detect_encoded_injection(response_text),
        "tag_context_result": detect_xss_deviation(response_text, "tag_text"),
        "attribute_context_result": detect_xss_deviation(response_text, "attribute_value"),
    }
    return results
