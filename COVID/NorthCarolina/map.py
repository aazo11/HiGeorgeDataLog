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
pops = {
    "Alamance County": 169509,
    "Alexander County": 37497,
    "Alleghany County": 11137,
    "Anson County": 24446,
    "Ashe County": 27203,
    "Avery County": 17557,
    "Beaufort County": 46994,
    "Bertie County": 18947,
    "Bladen County": 32722,
    "Brunswick County": 142820,
    "Buncombe County": 261191,
    "Burke County": 90485,
    "Cabarrus County": 216453,
    "Caldwell County": 82178,
    "Camden County": 10867,
    "Carteret County": 69473,
    "Caswell County": 22604,
    "Catawba County": 159551,
    "Chatham County": 74470,
    "Cherokee County": 28612,
    "Chowan County": 13943,
    "Clay County": 11231,
    "Cleveland County": 97947,
    "Columbus County": 55508,
    "Craven County": 102139,
    "Cumberland County": 335509,
    "Currituck County": 27763,
    "Dare County": 37009,
    "Davidson County": 167609,
    "Davie County": 42846,
    "Duplin County": 58741,
    "Durham County": 321488,
    "Edgecombe County": 51472,
    "Forsyth County": 382295,
    "Franklin County": 69685,
    "Gaston County": 224529,
    "Gates County": 11562,
    "Graham County": 8441,
    "Granville County": 60443,
    "Greene County": 21069,
    "Guilford County": 537174,
    "Halifax County": 50010,
    "Harnett County": 135976,
    "Haywood County": 62317,
    "Henderson County": 117417,
    "Hertford County": 23677,
    "Hoke County": 55234,
    "Hyde County": 4937,
    "Iredell County": 181806,
    "Jackson County": 43938,
    "Johnston County": 209339,
    "Jones County": 9419,
    "Lee County": 61779,
    "Lenoir County": 55949,
    "Lincoln County": 86111,
    "McDowell County": 45756,
    "Macon County": 35858,
    "Madison County": 21755,
    "Martin County": 22440,
    "Mecklenburg County": 1110356,
    "Mitchell County": 14964,
    "Montgomery County": 27173,
    "Moore County": 100880,
    "Nash County": 94298,
    "New Hanover County": 234473,
    "Northampton County": 19483,
    "Onslow County": 197938,
    "Orange County": 148476,
    "Pamlico County": 12726,
    "Pasquotank County": 39824,
    "Pender County": 63060,
    "Perquimans County": 13463,
    "Person County": 39490,
    "Pitt County": 180742,
    "Polk County": 20724,
    "Randolph County": 143667,
    "Richmond County": 44829,
    "Robeson County": 130625,
    "Rockingham County": 91010,
    "Rowan County": 142088,
    "Rutherford County": 67029,
    "Sampson County": 63531,
    "Scotland County": 34823,
    "Stanly County": 62806,
    "Stokes County": 45591,
    "Surry County": 71783,
    "Swain County": 14271,
    "Transylvania County": 34385,
    "Tyrrell County": 4016,
    "Union County": 239859,
    "Vance County": 44535,
    "Wake County": 1111761,
    "Warren County": 19731,
    "Washington County": 11580,
    "Watauga County": 56177,
    "Wayne County": 123131,
    "Wilkes County": 68412,
    "Wilson County": 81801,
    "Yadkin County": 37667,
    "Yancey County": 18069
}

pop_df = pd.DataFrame(data=pops.values(), index=pops.keys()).rename(columns={0: "Population"}).rename_axis("County")
pop_df


# %%
COUNTY = None
STATE = "North Carolina"
TZ = "US/Eastern"


# %%
def preprocess(**kwargs):
    return None


# %%
def get_hash(df, **kwargs):
    return hash_dataframes(jhu_utils.clean_jhu(df, [(STATE, COUNTY)]))


# %%
def process_data(df, **kwargs):
  df = df[df["Province_State"] == STATE]
  df = df[["Admin2", "Confirmed", "Deaths"]]
  df["Admin2"] = df["Admin2"] + " County"
  df = df.set_index("Admin2").rename_axis("County").drop("Unassigned County")
  df = df.rename(columns={"Confirmed": "Total Cases", "Deaths": "Total Deaths"})
  df = pd.concat((df, pop_df), axis=1)
  df["COVID per capita"] = df["Total Cases"] / df["Population"]
  return df


# %%
def get_updated_data(df, di, **kwargs):
  max_idx = df["COVID per capita"].idxmax()
  max_row = df.loc[max_idx]
  return {
    "smart_tiles": [
        {
          "figure": short_format(max_row["Total Cases"]),
          "subheader": max_row.name
        }
    ]
  }


# %%
CSV_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases.csv"