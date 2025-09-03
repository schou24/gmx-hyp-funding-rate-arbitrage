from numerize import numerize
from utils import _set_paths
import time

from gmx_python_sdk.scripts.v2.get.get_gmx_stats import GetGMXv2Stats
from gmx_python_sdk.scripts.v2.gmx_utils import (
    get_funding_factor_per_period, base_dir, execute_threading,
)
from gmx_python_sdk.scripts.v2.gmx_utils import ConfigManager
from gmx_python_sdk.scripts.v2.get.get import GetData
from gmx_python_sdk.scripts.v2.get.get_oracle_prices import OraclePrices
from gmx_python_sdk.scripts.v2.get.get_markets import Markets
from gmx_python_sdk.scripts.v2.get.get_open_interest import OpenInterest

_set_paths()

class GetGmxInterest(OpenInterest): #fix
    def __init__(self, config):
        self.oracle_prices_dict = OraclePrices( # TODO: fix redundancy
            config.chain
        ).get_recent_prices()
            
        self.markets = Markets(config)

        super().__init__(config=config)
    
    def get_gmx_interest(self, market_key: str):
        long_oi_output_list = []
        short_oi_output_list = []
        long_pnl_output_list = []
        short_pnl_output_list = []
        
        self._filter_swap_markets()
        self._get_token_addresses(market_key)

        index_token_address = self.markets.get_index_token_address(
            market_key
        )

        market = [
            market_key,
            index_token_address,
            self._long_token_address, # ??? CHECK
            self._short_token_address
        ]
        
        min_price = int(
                self.oracle_prices_dict[index_token_address]['minPriceFull']
            )
        
        max_price = int(
                self.oracle_prices_dict[index_token_address]['maxPriceFull']
            )

        prices_list = [min_price, max_price]
        
        try:
            if self.markets.is_synthetic(market_key):
                print("synthetic market")
                decimal_factor = self.markets.get_decimal_factor(
                    market_key,
                )
            else:
                decimal_factor = self.markets.get_decimal_factor(
                    market_key,
                    long=True
                )
        except KeyError:
            decimal_factor = self.markets.get_decimal_factor(
                market_key,
                long=True
                ) 
                
        oracle_factor = (30 - decimal_factor)
        precision = 10 ** (decimal_factor + oracle_factor)
        
        long_oi_with_pnl, long_pnl = self._get_pnl(
            market,
            prices_list,
            is_long=True
        )

        short_oi_with_pnl, short_pnl = self._get_pnl(
            market,
            prices_list,
            is_long=False
        )
        
        long_oi_output_list.append(long_oi_with_pnl)
        short_oi_output_list.append(short_oi_with_pnl)
        long_pnl_output_list.append(long_pnl)
        short_pnl_output_list.append(short_pnl)
            
        long_oi_threaded_output = execute_threading(long_oi_output_list) 
        time.sleep(.2)
        short_oi_threaded_output = execute_threading(short_oi_output_list)
        time.sleep(.2)
        long_pnl_threaded_output = execute_threading(long_pnl_output_list)
        time.sleep(.2)
        short_pnl_threaded_output = execute_threading(short_pnl_output_list)

        
        #short_oi_with_pnl.call()
        #short_pnl.call()
        
        precision = 10 ** 30
        long_value = (long_oi_threaded_output[0] - long_pnl_threaded_output[0]) / precision #long_precision list
        short_value = (short_oi_threaded_output[0] - short_pnl_threaded_output[0]) / precision

        self.log.info(
            f"{self.markets.get_market_symbol(market_key)} Long: ${numerize.numerize(long_value)}"
        )
        self.log.info(
            f"{self.markets.get_market_symbol(market_key)} Short: ${numerize.numerize(short_value)}"
        )

        self.output['long'][self.markets.get_market_symbol(market_key)] = long_value
        self.output['short'][self.markets.get_market_symbol(market_key)] = short_value 
            
        self.output['parameter'] = "open_interest"

        return self.output
        
#def get_open_interest(self, index_token_address=str, market_key=str):
    
    
    
if __name__ == "__main__":
    config = ConfigManager(chain='arbitrum')
    config.set_config()
    
    get_gmx_interest = GetGmxInterest(config)
    print(get_gmx_interest.get_gmx_interest("0x47c031236e19d024b42f8AE6780E44A573170703"))
    #pass
    '''get_gmx_funding_rate = GetGmxFundingRate()
    
    response1 = get_gmx_funding_rate.get_gmx_funding_rate("BTC", True, "0x47c031236e19d024b42f8AE6780E44A573170703", "0x47904963fc8b2340414262125aF798B9655E58Cd")
    response2 = get_gmx_funding_rate.get_gmx_funding_rate("BTC", False, "0x47c031236e19d024b42f8AE6780E44A573170703", "0x47904963fc8b2340414262125aF798B9655E58Cd")
    print("short funding rate: ", response1)
    print("long funding rate: ", response2)'''

