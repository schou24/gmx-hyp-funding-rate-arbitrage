from utils import _set_paths
from gmx_python_sdk.scripts.v2.get.get_gmx_stats import GetGMXv2Stats
from gmx_python_sdk.scripts.v2.gmx_utils import (
    get_funding_factor_per_period, base_dir, execute_threading,
)
from gmx_python_sdk.scripts.v2.gmx_utils import ConfigManager
from gmx_python_sdk.scripts.v2.get.get import GetData
from gmx_python_sdk.scripts.v2.get.get_oracle_prices import OraclePrices
from gmx_python_sdk.scripts.v2.get.get_markets import Markets

from get_gmx_interest import GetGmxInterest

_set_paths()

class GetGmxFundingRate(GetGMXv2Stats): #fix
    def __init__(self):
        self.config = ConfigManager(chain='arbitrum')
        self.config.set_config()
        self.markets = Markets(self.config)

        super().__init__(config=self.config, to_json=False, to_csv=False)
    
    def get_gmx_funding_rate(self, symbol: str, isLong: bool, market_key: str, index_token_address: str):

        data = GetData(config=self.config)
        data._get_token_addresses(market_key)     
                
        output = data._get_oracle_prices(
                    market_key,
                    index_token_address,
                ).call()
        
        get_open_interest = GetGmxInterest(self.config)
        open_interest = get_open_interest.get_gmx_interest(market_key)
    
        market_info_dict = {
                    "is_long_pays_short": output[4][0],
                    "funding_factor_per_second": output[4][1]
                }

        return get_funding_factor_per_period(
                    market_info_dict,
                    isLong,
                    3600,
                    open_interest['long'][symbol] * 10 ** 30,
                    open_interest['short'][symbol] * 10 ** 30
                )    
    
    
if __name__ == "__main__":
    get_gmx_funding_rate = GetGmxFundingRate()
    
    response1 = get_gmx_funding_rate.get_gmx_funding_rate("BTC", True, "0x47c031236e19d024b42f8AE6780E44A573170703", "0x47904963fc8b2340414262125aF798B9655E58Cd")
    response2 = get_gmx_funding_rate.get_gmx_funding_rate("BTC", False, "0x47c031236e19d024b42f8AE6780E44A573170703", "0x47904963fc8b2340414262125aF798B9655E58Cd")
    print("short funding rate: ", response1)
    print("long funding rate: ", response2)

