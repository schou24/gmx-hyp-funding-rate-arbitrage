import requests
import datetime
import json

class GetHypFundingRate: 
    def __init__(self):
        self.base_url = "https://api.hyperliquid.xyz/info"

        self.headers = {
            "Content-Type":"application/json"
        }

    def get_hyp_funding_rate(self, coin):
        data = {
            "type":"fundingHistory",
            "coin":coin,
            "startTime": int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000) - 3600000,  # 1 hours ago
        } 
        response = requests.post(self.base_url, headers=self.headers, json=data)
        return -1.0 * float(response.json()[0]['fundingRate']) # add a failsafe here if needed

if __name__ == "__main__":
    get_hyp_funding_rate = GetHypFundingRate()
    response = get_hyp_funding_rate.get_hyp_funding_rate("BTC")
    print(response)
