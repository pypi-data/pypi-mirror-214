#!/bin/python3 


"""
This module provides methods for retrieving auction data from Alpaca.Markets and posting it
to a socket server as a serialized JSON object.

Run the daemon by typing:

```
python3 -m Lab93BackendAPI --live-data \
                           --trade-pairs BTC/USD \
                           --host 127.0.0.1 \
                           --port 65535
```

"""




from threading import Thread
from .stream import StreamHandler

from alpaca.data.live import CryptoDataStream as stream

class liveDataServer:
    """
    The live data server uses a socket connection to retrieve live auction
    data from the Alpaca.Markets API and redirect the results to another
    socket server for interpretation by any other systems within the host.
    """


    def __init__( self, credentials,
                  symbols: list=["BTC/USD"],
                  host:    str="127.0.0.1",
                  port:    int=65535         ):


        # Set runtime constants.
        host = host # The IP of the socket server.
        port = port # Port for the socket server.
        data = {}   # Dictionary containing our results.


        # Initialize the Alpaca.Markets live data client.
        client = stream( credentials[0], credentials[1]  )

        # Subscribe to each of the asset pairs provided by the symbols list.
        for asset in symbols: client.subscribe_quotes( StreamHandler,
                                                       str(  asset.upper() )   )

        # Begin running the data client in the background.
        Thread( daemon=True,
                name="liveDataDaemon",
                target=client.run()  ).start()
