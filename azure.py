import json

import requests
from pathlib import Path


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


token = "token_here"
subscription_id = "1120c89d-2a5f-4a15-a582-2ea34f0bb5c3"  # from the portal above

url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups?api-version=2024-03-01"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()
for rg in response.json()["value"]:
    print(f"{rg['name']}: {rg['location']}")

    with open(OUTPUT_DIR / "azure_resource_groups.json", "w") as f:
        json.dump(response.json(), f, indent=2)
