from gmx_python_sdk.scripts.v2.gmx_utils import ConfigManager
from gmx_python_sdk.scripts.v2.get.get_gmx_stats import GetGMXv2Stats

from get_hyp_funding_rate import GetHypFundingRate
from get_gmx_funding_rate import GetGmxFundingRate
from get_gmx_borrow_rate import GetGmxBorrowRate

class GetNetFundingRate:
    def __init__(self, coin=str, market_key=str, index_token_address=str):
        config = ConfigManager(chain='arbitrum')
        config.set_config()
        
        get_gmx_funding_rate = GetGmxFundingRate() # use inheritance later
        get_hyp_funding_rate = GetHypFundingRate()
        get_gmx_borrow_rate = GetGmxBorrowRate(config)
        
        self.hyp_long = 12.0 * 365.0 * get_hyp_funding_rate.get_hyp_funding_rate(coin) # DOUBLE CHECK IF THIS IS RIGHT // Convert to annualized and divide by 2.0
        self.hyp_short = -1.0 * self.hyp_long
        
        gmx_long_funding = get_gmx_funding_rate.get_gmx_funding_rate(coin, True, market_key, index_token_address)
        gmx_short_funding = get_gmx_funding_rate.get_gmx_funding_rate(coin, False, market_key, index_token_address)
        
        gmx_long_borrow = get_gmx_borrow_rate.get_borrow_rate(market_key)['long'][coin]
        gmx_short_borrow = get_gmx_borrow_rate.get_borrow_rate(market_key)['short'][coin]
        
        print(gmx_long_funding)
        print(gmx_short_funding)
        
        print(gmx_long_borrow)
        print(gmx_short_borrow)

        self.gmx_long = 12.0 * 365.0 * (gmx_long_funding - gmx_long_borrow) # Convert to annualized and divide by 2.0
        self.gmx_short = 12.0 * 365.0 * (gmx_short_funding - gmx_short_borrow)
        
    def get_gmx_long_gmx_short(self):
        return self.gmx_long + self.gmx_short
    
    def get_gmx_long_hyp_short(self):
        return self.gmx_long + self.hyp_short
    
    def get_hyp_long_gmx_short(self):
        return self.hyp_long + self.gmx_short 
        
if __name__ == "__main__":
   get_net_funding_rate = GetNetFundingRate("BTC", "0x47c031236e19d024b42f8AE6780E44A573170703", "0x47904963fc8b2340414262125aF798B9655E58Cd")
  
    
