import pandas as pd
import time
import os
import random

def simulate_market():
    while True:
        # Simulate price fluctuations for Wheat
        price_data = [
            {"commodity": "Wheat", "grade": "FAQ", "price": random.uniform(24, 26)},
            {"commodity": "Wheat", "grade": "UG", "price": random.uniform(18, 20)},
            {"commodity": "Wheat", "grade": "Sample", "price": 12.0}
        ]
        df = pd.DataFrame(price_data)
        df.to_csv("data/mandi_prices/live_feed.csv", index=False)
        print("Market Prices Updated...")
        time.sleep(5) # Update every 5 seconds

if __name__ == "__main__":
    simulate_market()