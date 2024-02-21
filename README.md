# CS:GO Empire Trading Script

🚀 This Python script interacts with the CS:GO Empire API to perform various trading operations such as retrieving metadata, getting trading items, placing bids, withdrawing items, and more.

## Requirements
- Python 3.x
- Requests library (`pip install requests`)

## Usage
1. Clone the repository or download the script.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Run the script with the required arguments.

### Command-line Arguments
- `--api-key`: Your CS:GO Empire API key (required).
- `--num-runs`: Number of runs (default: 1).
- `--max-items`: Maximum number of items to bid on (default: 10).
- `--minROI`: Minimum ROI percentage (default: -12).
- `--minROIBUFF`: Minimum ROI buffer percentage (default: -12).
- `--minPRICE`: Minimum price (default: 0).
- `--bid-on-stickers`: Bid on stickers (optional).
- `--bid-on-cases`: Bid on cases (optional).
- `--bid-on-auction`: Bid on auctions (optional).
- `--bid-on-patches`: Bid on patches (optional).

### Example
```bash
python trading_script.py --api-key YOUR_API_KEY --num-runs 3 --max-items 5 --minROI -10 --bid-on-stickers
```

## Note
- Ensure your API key is valid and has the necessary permissions to perform the desired operations.
- It's recommended to review and customize the script according to your specific requirements and trading strategies.
