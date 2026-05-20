import requests
import json
import os

token = "token here"  # az account get-access-token --query accessToken -o tsv
subscription_id = "1120c89d-2a5f-4a15-a582-2ea34f0bb5c3"  # from the portal above

url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups?api-version=2024-03-01"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

data = response.json()

os.makedirs("output", exist_ok=True)

with open("output/azure_resource_groups.json", "w") as f:
    json.dump(data, f, indent=2)

for rg in response.json()["value"]:
    print(f"{rg['name']}: {rg['location']}")