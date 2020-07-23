import pandas as pd
import numpy as np
import datetime as dt
import requests as rq
import io
import pytz
import sys
import importlib

sys.path.insert(0,'..')
import jhu_utils
from script_utils import *


bay_area = [
    ("California", "San Francisco"),
    ("California", "Santa Clara"),
    ("California", "Contra Costa"),
    ("California", "Alameda"),
    ("California", "Marin"),
    ("California", "San Mateo")
]

jhu = None

def get_hash(df):
    global jhu
    jhu = jhu_utils.clean_jhu(jhu_utils.get_current(), bay_area)
    return hash_dataframes(df, jhu.loc['San Francisco'])


def process_data(df):
  return df


def get_updated_data(df, di):
  last_row = df.tail(1).iloc[0]
  d_today_str = dt.datetime.now(pytz.timezone('US/Pacific')).strftime('%-m/%-d')
  jhu_prev = jhu_utils.get_nearest_csv(dt.datetime.now() - dt.timedelta(hours=18))
  jhu_prev = jhu_utils.clean_jhu(jhu_prev, bay_area)
  us = get_us_data()
  # prev = dt.datetime.strptime(str(us['date']), '%Y%m%d') - dt.timedelta(days=1)
  # us_prev = get_us_data(date=prev)
  ca = get_state_data('ca')
  # ca_prev = get_state_data('ca', date=prev)
  sf_now = jhu.loc["San Francisco"]["Confirmed"]
  sf_prev = jhu_prev.loc["San Francisco"]["Confirmed"]
  bay_now = jhu.sum()["Confirmed"]
  bay_prev = jhu_prev.sum()["Confirmed"]
  return {
    "smart_tiles": [
        {
          "figure": short_format(ca['positiveIncrease'])
        },
        {
          "figure": short_format(sf_now - sf_prev)
        },
        {
          "figure": short_format(bay_now - bay_prev)
        },
        {
          "figure": short_format(us['positiveIncrease'])
        }
    ]
  }