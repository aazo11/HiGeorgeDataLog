import pandas as pd
import numpy as np
import datetime as dt
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


def process_data(df):
    cols = {
        "NAME": "County",
        "LoadDttm": "Date",
        "NEGATIVE": "Total negative tests",
        "POSITIVE": "Total cases",
        "DTH_NEW": "Deaths per day",
        "POS_NEW": "Cases per day",
        "NEG_NEW": "Negative tests per day",
        "TEST_NEW": "Tests per day"
    }

    new_df = df[cols.keys()].rename(columns=cols).fillna(0)
    new_df['Deaths per day'] = new_df['Deaths per day'].astype(int)
    new_df['Cases per day'] = new_df['Cases per day'].astype(int)
    new_df['Negative tests per day'] = new_df['Negative tests per day'].astype(int)
    new_df['Tests per day'] = new_df['Tests per day'].astype(int)
    new_df['Total negative tests'] = new_df['Total negative tests'].astype(int)
    new_df['Date'] = pd.to_datetime(new_df['Date'])
    new_df = new_df.sort_values(by='Date')
    new_df['Date'] = new_df['Date'].apply(lambda x: x.strftime("%-m/%-d/%Y"))
    new_df['Total deaths'] = new_df['Deaths per day'].cumsum()
    new_df['7 day rolling case average'] = new_df['Cases per day'].rolling(7).mean()
    new_df['7 day rolling deaths average'] = new_df['Deaths per day'].rolling(7).mean()
    tests = new_df[['Cases per day','Tests per day']].rolling(7).mean()
    new_df['7 day rolling tests average'] = tests['Cases per day'] / tests['Tests per day']
    return new_df.reset_index(drop=True)


def get_updated_data(df, di):
    last_row = df.tail(1).iloc[0]
    prev_row = df.tail(2).iloc[0]
    d_str = (dt.datetime.strptime(last_row['Date'], '%m/%d/%Y') - dt.timedelta(days=1)).strftime('%-m/%-d')
    d_local = dt.datetime.now(pytz.timezone('US/Central'))
    d_today_str = d_local.strftime('%-m/%-d')
    d_update_str = d_local.strftime('%A %-I:%M %p')
    return {
        "subtitle": "Updated {} CT".format(d_update_str),
        "smart_tiles": [
            {
                "figure": short_format(last_row['Cases per day']),
                "subheader": "On {}".format(d_str)
            },
            {
                "figure": short_format(last_row['Total cases']),
                "subheader": "As of {}".format(d_today_str)
            },
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