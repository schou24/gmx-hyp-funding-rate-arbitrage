from gmx_python_sdk.scripts.v2.get.get import GetData
from gmx_python_sdk.scripts.v2.gmx_utils import execute_threading
from gmx_python_sdk.scripts.v2.gmx_utils import ConfigManager

class GetGmxBorrowRate(GetData):
    def __init__(self, chain: str):
        super().__init__(chain)

    def get_borrow_rate(self, market_key: str):
        """
        Generate the dictionary of borrow APR data

        Returns
        -------
        funding_apr : dict
            dictionary of borrow data.

        """
        index_token_address = self.markets.get_index_token_address(
            market_key
        )
        
        self._get_token_addresses(market_key)
        
        output = self._get_oracle_prices( # Not a problem
            market_key,
            index_token_address,
        ).call()
        
        print(output)
        key = self.markets.get_market_symbol(market_key)
                
        self.output["long"][key] = (
            output[1] / 10 ** 28
        ) * 3600
        self.output["short"][key] = (
            output[2] / 10 ** 28
        ) * 3600

        self.log.info(
            (
                "{}\nLong Borrow Hourly Rate: -{:.5f}%\n"
                "Short Borrow Hourly Rate: -{:.5f}%\n"
            ).format(
                key,
                self.output["long"][key],
                self.output["short"][key]
                )
            )

        self.output['parameter'] = "borrow_apr"

        return self.output


if __name__ == "__main__":
    config = ConfigManager(chain='arbitrum')
    config.set_config()
    
    data = GetGmxBorrowRate(config).get_borrow_rate("0x47c031236e19d024b42f8AE6780E44A573170703")
                                                    #ETH: "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336")
                                                    #BTC: "0x47c031236e19d024b42f8AE6780E44A573170703"
                                                    #SOL: "0x09400D9DB990D5ed3f35D7be61DfAEB900Af03C9"
                                                    #XRP: "0x0CCB4fAa6f1F1B30911619f1184082aB4E25813c"
                                                    #LINK: "0x7f1fa204bb700853D36994DA19F830b6Ad18455C"
    print(data)