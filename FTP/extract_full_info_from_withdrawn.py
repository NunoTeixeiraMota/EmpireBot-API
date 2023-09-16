import json

# Hardcoded file paths
withdrawn_file_path = "FTP\Withdrawn_Items.json"
extracted_file_path = "FTP\extracted_items.json"

# Read data from JSON files
try:
    with open(withdrawn_file_path, "r") as withdrawn_file:
        withdrawn_items = json.load(withdrawn_file)
except FileNotFoundError:
    print(f"Error: File '{withdrawn_file_path}' not found.")
    exit(1)

try:
    with open(extracted_file_path, "r") as extracted_file:
        extracted_items = json.load(extracted_file)
except FileNotFoundError:
    print(f"Error: File '{extracted_file_path}' not found.")
    exit(1)

matched_items = []

for withdrawn_item in withdrawn_items:
    tradeoffer_id = withdrawn_item["data"]["tradeoffer_id"]
    for extracted_item in extracted_items:
        if tradeoffer_id == extracted_item["id"]:
            # Add "bought_at" with the value of "coin_value"
            extracted_item["bought_at"] = withdrawn_item["data"]["coin_value"]
            matched_items.append(extracted_item)

output_filename = "FullInfoWithdrawn.json"  # Assuming you want to save it in the parent directory
with open(output_filename, "w") as output_file:
    json.dump(matched_items, output_file, indent=4)

print(f"Matched items with 'bought_at' written to '{output_filename}'")
