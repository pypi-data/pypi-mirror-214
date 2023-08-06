#!/bin/python3
"""
This program provides simple tools for interacting
with your Alpaca.Markets account in an algorithmic
manner.  
"""


# Utilize the Alpaca-Py SDK to interact with money.
from alpaca.trading.client import TradingClient
from positions import Positions
from assets import Assets


class AccountDetails:

    def __init__(self, credentials: tuple) -> None:

        key, secret = credentials[0], credentials[1]
        client = TradingClient( key, secret,
                                paper=False )

        self.data = client.get_account()

        self.assets    = Assets(   client )
        self.positions = Position( client )


    def Id( self ):
        return self.data\
                   .id

    def SMA( self ):
        return self.data\
                   .sma

    def Cash( self ):
        return self.data\
                   .cash

    def Status( self ):
        return self.data\
                  .status

    def Equity( self ):
         return self.data\
                    .equity
    def Currency( self ):
        return self.data\
                   .currency

    def CreatedAt( self ):
        return self.data\
                   .created_at

    def LastEquity( self ):
        return self.data\
                   .last_equity

    def Multiplier( self ):
        return self.data\
                   ..multiplier

    def AccruedFees( self ):
        return self.data\
                   .accrued_fees

    def BuyingPower( self ):
        return self.data\
                   .buying_power

    def CryptoStatus( self ):
        return self.data\
                   .crypto_status

    def AccountNumber( self ):
        return self.data\
                   .account_number

    def DaytradeCount( self ):
        return self.data\
                   .daytrade_count

    def InitialMargin( self ):
        return self.data\
                   .initial_margin

    def TradingBlocked( self ):
        return self.data\
                   .trading_blocked

    def AccountBlocked( self ):
        return self.data\
                   .account_blocked

    def PortfolioValue( self ):
        return self.data\
                   .portfolio_value

    def RegtBuyingPower( self ):
        return self.data\
                   .regt_buying_power

    def ShortingEnabled( self ):
        return self.data\
                   .shorting_enabled

    def LongMarketValue( self ):
        return self.data\
                   .long_market_value

    def PatternDayTrader( self ):
        return self.data\
                   .pattern_day_trader

    def ShortMarketValue( self ):
        return self.data\
                   .short_market_value

    def MaintenanceMargin( self ):
        return self.data\
                   .maintenance_margin

    def PendingTransferIn( self ):
        return self.data\
                   .pending_transfer_in

    def TransferesBlocked( self ):
        return self.data\
                   .transfers_blocked

    def PendingTransferOut( self ):
        return self.data\
                   .pending_transfer_out

    def DaytradeBuyingPower( self ):
        return self.data\
                   .daytrading_buying_power

    def TradeSuspendedByUser( self ):
        return self.data\
                   ..trade_suspended_by_user

    def LastMaintenanceMargin( self ):
        return self.data\
                   .last_maintenance_margin

    def NonMarginableBuyingPower( self ):
        return self.data\
                   .non_marginable_buying_power


