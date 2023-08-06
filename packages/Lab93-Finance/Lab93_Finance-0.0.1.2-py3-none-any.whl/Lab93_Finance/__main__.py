from .__init__ import *
from argparse import ArgumentParser

from datetime import datetime, timedelta


today = datetime.today(); yesterday = today - timedelta(days=1)
arguments = ArgumentParser()
paradigm = arguments.add_mutually_exclusive_group()


''' Three different possible software suites here; '''

# Performance Reporting:
''' Draws up graphs on query data based on a given start and end date. '''
paradigm.add_argument( "--reports", action = 'store_true' )

# Account Details:
''' Allows for interaction and enumeration of an alpaca account. '''
paradigm.add_argument( "--account", action = 'store_true' )

# Trade Broker:
''' Provides functions for handling and automating an alpaca account. '''
paradigm.add_argument( "--trade",   action = 'store_true' )



''' Performance Reporting Argument Suite

If we're doing reports, then we need to recieve a start and and end date.
Otherwise, we default to yesterday for the start and today for the end. '''

# Collect a start date; default to yesterday.
arguments.add_argument( "-sD", "--start-day",   default = yesterday.day   )
arguments.add_argument( "-sM", "--start-month", default = yesterday.month )
arguments.add_argument( "-sY", "--start-year",  default = yesterday.year  )

# Collect an end date; default to today.
arguments.add_argument( "-eD", "--end-day",   default = today.day   )
arguments.add_argument( "-eM", "--end-month", default = today.month )
arguments.add_argument( "-eY", "--end-year",  default = today.year  )

# Allow specification of an output path.
arguments.add_argument( "-O", "--output-directory", default = "/server/front-end/assets")


arguments = arguments.parse_args()

if arguments.reports:
    ''' Format the start date. '''
    start = f"{arguments.start_year}-{arguments.start_month}-{arguments.start_day}"
    start = datetime.strptime(start, "%Y-%m-%d")

    ''' Format the end date. '''
    end = f"{arguments.end_year}-{arguments.end_month}-{arguments.end_day}"
    end = datetime.strptime(end, "%Y-%m-%d")

    output = f"{arguments.output_directory}/data-science/reports"

    GraphingReports(start, end, output)
