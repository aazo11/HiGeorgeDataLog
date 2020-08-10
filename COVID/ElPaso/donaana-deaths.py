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


# %%
COUNTY = "Dona Ana"
STATE = "New Mexico"
TZ = "US/Mountain"


# %%
def preprocess(**kwargs):
    return None


# %%
def get_hash(df, **kwargs):
    return hash_dataframes(jhu_utils.clean_jhu(df, [(STATE, COUNTY)]))


# %%
def process_data(df, **kwargs):
  if COUNTY:
    newest = jhu_utils.clean_jhu(df, [(STATE, COUNTY)])
  else:
    newest = jhu_utils.clean_state(jhu_utils.get_current_state_level(), STATE)

  ts = jhu_utils.get_cases_time_series()
  if COUNTY:
    ts = ts[(ts['Admin2'] == COUNTY) & (ts['Province_State'] == STATE)]
    ts = ts.set_index('Combined_Key').transpose().iloc[10:].rename(columns=lambda v: "Total Cases")
  else:
    ts = ts[ts['Province_State'] == STATE]
    ts = ts.set_index('Combined_Key').sum().to_frame().iloc[10:].rename(columns=lambda v: "Total Cases")

  ds = jhu_utils.get_deaths_time_series()
  if COUNTY:
    ds = ds[(ds['Admin2'] == COUNTY) & (ds['Province_State'] == STATE)]
    ds = ds.set_index('Combined_Key').transpose().iloc[10:].rename(columns=lambda v: "Total Deaths")
  else:
    ds = ds[ds['Province_State'] == STATE]
    ds = ds.set_index('Combined_Key').sum().to_frame().iloc[10:].rename(columns=lambda v: "Total Deaths")

  data = pd.concat((ts, ds), axis=1)
  data = data.drop('Population', errors='ignore')
  data = data.rename_axis("Date", axis=0).rename_axis(None, axis=1).fillna(0)
  data = data.reset_index()
  data["dt"] = pd.to_datetime(data["Date"])
  data = data.set_index("Date")
  data = data.sort_values(by='dt').drop('dt', axis=1)

  data.loc[dt.datetime.now(pytz.timezone(TZ)).strftime("%-m/%-d/%y")] = (newest.iloc[0]["Confirmed"], newest.iloc[0]["Deaths"])
  data["New Cases"] = (data["Total Cases"].shift(-1) - data["Total Cases"]).shift(1).fillna(0).astype(int)
  data["New Deaths"] = (data["Total Deaths"].shift(-1) - data["Total Deaths"]).shift(1).fillna(0).astype(int)

  # If current day's data matches previous day's, it's most likely that we should ignore today as it's probably not current
  if data.iloc[-1]["Total Cases"] == data.iloc[-2]["Total Cases"] and data.iloc[-1]["Total Deaths"] == data.iloc[-2]["Total Deaths"]:
    data = data.iloc[:-1]

  # Replace negative deaths with 0
  data["New Deaths"] = data["New Deaths"].apply(lambda v: v if v >= 0 else 0)

  data["New Cases 7 Day Average"] = data["New Cases"].rolling(7).mean().fillna(0)
  data["New Deaths 7 Day Average"] = data["New Deaths"].rolling(7).mean().fillna(0)
  return data


# %%
def get_updated_data(df, di, **kwargs):
  last_row = df.tail(1).iloc[0]
  prev_row = df.tail(2).iloc[0]
  d_str = (dt.datetime.strptime(last_row.name, '%m/%d/%y')).strftime('%-m/%-d')
  d_today_str = dt.datetime.now(TZ).strftime('%-m/%-d')
  return {
    "smart_tiles": [
        {
          "figure": short_format(last_row["New Deaths"]),
          "subheader": "Reported on {}".format(d_str)
        },
        {
          "figure": short_format(last_row["Total Deaths"]),
          "subheader": "Reported on {}".format(d_str)
        }
    ]
  }


# %%
CSV_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases.csv"