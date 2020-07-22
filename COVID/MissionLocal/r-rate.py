import pandas as pd
import numpy as np
import datetime as dt
import requests as rq
import pytz

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
    return None