import re

suspicious_domains = [
    "bit.ly",
    "tinyurl",
    ".ru",
    ".xyz",
    "free-gift",
    "secure-login"
]


def check_url(email_text):

    found_urls = re.findall(r'https?://\S+', email_text)

    threat = False

    reasons = []

    for url in found_urls:
        for domain in suspicious_domains:

            if domain in url:

                threat = True

                reasons.append(f"Suspicious URL detected: {url}")

    return threat, reasons