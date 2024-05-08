import requests
import csv
import time

def get_bitcoin_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']['usd']

def detect_movement(threshold=10, save_interval=60):
    last_price = get_bitcoin_price()
    print("Initial Bitcoin Price:", last_price)
    
    price_history = [[time.time(), last_price]]
    
    while True:
        current_price = get_bitcoin_price()
        price_difference = current_price - last_price
        
        if abs(price_difference) >= threshold:
            movement = "up" if price_difference > 0 else "down"
            print(f"Bitcoin price moved {movement} by ${abs(price_difference)}")
        
        last_price = current_price
        price_history.append([time.time(), current_price])
        
        if len(price_history) % save_interval == 0:
            save_to_csv(price_history)
        
        time.sleep(60)

def save_to_csv(data):
    with open('bitcoin_prices.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    detect_movement()
