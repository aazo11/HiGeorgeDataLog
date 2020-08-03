import pandas as pd
import numpy as np
import datetime as dt
import requests as rq
import io
import pytz
import sys

sys.path.insert(0,'..')
import jhu_utils
from script_utils import *


def preprocess(**kwargs):
    return None


def get_hash(df, **kwargs):
    return None


def process_data(tests, **kwargs):
  tests['specimen_collection_date'] = tests['specimen_collection_date'].apply(lambda v: v.split('T')[0])
  tests.sort_values('specimen_collection_date', ascending = False)
  rate = tests[['specimen_collection_date', 'pct', 'tests']]
  rate['Positive tests rate'] = rate['pct'] * 100
  rate['Total tests'] = rate['tests']
  average = list(np.zeros(6))
  for i in range(7,len(rate)+1):
      average += [np.mean(rate['Positive tests rate'][i-7:i])]
  rate['7 day average rate'] = average
  return rate


def get_updated_data(df, di, **kwargs):
  last_row = df.iloc[-3]
  d_str = dt.datetime.strptime(last_row['specimen_collection_date'], '%Y-%m-%d').strftime('%-m/%-d')
  d_today_str = dt.datetime.now(pytz.timezone('US/Pacific')).strftime('%-m/%-d')
  return {
    "smart_tiles": [
        {
          "figure": short_format(last_row['Total tests']),
          "subheader": "For {}".format(d_str)
        },
        {
          "figure": "{:.1f}%".format(last_row['Positive tests rate']),
          "subheader": "For {}".format(d_str)
        }
    ]
  }


CSV_URL = "https://data.sfgov.org/resource/nfpa-mg4g.csv?$order=specimen_collection_date"