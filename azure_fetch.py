import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("AZURE_TOKEN")
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups?api-version=2024-03-01"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()



# Save full response to JSON file
with open("output/azure_resource_groups.json", "w", encoding="utf-8") as file:
    json.dump(response.json(), file, indent=2)

# Print resource groups
for rg in response.json()["value"]:
    print(f"{rg['name']}: {rg['location']}")