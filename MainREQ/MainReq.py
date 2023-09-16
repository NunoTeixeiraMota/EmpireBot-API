import requests
import json
import argparse
import time
from time import sleep
currentbalance = 0

def get_metadata(api_key, filename):
    url = 'https://csgoempire.com/api/v2/metadata/socket'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
        else:
            print(f"Get metadata Request failed with status code: {response.status_code}")
            print("Response content:")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return data
def get_auction_items(api_key, filename,mineroibuff,minPRICE):
    url = 'https://csgoempire.com/api/v2/trading/items'
    params = {
        'per_page': 100,
        'page': 1,
        'price_max_above': -12,
        'sort': 'desc',
        'order': 'market_value',
        'auction':  "yes",
        'above_recomended_price': mineroibuff
    }
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            items = []
            for item in data["data"]:
                item_info = {
                    "market_name": item["market_name"],
                    "id": item["id"],
                    "market_value": item["market_value"],
                    "purchase_price": item["purchase_price"],
                    "auction_highest_bid" : item["auction_highest_bid"],
                    "custom_price_percentage": item["custom_price_percentage"],
                    "price_is_unreliable": item['price_is_unreliable']
                }
                if item_info["price_is_unreliable"] is False & item_info["purchase_price"] > minPRICE:
                    items.append(item_info)
            with open(filename, 'a') as file:
                json.dump(items, file, indent=4)
        else:
            print(f"Get auction Items Request failed with status code: {response.status_code}")
            print("Response content:")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return items
def get_trading_items(api_key, filename,minroi,mineroibuff,minPRICE):
    url = 'https://csgoempire.com/api/v2/trading/items'
    params = {
        'per_page': 100,
        'page': 1,
        'price_max_above': minroi,
        'sort': 'desc',
        'order': 'market_value',
        'auction': "no",
        'above_recomended_price': mineroibuff
    }
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
    
        if response.status_code == 200:
            data = response.json()
            items = []
            with open(filename, 'r') as file:
                # Load existing data from the file, if it exists
                existing_items = json.load(file)
            
            # Iterate through the items in the response
            for item in data["data"]:
                item_info = {
                    "market_name": item["market_name"],
                    "id": item["id"],
                    "market_value": item["market_value"],
                    "purchase_price": item["purchase_price"],
                    "custom_price_percentage": item["custom_price_percentage"],
                    "above_recomended_price": item["above_recommended_price"], 
                    "price_is_unreliable": item['price_is_unreliable']

                }
                
                # Check if the item with the same ID already exists in the file
                if not any(existing_item["id"] == item_info["id"] for existing_item in existing_items) :
                    if (item_info["price_is_unreliable"] is False) & (item_info["purchase_price"] > minPRICE):
                        items.append(item_info)

            # Append the new items to the existing data
            existing_items.extend(items)
            
            # Write the updated data back to the file
            with open(filename, 'w') as file:
                json.dump(existing_items, file, indent=4)
        else:
            print(f"Get trading items Request failed with status code: {response.status_code}")
            print("Response content:")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return items
def place_bid(api_key, weapon_id, bid_value,filename,custom_price_percentage):
    url = f'https://csgoempire.com/api/v2/trading/deposit/{weapon_id}/bid'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'bid_value': bid_value
    }
    currentbalance = get_current_balance(api_key,outputmetadata_filename="extracted_metadata.json")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()

        if response.status_code == 200:
            with open(filename, 'a') as file:
                response_data['data']['bid_value'] = bid_value  # Add coin_value to the response data
                response_data['data']['market'] = custom_price_percentage 
                json.dump(response_data, file, indent=4)
            return response_data
        else:
            message = "Bid placement failed | " + response_data['message']
            print(message)
    except Exception as e:
        return {"success": False, "message": str(e)}
def post_deposit_bid(api_key, deposit_id, bid_value, filename):
    url = f'https://csgoempire.com/api/v2/trading/deposit/{deposit_id}/bid'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'bid_value': bid_value
    }

    try:
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()

        if response.status_code == 200:
            response_data = response.json()
            with open(filename, 'a') as file:
                json.dump(response_data, file, indent=4)
            return response_data
        else:
            if not response_data['success']:
                message = "Failed | " + response_data['message']
                print(message)
            return None
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
def get_current_balance(api_key, outputmetadata_filename):
    metadata = get_metadata(api_key, outputmetadata_filename)

    if metadata:
        user_data = metadata.get("user")
        if user_data:
            balance = user_data.get("balance")
            if balance:
                return float(balance)

    return None


def withdraw_item(api_key, item_id, coin_value, filename, custom_price_percentage):
    url = f'https://csgoempire.com/api/v2/trading/deposit/{item_id}/withdraw'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'coin_value': coin_value
    }
    current_balance = get_current_balance(api_key, outputmetadata_filename="extracted_metadata.json")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Prepare the response information dictionary
        response_info = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'data': response.json()
        }

        if response.status_code == 200:
            current_balance = current_balance - coin_value
            with open(filename, 'a') as file:
                response_info['coin_value'] = coin_value  # Add coin_value to the response data
                response_info['custom_price_percentage'] = custom_price_percentage 
                json.dump(response_info, file, indent=4)
            return response_info
        else:
            message = "Withdrawal failed | " + response_info['data']['message']
            print(message)
    
    except Exception as e:
        return {"success": False, "message": str(e)}

