#!/bin/python3 


# Access tools for connecting to the api Hub.
from socket import socket, AF_INET, SOCK_STREAM

# JSON serialization for handling data objects.
from json import dumps as serialize
from time import sleep
from datetime import datetime

# Alpaca.Markets SDK
from alpaca.data.live import CryptoDataStream as CryptoStream
from alpaca.data.live import StockDataStream  as StocksStream


async def StreamHandler( self, data ):
    """
    Recieves new data from the market stream and redirects it to
    a local socket server for use by other facilities in the lab.
    """

    # Re-Write the sub-dictionary inside the self.data dictionary.
    self.data["Live Market Data"] =  {
        str(data.symbol): {
            "name": data.symbol, "time": datetime.timestamp( data.timestamp ),
            "ask price": data.ask_price, "ask size": data.ask_size,
            "bid price": data.bid_price, "bid size": data.bid_size
        }
    }

    # Connect to the socket server and send the data packet.
    with socket( AF_INET, SOCK_STREAM ) as server:

        # Establish connection.
        try:
            server.connect( (self.host, self.port) )

        except Exception: return Exception


        # Upload data packet.
        try:
            server.sendall( bytes( serialize( self.data ),
                                   encoding="utf-8"        ) )

        except Exception: return Exception

        # Close the connection
        finally: server.close(); sleep(1)
