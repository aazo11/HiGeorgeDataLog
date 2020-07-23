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


def process_data(states):
  date = states[states['county'] == 'San Francisco']['date']
  santaclara = states[states['county'] == 'Santa Clara']['totalcountdeaths']
  alam = states[states['county'] == 'Alameda']['totalcountdeaths']
  cc = states[states['county'] == 'Contra Costa']['totalcountdeaths']
  marin = states[states['county'] == 'Marin']['totalcountdeaths']
  smateo = states[states['county'] == 'San Mateo']['totalcountdeaths']
  sf = states[states['county'] == 'San Francisco']['totalcountdeaths']
  deaths = pd.DataFrame()

  deaths['Date'] = date.iloc[:].values
  deaths['Santa Clara'] = santaclara.iloc[:].values
  deaths['SF'] = sf.iloc[:].values
  deaths['Alameda'] = alam.iloc[:].values
  deaths['Contra Costa'] = cc.iloc[:].values
  deaths['Marin'] = marin.iloc[:].values
  deaths['San Mateo'] = smateo.iloc[:].values
  return deaths


def get_updated_data(df, di):
  last_row = df.set_index('Date').tail(1).iloc[0]
  d_today_str = dt.datetime.now(pytz.timezone('US/Pacific')).strftime('%-m/%-d')
  us = get_us_data()
  ca = get_state_data('ca')
  sf_now = jhu.loc["San Francisco"]["Deaths"]
  bay_now = jhu.sum()["Deaths"]
  return {
    "smart_tiles": [
        {
          "figure": short_format(bay_now - last_row.sum()),
          "subheader": "On {}".format(d_today_str)
        },
        {
          "figure": short_format(sf_now - last_row['SF']),
          "subheader": "On {}".format(d_today_str)
        },
        {
          "figure": short_format(ca['deathIncrease']),
          "subheader": "On {}".format(d_today_str),
          # "value_change": round(percent_change(ca['death'] - ca['deathIncrease'], ca['death']), 1)
        },
        {
          "figure": short_format(us['deathIncrease']),
          "subheader": "On {}".format(d_today_str),
          # "value_change": round(percent_change(us['death'] - us['deathIncrease'], us['death']), 1)
        }
    ]
  }