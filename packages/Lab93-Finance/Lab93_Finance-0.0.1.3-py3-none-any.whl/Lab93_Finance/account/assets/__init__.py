#!/bin/python3
"""
This program provides simple tools for interacting with your Alpaca.Markets account
in an algorithmic manner.  
"""


# Allow for monitoring the programs runtime.
from logging import getLogger, info, debug, exception

# Utilize the Alpaca-Py SDK to interact with money.
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass


class Assets:
    """
    Curate a list of offerings available on the Alpaca market.

    Currently, we only display the cryptocurrency assets, as there are over
    31,000 us_equity assets maintained by Alpaca.

    To display equity assets, the 31,000 should be broken up alphabetically
    and given by the broker bot individually, piece by piece.
    """


    def __init__( self, client ):
        self.client = client


    def Cryptocurrencies( self ):
        return self.client\
                   .get_all_assets(
                       GetAssetsRequest( asset_class=AssetClass.CRYPTO )
                   )


    def Stocks( self ):
        return self.client\
                   .get_all_assets(
                       GetAssetsRequest( asset_class=AssetClass.STOCKS )
                   )
