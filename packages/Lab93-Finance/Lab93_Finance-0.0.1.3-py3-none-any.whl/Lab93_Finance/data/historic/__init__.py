#!/bin/python3

# Import Alpaca-Py handling for cryptocurrency.
from alpaca.data.historical \
    import CryptoHistoricalDataClient as CryptoData

from alpaca.data.requests \
    import CryptoBarsRequest          as CryptoBars


# Import Alpaca-Py handling for stocks.
from alpaca.data.historical \
    import StockHistoricalDataClient as StocksData

from alpaca.data.requests \
    import StockBarsRequest          as StocksBars


# Time and Date related functionality.
from alpaca.data.timeframe import TimeFrame

# In-House tools for dealing with things.
from Lab93Cryptogram import CryptographyMethodsAPI




class Queries:
    def __init__( self, credentials, start, end,
                  symbols:   list = ["BTC/USD"],
                  timeframe: str  = "hour",
                  CRYPTO:    bool = True        ):
        """
        """

        self.CRYPTO = CRYPTO
        self.timeframe = timeframe


        if   timeframe.lower() == "second":
            timeframe = TimeFrame.Second

        elif timeframe.lower() == "minute":
            timeframe = TimeFrame.Minute

        elif timeframe.lower() == "hour":
            timeframe = TimeFrame.Hour

        elif timeframe.lower() == "day":
            timeframe = TimeFrame.Day

        elif timeframe.lower() == "week":
            timeframe = TimeFrame.Week

        elif timeframe.lower() == "month":
            timeframe = TimeFrame.Month

        else:
            raise InvalidTimeframe( timeframe )
    
    
        # Use crypto client if CRYPTO is set to True.
        if CRYPTO:

            self.client = CryptoData( credentials[0],
                                      credentials[1] )

            self.parameters = CryptoBars(
                     symbol_or_symbols = symbols,
                     timeframe         = timeframe,
                     start             = start,
                     end               = end
            )
    
   

        # Otherwise use the stocks client.
        else:

            self.client = StocksData( credentials[0],
                                      credentials[1] )
        
            self.parameters = StocksBars(
                     symbol_or_symbols = symbols,
                     timeframe         = timeframe,
                     start             = yesterday,
                     end               = today
            )
   

    def HLOC( self ):

        if self.CRYPTO: 
            return self.client.get_crypto_bars( self.parameters )
        else:
            return self.client.get_stock_bars( self.parameters )


class InvalidTimeframe(Exception):
    def __init__(self, timeframe):
        print(
        f"The given timeframe: {timeframe}; "
        f"--is invalid."
    )
