import pandas as pd
import numpy as np
import datetime as dt
import requests as rq
import pytz

def short_format(num):
    if num >= 0 and num < 10000:
        return '{:,.4g}'.format(num)
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def get_us_data(field=None):
    """
    Returns a JSON object with the following notable fields:
    positive, negative, death, total (number of tests), recovered
    hospitalizedCurrently, inIcuCurrently, onVentilatorCurrently
    deathIncrease, hospitalizedIncrease, positiveIncrease, negativeIncrease, totalTestResultsIncrease
    """
    j = rq.get("https://covidtracking.com/api/v1/us/current.json").json()[0]
    return j[field] if field else j

def get_state_data(state, field=None):
  """
  Returns a JSON object with the following notable fields:
    positive, negative, death, total (number of tests), recovered
    hospitalizedCurrently, inIcuCurrently, onVentilatorCurrently
    deathIncrease, hospitalizedIncrease, positiveIncrease, negativeIncrease, totalTestResultsIncrease
  """
  j = rq.get("https://covidtracking.com/api/v1/states/{}/current.json".format(state)).json()[0]
  return j[field] if field else j

def percent_change(old, new):
  return (new - old) / old * 100

def process_data(tests):
  tests.sort_values('specimen_collection_date', ascending = False)
  rate = tests[['specimen_collection_date', 'pct', 'tests']]
  rate['Positive tests rate'] = rate['pct'] * 100
  rate['Total tests'] = rate['tests']
  return rate

def get_updated_data(df):
  last_row = df.tail(1).iloc[0]
  d_str = dt.datetime.strptime(last_row['specimen_collection_date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%-m/%-d/%Y')
  d_today_str = dt.datetime.now(pytz.timezone('US/Pacific')).strftime('%-m/%-d/%Y')
  return {
    "smart_tiles": [
        {
          "figure": short_format(last_row['Total tests']),
          "subheader": "For {}".format(d_str)
        },
        {
          "figure": "{:.1f}%".format(last_row['Positive tests rate']),
          "subheader": "For {}".format(d_str)
        }
    ]
  }