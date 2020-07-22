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

def process_data(states):
  date = states[(states['Region'] == 'San Francisco') & (states['Date']>'2020-03-10')]['Date']
  santaclara = states[(states['Region'] == 'Santa Clara') & (states['Date']>'2020-03-10')]['Estimated Effective R']
  alam = states[(states['Region'] == 'Alameda') & (states['Date']>'2020-03-10')]['Estimated Effective R']
  cc = states[(states['Region'] == 'Contra Costa') & (states['Date']>'2020-03-10')]['Estimated Effective R']
  marin = states[(states['Region'] == 'Marin') & (states['Date']>'2020-03-10')]['Estimated Effective R']
  smateo = states[(states['Region'] == 'San Mateo') & (states['Date']>'2020-03-10')]['Estimated Effective R']
  sf = states[(states['Region'] == 'San Francisco') & (states['Date']>'2020-03-10')]['Estimated Effective R']
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
  last_row = df.tail(1).iloc[0]
  d_today_str = dt.datetime.now(pytz.timezone('US/Pacific')).strftime('%-m/%-d')
  us = get_us_data()
  ca = get_state_data('ca')
  return {
    "smart_tiles": [
        {

        },
        {

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