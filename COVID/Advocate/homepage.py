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
    return hash_dataframes(jhu_utils.clean_jhu(df, [("Texas", "Dallas")]))


def process_data(df, **kwargs):
  newest = jhu_utils.clean_jhu(df, [("Texas", "Dallas")])

  ts = jhu_utils.get_cases_time_series()
  ts = ts[(ts['Admin2'] == 'Dallas') & (ts['Province_State'] == 'Texas')]
  ts = ts.set_index('Combined_Key').transpose().iloc[10:].rename(columns=lambda v: "Total Cases")

  ds = jhu_utils.get_deaths_time_series()
  ds = ds[(ds['Admin2'] == 'Dallas') & (ds['Province_State'] == 'Texas')]
  ds = ds.set_index('Combined_Key').transpose().iloc[10:].rename(columns=lambda v: "Total Deaths")

  data = pd.concat((ts, ds), axis=1)
  data = data.drop('Population', errors='ignore')
  data = data.rename_axis("Date", axis=0).rename_axis(None, axis=1).fillna(0)
  data = data.reset_index()
  data["dt"] = pd.to_datetime(data["Date"])
  data = data.set_index("Date")
  data = data.sort_values(by='dt').drop('dt', axis=1)

  data.loc[dt.datetime.now(pytz.timezone('US/Eastern')).strftime("%-m/%-d/%y")] = (newest.iloc[0]["Confirmed"], newest.iloc[0]["Deaths"])
  data["New Cases"] = (data["Total Cases"].shift(-1) - data["Total Cases"]).shift(1).fillna(0).astype(int)
  data["New Deaths"] = (data["Total Deaths"].shift(-1) - data["Total Deaths"]).shift(1).fillna(0).astype(int)
  data["New Cases 7 Day Average"] = data["New Cases"].rolling(7).mean().fillna(0)
  return data


def get_updated_data(df, di, **kwargs):
  last_row = df.tail(1).iloc[0]
  prev_row = df.tail(2).iloc[0]
  d_str = (dt.datetime.strptime(last_row.name, '%m/%d/%y')).strftime('%-m/%-d')
  d_today_str = dt.datetime.now(pytz.timezone('US/Central')).strftime('%-m/%-d')
  return {
    "smart_tiles": [
        {
          "figure": short_format(last_row["New Cases"]),
          "unit": "On {}".format(d_str)
        },
        {
          "figure": short_format(last_row["New Deaths"]),
          "unit": "On {}".format(d_str)
        },
        {
          "figure": short_format(last_row["Total Cases"]),
          "unit": "As of {}".format(d_today_str)
        },
        {
          "figure": short_format(last_row["Total Deaths"]),
          "unit": "As of {}".format(d_today_str)
        }
    ]
  }