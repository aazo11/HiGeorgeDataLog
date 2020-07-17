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

def process_data(cap):
  icu = cap[cap['bed_type'] == 'Intensive Care'].sort_values('date', ascending=False)
  other = icu[icu['status'] == 'Other Patients']['count']
  covid = icu[icu['status'] == 'COVID-19 (Confirmed & Suspected)']['count']
  avail = icu[icu['status'] == 'Available']['count']
  date = list(set(list(icu['date'])))
  date.sort(reverse=True)
  d = {'COVID': list(covid), 'Available': list(avail), 'Other': list(other)}
  df = pd.DataFrame(data=d, index=date)
  return df

def get_updated_data(df):
  first_row = df.head(1).iloc[0]
  prev_day = df.head(2).iloc[1]
  d_str = dt.datetime.strptime(first_row.name, '%Y-%m-%dT%H:%M:%S.%f').strftime('%-m/%-d/%Y')
  d_today_str = dt.datetime.now(pytz.timezone('US/Pacific')).strftime('%-m/%-d/%Y')
  us = get_us_data()
  return {
    "smart_tiles": [
      {
        "figure": short_format(first_row['COVID'] + first_row['Other']),
        "subheader": "As of {}".format(d_str),
        "unit": "{:+}".format(first_row['COVID'] + first_row['Other'] - (prev_day['COVID'] + prev_day['Other'])),
        "value_change": round(percent_change(prev_day['COVID'] + prev_day['Other'], first_row['COVID'] + first_row['Other']), 1)
      },
      {
        "figure": short_format(first_row['COVID']),
        "subheader": "As of {}".format(d_str),
        "unit": "{:+}".format(first_row['COVID'] - prev_day['COVID']),
        "value_change": round(percent_change(prev_day['COVID'], first_row['COVID']), 1)
      },
      {
        "figure": short_format(us["hospitalizedCurrently"]),
        "subheader": "As of {}".format(d_today_str)
      }
    ]
  }