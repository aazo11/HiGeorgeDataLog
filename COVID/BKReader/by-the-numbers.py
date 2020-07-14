import pandas as pd
import numpy as np

def short_format(num):
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
    nyc['Date'] = imported['DATE_OF_INTEREST']
    
    average = list(np.zeros(4)) + list(np.ones(2)*0.5)
    for i in range(7,len(nyc)+1):
        average += [np.mean(nyc['Cases'][i-7:i])]

    nyc['7 day average'] = average
    
    return nyc

def get_tiles(nyc):
    return [
        {
            "figure": short_format(nyc.tail(1).iloc[0]['Cases']),
            "subheader": "On {}".format(nyc.tail(1).iloc[0]['Date'])
        },
        {
            "figure": short_format(nyc.tail(1).iloc[0]['Deaths']),
            "subheader": "On {}".format(nyc.tail(1).iloc[0]['Date'])
        },
        {
            "figure": short_format(sum(nyc['Cases'])),
            "subheader": "As of {}".format(nyc.tail(1).iloc[0]['Date'])
        },
        {
            "figure": short_format(nyc.tail(1).iloc[0]['Total Deaths']),
            "subheader": "As of {}".format(nyc.tail(1).iloc[0]['Date'])
        }
    ]