#!/bin/python3

"""
"""


class Positions:
    """
    Collect a readout of all of our currently held
    positions.  Can either be used in an
    interactive setting or a programmatic setting.
    """


    def __init__( self, client):

        # Make the API call requesting positions.
        self.data = client.get_all_positions()

        # Break up data into individual assets.
        self.assets = []
        for position in self.data:
            self.assets\
                .append( position )

 
    def Qty( self, asset ):
        return asset.qty


    def Side( self, asset ):
        return asset.side


    def Symbol( self, asset ):
        return asset.symbol


    def Exchange( self, asset ):
        return asset.exchange


    def CostBasis( self, asset ):
        return asset.cost_basis


    def AssetClass( self, asset ):
        return asset.asset_class


    def MarketValue( self, asset ):
        return asset.market_value


    def ChangeToday( self, asset ):
        return asset.change_today


    def UnrealizedPL( self, asset ):
        return asset.unrealized_pl


    def CurrentPrice( self, asset ):
        return asset.current_price


    def LastdayPrice( self, asset ):
        return asset.lastday_price


    def AvgEntryPrice( self, asset ):
        return asset.avg_entry_price


    def UnrealizedPLP( self, asset ):
        return asset.Cunrealized_plpc


    def UnrealizedIntradayPL(  self, asset ):
        return asset.unrealized_intraday_pl


    def UnrealizedIntradayPLPC( self, asset ):
        return asset.unrealized_intraday_plpc


