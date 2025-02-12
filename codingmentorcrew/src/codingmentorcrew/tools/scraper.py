import requests
import json

# Browserless API Key
BROWSERLESS_KEY = "RlD0rhXdoT6pvHd2cc29ca78c503a38beb97bf5254"

def scrape_page(url):
    """Scrape a webpage using Browserless and return the content."""
    browserless_url = f"https://chrome.browserless.io/content?token={BROWSERLESS_KEY}"
    payload = json.dumps({"url": url})
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(browserless_url, data=payload, headers=headers)
    
    if response.status_code == 200:
        return response.text  # Extracted page content
    else:
        return f"Error scraping {url}"