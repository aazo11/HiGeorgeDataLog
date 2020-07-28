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
    return hash_dataframes(df.set_index('Province_State').loc["Pennsylvania"])


def process_data(df, **kwargs):
  newest = df.set_index('Province_State').loc["Pennsylvania"]
  pa = get_state_data("pa", "daily")

  ts = jhu_utils.get_cases_time_series()
  ts = ts[(ts['Province_State'] == 'Pennsylvania')]
  ts = ts.set_index('Combined_Key').transpose().iloc[10:].transpose().sum().astype(int)
  ds = jhu_utils.get_deaths_time_series()
  ds = ds[(ds['Province_State'] == 'Pennsylvania')]
  ds = ds.set_index('Combined_Key').transpose().iloc[10:].transpose().sum().astype(int)

  data = pd.concat((ts, ds), axis=1)
  data = data.drop('Population', errors='ignore')
  data = data.rename(columns={0: "Total Cases", 1: "Total Deaths"})

  data.loc[dt.datetime.now(pytz.timezone('US/Eastern')).strftime("%-m/%-d/%y")] = (newest["Confirmed"], newest["Deaths"])

  data = data.reset_index().rename(columns={"index": "Date"})
  data["dt"] = pd.to_datetime(data["Date"])
  data = data.set_index("Date")
  data = data.sort_values(by='dt').drop('dt', axis=1)

  data["New Cases"] = (data["Total Cases"].shift(-1) - data["Total Cases"]).shift(1).fillna(0).astype(int)
  data["New Deaths"] = (data["Total Deaths"].shift(-1) - data["Total Deaths"]).shift(1).fillna(0).astype(int)
  data["New Cases 7 Day Average"] = data["New Cases"].rolling(7).mean().fillna(0)

  pa = pd.DataFrame(data=pa)[["date", "positive", "total"]]
  pa["Date"] = pa["date"].apply(lambda d: dt.datetime.strptime(str(d), "%Y%m%d").strftime("%-m/%-d/%y"))
  pa = pa.drop('date', axis=1).set_index('Date').rename(columns={"total": "Total Tests"})

  data = pd.concat((data, pa), axis=1)

  data = data.reset_index().rename(columns={"index": "Date"})
  data["dt"] = pd.to_datetime(data["Date"])
  data = data.set_index("Date")
  data = data.sort_values(by='dt').drop('dt', axis=1)

  data["Positive Test Rate"] = data["positive"] / data["Total Tests"] * 100
  data["Tests Per Day"] = (data["Total Tests"].shift(-1) - data["Total Tests"]).shift(1).fillna(0).astype(int)
  data = data.drop('positive', axis=1)

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
          "figure": short_format(prev_row["Tests Per Day"]),
          "subheader": "Reported on {}".format(d_prev)
        },
        {
          "figure": str(round(prev_row["Positive Test Rate"], 2)) + '%',
          "subheader": "Reported on {}".format(d_prev)
        },
    ]
  }