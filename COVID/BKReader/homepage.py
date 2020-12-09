import pandas as pd
import numpy as np
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
    d_local = datetime.now(pytz.timezone('US/Eastern'))
    d_today_str = d_local.strftime('%-m/%-d')
    d_update_str = d_local.strftime('%A %-I:%M %p')
    return {
        "smart_tiles": [
            {
                "figure": short_format(last_row['Cases']),
                "unit": "On {}".format(d_str)
            },
            {
                "figure": short_format(last_row['Deaths']),
                "unit": "On {}".format(d_str)
            },
            {
                "figure": short_format(sum(nyc['Cases'])),
                "unit": "As of {}".format(d_today_str)
            },
            {
                "figure": short_format(last_row['Total Deaths']),
                "unit": "As of {}".format(d_today_str)
            }
        ],
        "subtitle": "Updated {} ET".format(d_update_str)
    }