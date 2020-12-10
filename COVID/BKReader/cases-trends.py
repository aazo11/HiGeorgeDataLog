import pandas as pd
import numpy as np
import requests as rq
import pytz
from datetime import datetime

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

def process_data(imported):
    nyc = pd.DataFrame()
    nyc['Deaths'] = imported['BK_DEATH_COUNT']
    nyc['Cases'] = imported['BK_CASE_COUNT']
    nyc['Total Deaths'] = np.cumsum(nyc['Deaths'])
    nyc['Date'] = imported['date_of_interest']
    
    average = list(np.zeros(4)) + list(np.ones(2)*0.5)
    for i in range(7,len(nyc)+1):
        average += [np.mean(nyc['Cases'][i-7:i])]

    nyc['7 day average'] = average
    
    return nyc

def get_updated_data(nyc, di):
    last_row = nyc.tail(1).iloc[0]
    d_str = datetime.strptime(last_row['Date'], '%m/%d/%Y').strftime('%-m/%-d')
    d_today_str = datetime.now(pytz.timezone('US/Pacific')).strftime('%-m/%-d')
    return {
        "smart_tiles": [
            {
                "figure": short_format(sum(nyc['Cases'])),
                "subheader": "As of {}".format(d_today_str)
            },
            {
                "figure": short_format(last_row['Cases']),
                "subheader": "On {}".format(d_str)
            },
            {
                "figure": short_format(get_us_data('positive')),
                "subheader": "As of {}".format(d_today_str)
            }
        ]
    }
