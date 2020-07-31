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


def process_data(df):
  clean = pd.DataFrame()
  clean["date"] = df["date"].apply(lambda d: dt.datetime.strptime(str(d), "%Y%m%d").strftime("%Y-%m-%d"))
  clean["Overall positivity rate"] = (df["positive"].fillna(0) / df["total"]).fillna(0)
  clean["Positivity rate by day"] = (df["positiveIncrease"].fillna(0) / df["totalTestResultsIncrease"]).fillna(0)
  clean["fatality rate"] = (df["death"].fillna(0) / df["positive"]).fillna(0)
  clean["fatality rate by day"] = (df["deathIncrease"].fillna(0) / df["positiveIncrease"]).fillna(0)
  return clean.sort_values(by='date').set_index('date')


def get_updated_data(df, di):
  last_row = df.tail(1).iloc[0]
  prev_row = df.tail(2).iloc[0]
  d_str = dt.datetime.strptime(last_row.name, "%Y-%m-%d").strftime('%-m/%-d')
  d_today_str = dt.datetime.now(pytz.timezone('US/Central')).strftime('%-m/%-d')
  return {
    "smart_tiles": [
        {
            "figure": "{:.2%}".format(last_row["Positivity rate by day"]),
            "subheader": "On {}".format(d_str)
        },
        {
            "figure": "{:.2%}".format(last_row["Overall positivity rate"]),
        },
        {
            "figure": "{:.2%}".format(last_row["fatality rate by day"]),
            "subheader": "On {}".format(d_str),
        },
        {
            "figure": "{:.2%}".format(last_row["fatality rate"]),
        }
    ]
  }


CSV_URL = "https://covidtracking.com/api/v1/states/il/daily.csv"