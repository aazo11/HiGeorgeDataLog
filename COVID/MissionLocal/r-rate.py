import pandas as pd
import numpy as np
import datetime as dt
import requests as rq
import pytz

def process_data(r):
    final_r = r[r['Region'] == 'San Francisco']
    final_r = final_r[final_r['Date'] > '2020-03-11']
    final_r['one'] = 1
    return final_r

def get_updated_data(df, di):
    return None