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


def get_hash(df):
    return None


def process_data(df):
  clean = pd.DataFrame()
  clean["date"] = df["date"].apply(lambda d: dt.datetime.strptime(str(d), "%Y%m%d").strftime("%Y-%m-%d"))
  clean["Total COVID Cases"] = df["positive"]
  clean["New COVID cases in one day"] = df["positiveIncrease"]
  clean["deaths"] = df["death"].fillna(0).astype(int)
  clean["new deaths"] = df["deathIncrease"].fillna(0).astype(int)
  return clean.sort_values(by='date').set_index('date')


def get_updated_data(df, di):
  last_row = df.tail(1).iloc[0]
  prev_row = df.tail(2).iloc[0]
  d_str = dt.datetime.strptime(last_row.name, "%Y-%m-%d").strftime('%-m/%-d')
  d_today_str = dt.datetime.now(pytz.timezone('US/Central')).strftime('%-m/%-d')
  return {
    "smart_tiles": [
        {
            "figure": short_format(last_row["new deaths"]),
            "subheader": "On {}".format(d_str),
            "value_change": round(percent_change(prev_row["new deaths"], last_row["new deaths"]), 1)
        },
        {
            "figure": short_format(last_row["New COVID cases in one day"]),
            "subheader": "On {}".format(d_str),
            "value_change": round(percent_change(prev_row["New COVID cases in one day"], last_row["New COVID cases in one day"]), 1)
        },
        {
            "figure": short_format(last_row["deaths"]),
            "subheader": "As of {}".format(d_str),
            "unit": '+' + short_format(last_row["new deaths"]),
            "value_change": round(percent_change(prev_row["deaths"], last_row["deaths"]), 1)
        },
        {
            "figure": short_format(last_row["Total COVID Cases"]),
            "subheader": "As of {}".format(d_str),
            "unit": '+' + short_format(last_row["New COVID cases in one day"]),
            "value_change": round(percent_change(prev_row["Total COVID Cases"], last_row["Total COVID Cases"]), 1)
        }
    ]
  }