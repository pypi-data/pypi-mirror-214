#!/bin/python3
"""
The reporter script offers graphing functionality to the
Lab93-Brokerage system using
plotly.  It pulls periodic HLOC data from a list of
cryptocurrency and stocks and writes a summary of the
days performance.
"""


# Import movement charting;
from .CandlestickGraphs import CandlestickChart

"""
# Import predictive analysis;
from .LinearRegression import Regression

# Import trend analysis;
from .MovingCrossAverage import CrossAverages
"""

class FinanceReports:

    def __init__( self,
                  output_basepath: str = ""
    ):

        if output_basepath == "":
            self.output_basepath = (
                f"/server/front-end"
                f"/assets/data-science"
                f"/reports"
            )

        else: self.output_basepath = output_basepath


    def CandleGraph( self, ranges,
    ):

         return CandlestickChart(
             ranges = ranges,
             output_directory = self.directory
         )



