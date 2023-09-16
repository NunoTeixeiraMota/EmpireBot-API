import argparse
import json
import requests
import subprocess
command = ["python", "FTP\extract_full_info_from_withdrawn.py"]
subprocess.run(command)

FullInfoWithdrawn = "FullInfoWithdrawn.json"

# Define the argument parser
parser = argparse.ArgumentParser(description="Parse JSON files and calculate profit.")
parser.add_argument("api_key", type=str, help="Your API Key for csgoempire.com")

# Parse the command-line arguments
args = parser.parse_args()

# Try to open and read the withdrawn invoice JSON file
try:
    with open(FullInfoWithdrawn, "r") as withdrawn_file:
        withdrawn_invoice = json.load(withdrawn_file)
except FileNotFoundError:
    print(f"Error: The file '{FullInfoWithdrawn}' does not exist.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to parse JSON from '{FullInfoWithdrawn}'.")
    exit(1)

# Define the URL for fetching the inventory data
inventory_url = 'https://csgoempire.com/api/v2/trading/user/inventory'

# Prepare the headers for the GET request
headers = {
    "Authorization": f"Bearer {args.api_key}"
}

# Send a GET request to fetch the inventory data
response = requests.get(inventory_url, headers=headers)

if response.status_code == 200:
    # Parse the JSON response
    inventory_data = response.json()
    
    # Create a dictionary to store the items by market_name
    inventory_by_name = {item["market_name"]: item for item in inventory_data["data"]}
    # Convert withdrawn_invoice to a dictionary if it's a list
    if isinstance(withdrawn_invoice, list):
        withdrawn_invoice = {item["market_name"]: item for item in withdrawn_invoice}
    # Iterate through items that exist in both files and calculate profit
    for market_name in withdrawn_invoice.keys() & inventory_by_name.keys():
        withdrawn_item = withdrawn_invoice[market_name]
        inventory_item = inventory_by_name[market_name]

        bought_at = withdrawn_item.get("bought_at")
        market_value = inventory_item.get("market_value")
        item_id = inventory_item.get("id")  # ID required for the POST request

        if bought_at is not None and market_value is not None:
            profit = market_value - bought_at
            profit_percentage = (profit / bought_at) * 100

            if profit_percentage > 12:
                print(f"Market name: {market_name}, Profit: {profit}, Profit Percentage: {profit_percentage:.2f}%")

                """ # Prepare the POST request data
                payload = {
                    "items": [{"id": item_id, "coin_value": int(market_value)}]
                }

                # Send the POST request
                response = requests.post('https://csgoempire.com/api/v2/trading/deposit', headers=headers, json=payload)

                if response.status_code == 200:
                    print("Successfully deposited item.")
                else:
                    print(f"Failed to deposit item. Status Code: {response.status_code}") """
else:
    print(f"Failed to fetch inventory data. Status Code: {response.status_code}")