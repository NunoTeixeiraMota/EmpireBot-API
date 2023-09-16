import requests
import json

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'be9cffb0b902d7575cf9d5110f6ec71a'

def get_api_response(api_key, page):
    url = f'https://csgoempire.com/api/v2/user/transactions?page={page}'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 responses

        data = response.json()
        if 'data' in data:
            withdrawal_invoices = [item for item in data['data'] if item.get('key') == 'withdrawal_invoices']
            return withdrawal_invoices
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

filename = 'withdrawal_invoices.json'

# Set the number of pages to iterate
num_pages = 50  # You can change this to the number of pages you want to fetch

# Open the JSON file and write the opening bracket of the JSON array
with open(filename, 'w') as file:
    file.write('[')

for page in range(1, num_pages + 1):
    withdrawal_invoices_response = get_api_response(api_key, page)
    if withdrawal_invoices_response is not None:
        with open(filename, 'a') as file:
            if file.tell() != 1:  # Check if it's not the first JSON object (skip the leading '[')
                file.write(", ")  # Add a comma if it's not the first JSON object
            json.dump(withdrawal_invoices_response, file, indent=4)

# Close the JSON array and the file
with open(filename, 'a') as file:
    file.write(']')

print(f"API responses appended to {filename}")