def main():
    parser = argparse.ArgumentParser(description='CS:GO Empire Trading Script')
    parser.add_argument('--api-key', required=True, help='Your API key')
    parser.add_argument('--num-runs', type=int, default=1, help='Number of runs')
    parser.add_argument('--max-items', type=int, default=10, help='Max Items to Bid On')
    parser.add_argument('--minROI', type=int, default=-12, help='Minimum ROI %')
    parser.add_argument('--minROIBUFF', type=int, default=-12, help='Minimum ROI buff %')
    parser.add_argument('--minPRICE', type=int, default=0, help='Minimum PRICE')
    parser.add_argument('--bid-on-stickers', action='store_true', help='Bid on Stickers')
    parser.add_argument('--bid-on-cases', action='store_true', help='Bid on Cases')
    parser.add_argument('--bid-on-auction', action='store_true', help='Bid on auctions')
    parser.add_argument('--bid-on-patches', action='store_true', help='Bid on patches')
    args = parser.parse_args()
    currentbalance = get_current_balance(args.api_key,outputmetadata_filename="extracted_metadata.json")
    print(args.minROI)
    for _ in range(args.num_runs):
        itemsAuction = []
        items = []
        sleep(2.5)
        print("get_trading_items")
        items = get_trading_items(args.api_key, 'extracted_items.json',minroi=args.minROI,mineroibuff=args.minROIBUFF,minPRICE=args.minPRICE)
        print("Current Balance:",currentbalance)
        if items is not None:
            for index, item in enumerate(items):
                if(item['purchase_price']<currentbalance):
                    if(args.bid_on_cases) and (args.bid_on_stickers) and index < args.max_items:
                        print(f"Purchased {item['market_name']} | for {item['purchase_price']} Coins")
                        sleep(2.5)
                        withdraw_item(args.api_key, item_id=item["id"], coin_value=item["purchase_price"],filename="Withdrawn_Items.json",custom_price_percentage=item['custom_price_percentage'])
                    if (not args.bid_on_cases)and (args.bid_on_stickers) and index < args.max_items:
                        if "case" not in item["market_name"].lower():
                            currentbalance = get_current_balance(args.api_key,outputmetadata_filename="extracted_metadata.json")
                            sleep(2.5)
                            print(f"Purchased {item['market_name']} | for {item['purchase_price']} Coins")
                            withdraw_item(args.api_key, item_id=item["id"], coin_value=item["purchase_price"],filename="Withdrawn_Items.json",custom_price_percentage=item['custom_price_percentage'])
                    if ( args.bid_on_cases) and (not args.bid_on_stickers) and index < args.max_items:
                        if "sticker" not in item["market_name"].lower():    
                            currentbalance = get_current_balance(args.api_key,outputmetadata_filename="extracted_metadata.json") 
                            sleep(2.5)
                            print(f"Purchased {item['market_name']} | for {item['purchase_price']} Coins")
                            withdraw_item(args.api_key, item_id=item["id"], coin_value=item["purchase_price"],filename="Withdrawn_Items.json",custom_price_percentage=item['custom_price_percentage'])
                    if ( not args.bid_on_cases) and (not args.bid_on_stickers) and index < args.max_items:
                        if "sticker" not in item["market_name"].lower() and "case" not in item["market_name"].lower() & "patch" not in item["market_name"].lower():
                            currentbalance = get_current_balance(args.api_key,outputmetadata_filename="extracted_metadata.json")
                            sleep(2.5)
                            print(f"Purchased {item['market_name']} | for {item['purchase_price']} Coins")
                            withdraw_item(args.api_key, item_id=item["id"], coin_value=item["purchase_price"],filename="Withdrawn_Items.json",custom_price_percentage=item['custom_price_percentage'])
        if(args.bid_on_auction):
            sleep(2.5)
            print("get_auction_items")
            itemsAuction = get_auction_items(args.api_key,'extracted_auction.json',mineroibuff=args.minROIBUFF,minPRICE=args.minPRICE) 
            if itemsAuction is not None:
                sleep(2.5)
                print("Current Balance:",currentbalance)
                for item in itemsAuction:
                    if item["auction_highest_bid"] is not None:
                                if(item['purchase_price']<currentbalance):
                                    currentbalance = get_current_balance(args.api_key,outputmetadata_filename="extracted_metadata.json")
                                    print(f"Bidded on {item['market_name']} | for {item['purchase_price']} Coins")
                                    sleep(2.5)
                                    print("place_bid")
                                    place_bid(args.api_key,weapon_id=item["id"],bid_value=item["auction_highest_bid"],filename="Bidded_Items.json",custom_price_percentage=item['custom_price_percentage'])
if __name__ == "__main__":
    main()