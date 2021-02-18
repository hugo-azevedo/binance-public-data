import csv
import io
import json
import math
import os
import pandas as pd
from pathlib import Path
import zipfile

zip_pathlist = Path(os.path.join(os.getcwd(), 'data')).rglob('*.zip')
zipfile_list = list(zip_pathlist)
total = len(zipfile_list)
print(f'Extracting {total} zip files...')

counter = 1
for zip_path in zipfile_list:
  tmp_zip = zipfile.ZipFile(zip_path, 'r')
  tmp_zip.extractall(path='data/csv/')
  percent = math.floor(counter/total * 100)
  prev = math.floor((counter -1)/total * 100)
  if percent > prev:
    print(f'{percent}%')
  counter += 1
  
print('Done.')