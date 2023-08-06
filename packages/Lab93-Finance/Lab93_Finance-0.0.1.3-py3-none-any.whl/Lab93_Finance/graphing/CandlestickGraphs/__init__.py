#!/bin/python3


"""
CandlestickChart produces a .png graphical chart at the
specified location `output_directory`; it requires a
packet of timeseries `THLOC` values in sequence.

To produce our charts, we use plotly.graph_objects
                                    .Candlestick and save
the results to  a portable network graphic.
"""

# Retrieve plotly tools for drawing candlestick graphs.
from plotly.graph_objects import Figure, Candlestick

# Datetime objects for coming up with a filepath.
from datetime import datetime, timedelta

# Operating-System level filesystem control.
from os.path import exists as directory
from os import system as command


class drawCandlestick:
    """
    """

    def __init__( self,

        # A dictionary of lists containing HLOC points.
        ranges: dict = {
            'time':   [ 1, 2, 3, 4, 5 ],
            'high':   [ 4, 5, 6, 7, 8 ],
            'low':    [ 3, 4, 5, 6, 7 ],
            'open':   [ 4, 5, 6, 7, 8 ],
            'close':  [ 3, 4, 5, 6, 7 ],
            'symbol': "BTC-USD"
        },

        # Filepath for placing generated output.
        output_directory: str = "./reports" ):

        # Create the directory containing the output.
        if not directory( output_directory ):
            command( f"mkdir -p {output_directory}" )

        # Define the output file; as a .png file.
        self.output = (
            f"{output_directory}/"
            f"{ranges['symbol'].replace('/', '-')}"
            f".candlestick.html"
        )


        # Draw the graph and save it to the output file.
        Figure(
            data=[
                Candlestick( x     = ranges[ 'time'  ],
                             open  = ranges[ 'open'  ],
                             high  = ranges[ 'high'  ],
                             low   = ranges[ 'low'   ],
                             close = ranges[ 'close' ] )
            ]
        ).write_html( self.output,
                      include_plotlyjs = 'cdn' )
