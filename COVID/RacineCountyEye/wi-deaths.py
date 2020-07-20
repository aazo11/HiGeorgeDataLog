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


def process_data(wi):
    wi.fillna(0, inplace=True)
    wi = wi.sort_values(by = 'LoadDttm')
    new_cases = wi['POS_NEW'].astype(int)
    new_deaths = wi['DTH_NEW'].astype(int)
    new_deaths[new_deaths<0] = 0
    new_cases[new_cases<0] = 0

    dates = wi['LoadDttm'].apply(lambda s: "{0[1]}/{0[2]}".format(s.split('/')).split(' ')[0])

    clean = pd.DataFrame({'Date': dates,
              'Cases per day': new_cases,
             'Deaths per day': new_deaths})
    case_avg = clean['Cases per day'].rolling(7).mean()
    clean['7 day rolling case average'] = case_avg
    death_sum = clean['Deaths per day'].cumsum()
    clean['Total cases'] = clean['Cases per day'].cumsum()
    clean['Total deaths'] = death_sum.astype(int)

    return clean

def get_updated_data(df, di):
    last_row = df.tail(1).iloc[0]
    d_str = (dt.datetime.strptime(last_row['Date'], '%m/%d').replace(year=dt.datetime.now().year) - dt.timedelta(days=1)).strftime('%-m/%-d')
    d_today_str = dt.datetime.now(pytz.timezone('US/Pacific')).strftime('%-m/%-d')
    return {
        "smart_tiles": [
            {
                "figure": short_format(last_row['Deaths per day']),
                "subheader": "On {}".format(d_str)
            },
            {
                "figure": short_format(last_row['Total deaths']),
                "subheader": "As of {}".format(d_today_str)
            }
        ]
    }