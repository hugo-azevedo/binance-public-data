#!/usr/bin/env python

"""
  script to download klines.
  set the absoluate path destination folder for STORE_DIRECTORY, and run

  e.g. STORE_DIRECTORY=/data/ ./download-kline.py
"""

from colorama import init
import json
import os
from pathlib import Path
import sys, getopt
from termcolor import colored
import urllib.request

# use Colorama to make Termcolor work on Windows too
init()

YEARS = ['2017', '2018', '2019', '2020', '2021']
INTERVALS = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1mo"]

BASE_URL = 'https://data.binance.vision/'

REVERSE_TICKER_ORDER = False

def get_destination_dir(file_url):
  store_directory = os.environ.get('STORE_DIRECTORY')
  if not store_directory:
    store_directory = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(store_directory, file_url)

def get_download_url(file_url):
    return "{}{}".format(BASE_URL, file_url)

def get_all_symbols():
  response = urllib.request.urlopen("https://api.binance.com/api/v3/exchangeInfo").read()
  return list(map(lambda symbol: symbol['symbol'], json.loads(response)['symbols']))

def download_file(path, file_name):
  file_path = "{}{}".format(path, file_name)
  save_path = get_destination_dir(file_path)

  if os.path.exists(save_path):
    print(colored("file already existed! {}".format(save_path), 'red'))
    return
  
  # make the directory
  Path(get_destination_dir(path)).mkdir(parents=True, exist_ok=True)

  try:
    download_url = get_download_url(file_path)
    with urllib.request.urlopen(download_url) as dl_file:
        with open(save_path, 'wb') as out_file:
            out_file.write(dl_file.read())
            print(colored("File Download: {}".format(save_path), 'blue'))
  except urllib.error.HTTPError:
    print(colored("File not found: {}".format(download_url), 'red'))
    pass

def select_symbols_subset(symbols):
  selected_symbols = []
  choosing = True
  while choosing :
    new_symbol = input(colored("Input symbol to add to list or press <ENTER> to continue: ", 'blue'))
    if new_symbol == "" or new_symbol is None:
      choosing = False
    else:
      if new_symbol.upper() in symbols:
        selected_symbols.append( new_symbol.upper() )
        print(colored("Currently selected symbols:", 'yellow'))
        print(", ".join(selected_symbols))
      else:
        print(colored(">> Error: Symbol {} does not exist. Try again. ".format(new_symbol.upper()), 'red'))
  return selected_symbols

def select_years_subset():
  selected_years = []
  choosing = True
  print(colored("Available years are:", 'green'))
  print(", ".join(YEARS))
  while choosing :
    year = input(colored("Input year to add to list or press <ENTER> to continue: ", 'blue'))
    if year == "" or year is None:
      choosing = False
    else:
      if year in YEARS:
        selected_years.append( year )
        print(colored("Currently selected years:", 'yellow'))
        print(", ".join(selected_years))
      else:
        print(colored(">> Error: Data for {} does not exist. Try again. ".format(year), 'red'))
  return selected_years

def select_intervals_subset():
  selected_intervals = []
  choosing = True
  print(colored("Available intervals are:", 'green'))
  print(", ".join(INTERVALS))
  while choosing :
    interval = input(colored("Input interval to add to list or press <ENTER> to continue: ", 'blue'))
    if interval == "" or interval is None:
      choosing = False
    else:
      if interval in INTERVALS:
        selected_intervals.append( interval )
        print(colored("Currently intervals years:", 'yellow'))
        print(", ".join(selected_intervals))
      else:
        print(colored(">> Error: {} is not a valid interval. Try again. ".format(interval), 'red'))
  return selected_intervals

def main(argv):
  opts, args = getopt.getopt(argv,"r")
  for opt, arg in opts:
    if opt in ("-r"):
      print('Using reversed order')
      global REVERSE_TICKER_ORDER
      REVERSE_TICKER_ORDER = True

if __name__ == "__main__":
    main(sys.argv[1:])
    print(REVERSE_TICKER_ORDER)
    
    print(colored("Fetching all symbols from exchange...", 'blue'))
    symbols = get_all_symbols()
    all = len(symbols)

    current = 0
    print(colored("Found {} symbols".format(all), 'red'))

    select_symbols = input(colored("Download klines for all symbols? (Y/N) ", 'blue')).upper()
    if select_symbols != "Y" and select_symbols != '':
      symbols = select_symbols_subset(symbols)
    else:
      if select_symbols == '':
        print('Y')
    
    select_years = input(colored("Download klines for all years? (Y/N) ", 'blue')).upper()
    if select_years != "Y" and select_years != '': 
      YEARS = select_years_subset()
    else:
      if select_years == '':
        print('Y')
    
    select_intervals = input(colored("Download klines for all intervals? (Y/N) ", 'blue')).upper()
    if select_intervals != "Y" and select_intervals != '': 
      INTERVALS = select_intervals_subset()
    else:
      if select_intervals == '':
        print('Y')

    for symbol in (reversed(symbols) if REVERSE_TICKER_ORDER else symbols):
      print(colored("[{}/{}] - start download {} klines ".format(current+1, len(symbols), symbol), 'blue'))
      for interval in INTERVALS:
        for year in YEARS:
          for month in list(range(1, 13)):
            path = "data/spot/klines/{}/{}/".format(symbol.upper(), interval)
            file_name = "{}-{}-{}-{}.zip".format(symbol.upper(), interval, year, '{:02d}'.format(month))
            download_file(path, file_name)
      
      current += 1