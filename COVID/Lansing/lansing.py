import pandas as pd
import numpy as np
import datetime as dt
import requests as rq
import io
import pytz
import sys
import importlib
import hashlib

sys.path.insert(0,'..')
import jhu_utils
from script_utils import *


def get_hash(df, **kwargs):
    r = kwargs.get("response")
    if not r:
        return None
    return hashlib.md5(r.headers["Last-Modified"].encode()).hexdigest()


def process_data(df, **kwargs):
  clean = df[["Race", "Latino", "Date of Death"]]
  clean.rename(columns={"Date of Death": "Date"}, inplace=True)
  clean["Date"] = pd.to_datetime(clean["Date"]).apply(lambda v: v.strftime("%Y-%m-%d"))
  return clean.set_index("Date")


def get_updated_data(df, di, **kwargs):
  last_row = df.tail(1).iloc[0]
  prev_row = df.tail(2).iloc[0]
  # d_str = dt.datetime.strptime(last_row.name, "%Y-%m-%d").strftime('%-m/%-d')
  d_today_str = dt.datetime.now(pytz.timezone('US/Central')).strftime('%-m/%-d')
  d_prev = dt.datetime.now(pytz.timezone('US/Central')) - dt.timedelta(days=1)
  d_prev_prev = d_prev - dt.timedelta(days=1)
  try:
    new_prev = len(df.loc[d_prev.strftime("%Y-%m-%d")])
  except KeyError:
    new_prev = 0
  try:
    new_prev_prev = len(df.loc[d_prev_prev.strftime("%Y-%m-%d")])
  except:
    new_prev_prev = 0
  d_prev_str = d_prev.strftime('%-m/%-d')
  return {
    "smart_tiles": [
        {
          "figure": short_format(new_prev),
          "subheader": "On {}".format(d_prev_str),
          "value_change": round(percent_change(new_prev_prev, new_prev), 1)
        },
        {},
        {
          "figure": short_format(len(df)),
          "subheader": "As of {}".format(d_today_str),
          "unit": '+' + short_format(new_prev),
          "value_change": round(percent_change(len(df) - new_prev, len(df)), 1)
        },
        {}
    ]
  }