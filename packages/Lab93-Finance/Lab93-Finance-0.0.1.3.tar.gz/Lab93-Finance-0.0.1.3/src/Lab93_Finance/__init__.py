from Lab93_DatabaseSystem import AdministratorDatabase
from datetime import datetime, timedelta
from graphing.CandlestickGraphs import drawCandlestick
from data.historic import Queries
from account import AccountDetails


AdminDB = AdministratorDatabase()


today = datetime.today()
yesterday = today - timedelta(days=1)


class AlpacaMarket:
    def __init__(self):
        self.account = AccountDetails(
           ( AdminDB.Retrieve( user = "admin",
                               platform = "alpaca_key" ),
             AdminDB.Retrieve( user = "admin",
                               platform = "alpaca_secret" ) ),
        )

class GraphingReports:
    def __init__(self, start=yesterday, end=today,
        output = "/server/front-end/assets/data-science/reports" ):

        # Collect High, Low, Open, Close, and Times for the given symbol.
        # TODO: Allow for custom symbol entries.
        # TODO: Allow for custom timeframes.
        # TODO: Retrieve credentials from environment.
        data = Queries( start = start, end = end, symbols = [ "BTC/USD" ],
                        timeframe = "hour",
                        credentials = ( AdminDB.Retrieve( user     = "admin",
                                                          platform = "alpaca_key" ),
                                        AdminDB.Retrieve( user     = "admin",
                                                          platform = "alpaca_secret" ) ) )\
               .HLOC()\
               .data

        # Convert start date into string separated by forward slashes.
        datestring = datetime.strftime(start, "%Y/%m/%d")

        # Organize data array into packet hashmap for passing to Candlestick class.
        self.packet = {

            "time":   [ line.timestamp for symbol in data for line in data[symbol] ],
            "high":   [ line.high for symbol in data for line in data[symbol]      ],
            "low":    [ line.low for symbol in data for line in data[symbol]       ],
            "open":   [ line.open for symbol in data for line in data[symbol]      ],
            "close":  [ line.close for symbol in data for line in data[symbol]     ],
            "symbol": [ line.symbol for symbol in data for line in data[symbol] ][0]

        }

        # Draw the candlestick graph at the specially formulated filepath.
        drawCandlestick( self.packet, f"{output}/{datestring}")
