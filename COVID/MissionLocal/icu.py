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


# %%
def preprocess(**kwargs):
    return None


# %%
def get_hash(df, **kwargs):
    return None


# %%
def process_data(hosp, **kwargs):
  date = list(set(list(hosp['reportdate'])))
  date.sort()
  acute = hosp[hosp['dphcategory'] == 'Med/Surg'][['reportdate','patientcount']].groupby('reportdate').sum()
  icu = hosp[hosp['dphcategory'] == 'ICU'][['reportdate','patientcount']].groupby('reportdate').sum()
  hosp_new = pd.DataFrame()
  hosp_new['Date'] = [d.split('T')[0] for d in date]
  hosp_new['Acute care COVID patients'] = acute.iloc[:].values
  hosp_new['ICU COVID patients'] = icu.iloc[:].values
  return hosp_new


# %%
def get_updated_data(df, di, **kwargs):
  last_row = df.tail(1).iloc[0]
  d_str = dt.datetime.strptime(last_row["Date"], "%Y-%m-%d").strftime("%-m/%-d")
  return {
    "smart_tiles": [
        {
          "figure": short_format(last_row["ICU COVID patients"]),
          "subheader": "As of {}".format(d_str)
        },
        {
          "figure": short_format(last_row["Acute care COVID patients"]),
          "subheader": "As of {}".format(d_str)
        }
    ]
  }


# %%
CSV_URL = "https://data.sfgov.org/resource/nxjg-bhem.csv?$order=reportdate"