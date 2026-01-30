import requests
import csv
import time
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

def extract_domain(domain):
    if not domain.startswith("http"):
        domain = "https://" + domain
    return urlparse(domain).netloc.replace("www.", "")

def brand_name(domain):
    return domain.split(".")[0].title()

def fetch_and_save_csv(domains, output="uae_company_list.csv"):
    results = []
    seen = set()

    for d in domains:
        domain = extract_domain(d)
        brand = brand_name(domain)

        url = "https://api.hunter.io/v2/domain-search"
        params = {
            "domain": domain,
            "api_key": HUNTER_API_KEY,
            "type": "personal"
        }

        try:
            r = requests.get(url, params=params, timeout=20)
            data = r.json()
            emails = data.get("data", {}).get("emails", [])

            if not emails:
                results.append({
                    "Brand": brand,
                    "Domain": domain,
                    "Email": ""
                })

            for e in emails:
                email = e.get("value")
                if email and email not in seen:
                    seen.add(email)
                    results.append({
                        "Brand": brand,
                        "Domain": domain,
                        "Email": email
                    })

            time.sleep(1)

        except Exception as ex:
            print("Hunter error:", ex)

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Brand", "Domain", "Email"])
        writer.writeheader()
        writer.writerows(results)

    return output
