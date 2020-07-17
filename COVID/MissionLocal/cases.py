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
  j = rq.get("https://covidtracking.com/api/v1/states/{}/current.json".format(state)).json()
  return j[field] if field else j

def percent_change(old, new):
  return (new - old) / old * 100

def process_data(sfcases):
  cases = sfcases[['specimen_collection_date', 'case_count']].groupby('specimen_collection_date').sum()
  average = list(np.zeros(6))
  for i in range(7,len(cases)+1):
      average += [np.mean(cases['case_count'][i-7:i])]
  cases['7 day average'] = average
  return cases

def get_updated_data(df):
  last_row = df.tail(1).iloc[0]
  d_today_str = dt.datetime.now(pytz.timezone('US/Pacific')).strftime('%-m/%-d/%Y')
  us = get_us_data()
  ca = get_state_data('ca')
  return {
    "smart_tiles": [
        {

        },
        {

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