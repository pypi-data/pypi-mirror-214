#!/bin/python3
from glob import glob
from os import system as command


class FSLinker:

    def __init__( self, data, date,
                  asset_basepath: str = "/server/front-end/assets/data-science/reports",
                  target_directory: str = "/server/front-end/_posts/reports"
    ):

        self.date = date; self.data = data
        self.date_directory = self.date.replace("-", "/")

        self.report = f"{target_directory}/{self.date}-Daily-Finance-Report.md"

        self.assets = glob(f"{asset_basepath}/{ self.date_directory}/*")

        self.url = f"https://guyyatsu.me/assets/data-science/reports/{self.date_directory}"


    def DailyReport( self ):
        """
        """

        report = open(self.report, "w")

        # Write the front matter.
        report.write( "---\n" )
        report.write( f"title: Daily Finance Report for {self.date}.\n" )
        report.write( "layout: post\n" )
        report.write( "category: finance-reports\n" )
        report.write( "\n" )
        report.write( "---\n" )
        report.write( "\n" )


        symbols = []
 
        for asset in self.assets:
            symbols.append( asset.split( "/" )[ -1 ][ 0 ] )

        for symbol in symbols:
            report.write( f"# {symbol}\n" )
            if self.data[symbol]["start"] > self.data[symbol]["end"]:
                difference = self.data[symbol]["start"] - self.data[symbol]["end"]
                report.write(f"{symbol} rose by {difference} points.")
            else:
                difference = self.data[symbol]["end"] - self.data[symbol]["start"]
                report.write(f"{symbol} fell by {difference} points.")
         

            if glob(f"{self.asset_basepath}/{self.asset_date}/{symbol}.candlestick.html"):
                report.write(
                    f"<embed type='text/html' "
                    f"src='{self.url}/{symbol}.candlestick.html' "
                    f"height='350' width='750'>\n"
                )

        report.close()

FSLinker().DailyReport()
