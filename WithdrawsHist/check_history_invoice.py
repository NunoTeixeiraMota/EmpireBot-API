import json
import sys

def load_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON from '{filename}': {e}")
        sys.exit(1)

if len(sys.argv) != 3:
    print("Usage: python confirm.py <Items.json> <Invoices.json>")
    sys.exit(1)

items_filename = sys.argv[1]
invoices_filename = sys.argv[2]

items_data = load_json_file(items_filename)
invoices_data = load_json_file(invoices_filename)

# Create sets for tradeoffer_ids from items data and invoices data
tradeoffer_ids_items = set(item['data']['tradeoffer_id'] for item in items_data if 'data' in item)
tradeoffer_ids_invoices = set()

# Create a dictionary to store the data associated with trade offer IDs found in invoices
invoice_data_dict = {}

# Iterate through the lists of invoices and add tradeoffer_ids and their data to the dictionary
for invoice_list in invoices_data:
    for invoice in invoice_list:
        if 'data' in invoice and 'metadata' in invoice['data']:
            tradeoffer_id = invoice['data']['metadata']['deposit_id']
            tradeoffer_ids_invoices.add(tradeoffer_id)
            invoice_data_dict[tradeoffer_id] = invoice

# Find the common trade offer IDs between items and invoices
common_tradeoffer_ids = tradeoffer_ids_items.intersection(tradeoffer_ids_invoices)

# Print the data associated with the common trade offer IDs
if common_tradeoffer_ids:
    print("Data associated with Trade Offer IDs found in both Items and Invoices:")
    for tradeoffer_id in common_tradeoffer_ids:
        print(f"Trade Offer ID: {tradeoffer_id}")
        print(json.dumps(invoice_data_dict[tradeoffer_id], indent=4))  # Print the associated data
else:
    print("No common Trade Offer IDs found in both Items and Invoices.")
