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


def process_data(sfcases):
  sfcases['specimen_collection_date'] = sfcases['specimen_collection_date'].apply(lambda v: v.split('T')[0])
  cases = sfcases[['specimen_collection_date', 'case_count']].groupby('specimen_collection_date').sum()
  average = list(np.zeros(6))
  for i in range(7,len(cases)+1):
      average += [np.mean(cases['case_count'][i-7:i])]
  cases['7 day average'] = average

  data = ['More reliable'] * len(cases)-4
  data += ['Less reliable, likely to be updated'] * 4
  cases['Data Reliability'] = data

  return cases.rename(columns={"case_count": "Case Count"})


def get_updated_data(df, di):
  last_row = df.tail(1).iloc[0]
  d_today_str = dt.datetime.now(pytz.timezone('US/Pacific')).strftime('%-m/%-d')
  jhu_prev = jhu_utils.get_nearest_csv(dt.datetime.now() - dt.timedelta(hours=18))
  jhu_prev = jhu_utils.clean_jhu(jhu_prev, bay_area)
  us = get_us_data()
  ca = get_state_data('ca')
  sf_now = jhu.loc["San Francisco"]["Confirmed"]
  sf_prev = jhu_prev.loc["San Francisco"]["Confirmed"]
  bay_now = jhu.sum()["Confirmed"]
  bay_prev = jhu_prev.sum()["Confirmed"]
  return {
    "smart_tiles": [
        {
          "figure": short_format(sf_now),
          "subheader": "As of {}".format(d_today_str),
          "unit": "+{}".format(short_format(sf_now - sf_prev)),
          "value_change": round(percent_change(sf_prev, sf_now), 1)
        },
        {
          "figure": short_format(bay_now),
          "subheader": "As of {}".format(d_today_str),
          "unit": "+{}".format(short_format(bay_now - bay_prev)),
          "value_change": round(percent_change(bay_prev, bay_now), 1)
        },
        {
          "figure": short_format(ca['positive']),
          "subheader": "As of {}".format(d_today_str),
          "unit": "+{}".format(short_format(ca['positiveIncrease'])),
          "value_change": round(percent_change(ca['positive'] - ca['positiveIncrease'], ca['positive']), 1)
        },
        {
          "figure": short_format(us['positive']),
          "subheader": "As of {}".format(d_today_str),
          "unit": "+{}".format(short_format(us['positiveIncrease'])),
          "value_change": round(percent_change(us['positive'] - us['positiveIncrease'], us['positive']), 1)
        }
    ]
  }