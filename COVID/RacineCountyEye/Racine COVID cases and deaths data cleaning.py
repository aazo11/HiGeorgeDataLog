#!/usr/bin/env python
# coding: utf-8

# In[242]:


import numpy as np
import pandas as pd
import datetime as dt


# In[243]:


cases = pd.read_csv("Cases_by_day_data.csv",encoding = "utf-16")
deaths = pd.read_csv("Deaths_by_day_data.csv",encoding = "utf-16")


# Cases cleaning

# In[244]:


clean_case = pd.DataFrame()
clean_case_values = pd.DataFrame(cases.values)[0].str.split('\t')
for i in np.arange(4):
    clean_case[i] = clean_case_values.str[i]
clean_case[0] = cases.index.values


# In[245]:


clean_case.rename({
    0: "Date",
    1: "Note",
    2: "County",
    3: "Cases per day"
}, axis=1 , inplace = True)


# In[246]:


clean_case = clean_case.sort_index(ascending=False)
case_avg = clean_case['Cases per day'].rolling(7).mean()
clean_case['7 day rolling case average'] = case_avg
clean_case.to_csv("Racine_County_COVID_Cases.csv")


# Deaths cleaning

# In[247]:


clean_death = pd.DataFrame()
clean_death_values = pd.DataFrame(deaths.values)[0].str.split('\t')
for i in np.arange(4):
    clean_death[i] = clean_death_values.str[i]
clean_death[0] = deaths.index.values


# In[248]:


clean_death.rename({
    0: "Date",
    1: "Note",
    2: "County",
    3: "Deaths per day"
}, axis=1 , inplace = True)


# In[249]:


clean_death['Deaths per day'] = clean_death['Deaths per day'].astype(int)
clean_death = clean_death.sort_index(ascending=False)
death_sum = clean_death['Deaths per day'].cumsum()
clean_death['Total COVID deaths'] = death_sum
clean_death.to_csv("Racine_County_COVID_Deaths.csv")


# In[ ]:




