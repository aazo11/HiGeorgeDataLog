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


def process_data(df, **kwargs):
  data = pd.DataFrame()
  data["Date"] = df["date"].apply(lambda d: dt.datetime.strptime(str(d), "%Y%m%d").strftime("%-m/%-d/%y"))
  data["Total Cases"] = df["positive"]
  data["New Cases"] = df["positiveIncrease"]
  data["Total Deaths"] = df["death"].fillna(0).astype(int)
  data["New Deaths"] = df["deathIncrease"]
  data["Total Tests"] = df["total"]
  data["Positive Test Rate"] = df["positive"] / df["total"] * 100
  data["Positive Test Rate"] = data["Positive Test Rate"].apply(lambda v: None if v == 100 else v)
  data["Tests Per Day"] = df["totalTestResultsIncrease"]
  data["dt"] = pd.to_datetime(data["Date"])
  data = data.sort_values(by="dt")
  data = data.drop("dt", axis=1)
  data = data.set_index("Date")
  data["New Cases 7 Day Average"] = data["New Cases"].rolling(7).mean().fillna(0)
  return data


def get_updated_data(df, di, **kwargs):
  last_row = df.tail(1).iloc[0]
  prev_row = df.tail(2).iloc[0]
  d_prev = (dt.datetime.strptime(prev_row.name, '%m/%d/%y')).strftime('%-m/%-d')
  d_str = (dt.datetime.strptime(last_row.name, '%m/%d/%y')).strftime('%-m/%-d')
  d_today_str = dt.datetime.now(pytz.timezone('US/Eastern')).strftime('%-m/%-d')
  return {
    "smart_tiles": [
        {
          "figure": short_format(last_row["New Deaths"]),
          "subheader": "Reported on {}".format(d_str)
        },
        {
          "figure": short_format(last_row["Total Deaths"]),
          "subheader": "Reported on {}".format(d_str)
        },
    ]
  }