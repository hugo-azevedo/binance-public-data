import csv
import json
import os
from pathlib import Path
import zipfile
import shutil
import gzip
import pandas as pd
import io

json_folder = os.path.join(os.getcwd(), 'data', 'json')
json_path = os.path.join(json_folder, 'all.json')
Path(json_folder).mkdir(parents=True, exist_ok=True)
Path(json_path).touch()
json_file = open(json_path, 'w').close() #empty file
json_file = open(json_path, 'w')
csv_field_names = ("start", "open", "high", "low", "close", "volume", "end", "quote_asset_volume", "no_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore")

zip_pathlist = Path(os.path.join(os.getcwd(), 'data')).rglob('*.zip')

with open(os.path.join(json_folder, 'tempfile.csv'), 'wb') as tmp_csv:
  print('Merging csv files into 1 json...')
  prev_ticker = ''
  for zip_path in zip_pathlist:
    tmp_zip = zipfile.ZipFile(zip_path, 'r')
    csv_filename = tmp_zip.namelist()[0]

    params = csv_filename.strip('.csv').split('-')
    if prev_ticker != params[0]:
      print(f'Merging {params[0]} csv files...')
      prev_ticker = params[0]

    with io.TextIOWrapper(tmp_zip.open(csv_filename, 'r')) as tmp_csv:
      reader = csv.DictReader( tmp_csv, csv_field_names)
      for row in reader:
        row['ticker'] = params[0]
        row['interval'] = params[1]
        row['year'] = params[2]
        row['month'] = params[3]

        del row['quote_asset_volume']
        del row['taker_buy_base_asset_volume']
        del row['taker_buy_quote_asset_volume']
        del row['ignore']

        json.dump(row, json_file)
        json_file.write('\n')
  
  print('Done.')