import pandas as pd
import numpy as np
import datetime as dt
import requests as rq
import io
import pytz
import sys

sys.path.insert(0,'..')
import jhu_utils
from script_utils import *


def preprocess(**kwargs):
    return None


def get_hash(df, **kwargs):
    return None


def process_data(states, **kwargs):
    date = states[(states['Region'] == 'San Francisco') & (states['Date']>'2020-03-10')][['Date']].set_index('Date')
    santaclara = states[(states['Region'] == 'Santa Clara') & (states['Date']>'2020-03-10')][['Date', 'Estimated Effective R']].set_index('Date').rename(columns=lambda t: "Santa Clara")
    alam = states[(states['Region'] == 'Alameda') & (states['Date']>'2020-03-10')][['Date', 'Estimated Effective R']].set_index('Date').rename(columns=lambda t: "Alameda")
    cc = states[(states['Region'] == 'Contra Costa') & (states['Date']>'2020-03-10')][['Date', 'Estimated Effective R']].set_index('Date').rename(columns=lambda t: "Contra Costa")
    marin = states[(states['Region'] == 'Marin') & (states['Date']>'2020-03-10')][['Date', 'Estimated Effective R']].set_index('Date').rename(columns=lambda t: "Marin")
    smateo = states[(states['Region'] == 'San Mateo') & (states['Date']>'2020-03-10')][['Date', 'Estimated Effective R']].set_index('Date').rename(columns=lambda t: "San Mateo")
    sf = states[(states['Region'] == 'San Francisco') & (states['Date']>'2020-03-10')][['Date', 'Estimated Effective R']].set_index('Date').rename(columns=lambda t: "San Francisco")
    
    return pd.concat((date, santaclara, alam, cc, marin, smateo, sf), axis=1)


def get_updated_data(df, di, **kwargs):
    return None


CSV_URL = "https://ca-covid-r.info/ca_daily_cases_and_r.csv"