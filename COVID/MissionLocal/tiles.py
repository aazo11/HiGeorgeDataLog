import pandas as pd
import numpy as np
import datetime as dt
import requests as rq
import pytz

def short_format(num):
    if num > -10000 and num < 10000:
        return '{:,.4g}'.format(num)
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def get_us_data(date=None, field=None):
    """
    Returns a JSON object with the following notable fields:
    positive, negative, death, total (number of tests), recovered
    hospitalizedCurrently, inIcuCurrently, onVentilatorCurrently
    deathIncrease, hospitalizedIncrease, positiveIncrease, negativeIncrease, totalTestResultsIncrease
    """
    j = rq.get("https://covidtracking.com/api/v1/us/{}.json".format(date.strftime('%Y%m%d') if date else "current")).json()
    j = j if date else j[0]
    return j[field] if field else j

def get_state_data(state, date=None, field=None):
  """
  Returns a JSON object with the following notable fields:
    positive, negative, death, total (number of tests), recovered
    hospitalizedCurrently, inIcuCurrently, onVentilatorCurrently
    deathIncrease, hospitalizedIncrease, positiveIncrease, negativeIncrease, totalTestResultsIncrease
  """
  j = rq.get("https://covidtracking.com/api/v1/states/{}/{}.json".format(state, date.strftime('%Y%m%d') if date else "current")).json()
  return j[field] if field else j

def percent_change(old, new):
  return (new - old) / old * 100

def process_data(df):
  return df

def get_updated_data(df, di):
  now = dt.datetime.now(pytz.timezone('US/Pacific'))
  us = get_us_data()
  us_prev = get_us_data(date=now - dt.timedelta(days=1))
  ca = get_state_data('ca')
  ca_prev = get_state_data('ca', date=now - dt.timedelta(days=1))
  return {
    "smart_tiles": [
        {
          "figure": short_format(ca['positiveIncrease']),
          "unit": "{}{}".format('+' if (ca['positiveIncrease'] - ca_prev['positiveIncrease']) >= 0 else '', short_format(ca['positiveIncrease'] - ca_prev['positiveIncrease'])),
          "value_change": round(percent_change(ca_prev['positiveIncrease'], ca['positiveIncrease']), 1)
        },
        {

        },
        {

        },
        {
          "figure": short_format(us['positiveIncrease']),
          "unit": "{}{}".format('+' if (us['positiveIncrease'] - us_prev['positiveIncrease']) >= 0 else '', short_format(us['positiveIncrease'] - us_prev['positiveIncrease'])),
          "value_change": round(percent_change(us_prev['positiveIncrease'], us['positiveIncrease']), 1)
        }
    ]
  }