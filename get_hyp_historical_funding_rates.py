import requests
import pytz
import time
from datetime import datetime
import json 

import csv

# Function to Retrieve data from Hyperliquid API
base_url = "https://api.hyperliquid.xyz/info"
headers = {
    "Content-Type":"application/json"
}

def get_funding_rate(coin, startDatetime):
    data = {
        "type":"fundingHistory",
        "coin":coin,
        "startTime": int(startDatetime),
        "endTime": int(startDatetime) + 86400000 
    } 
    response = requests.post(base_url, headers=headers, json=data)
    return response

starting_date_str = '2024-02-21 00:00:00' # First date for which rates are retrieved
starting_date = datetime.fromisoformat(starting_date_str).astimezone(pytz.utc).timestamp() * 1000 # original date in ms
coins = ("BTC", "SOL", "XRP", "LINK", "ETH", "HYPER", "AVAX") # Tuple of currencies used

csv_file_name = 'fundingrateData.csv' #NAME OF OUTPUT FILE
with open('fundingrateData.csv', 'w', newline='') as csvfile:
    fieldnames = ['Date', 'BTC', 'SOL', 'XRP', 'LINK', 'ETH', 'HYPER', 'AVAX'] # adjust if using different currrencies
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
                
for j in range(int((datetime.now().astimezone(pytz.utc).timestamp() * 1000 - starting_date) / 86400000)):#86400000)):
    time.sleep(2) #prevent timeout
    
    allRates = []
    for i in range (len(coins)):
        time.sleep(2) # Prevent timeout
        response = get_funding_rate(coins[i], starting_date +  86400000 * j)
        if response.ok:
            data = response.json()
            total_funding_rate = 0.0
            
            for entry in data: # 24 hourly funding rates
                total_funding_rate += float(entry['fundingRate'])
                
            allRates.append(-1 * total_funding_rate)
        else:
            print("Error:", response.status_code, response.text)

    with open('fundingrateData.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        date_from_timestamp = datetime.fromtimestamp((starting_date + 86400000 * j) / 1000)
        date = date_from_timestamp.astimezone(pytz.timezone('America/New_York')).date()
        
        writer.writerow({'Date':date , 'BTC': allRates[0], 'SOL': allRates[1], 'XRP': allRates[2], 'LINK': allRates [3], 'ETH': allRates[4], 'HYPER': allRates[5], 'AVAX': allRates[6]})
    