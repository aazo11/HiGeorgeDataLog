import pandas as pd
import numpy as np

def process_data(imported):
    nyc = pd.DataFrame()
    nyc['Deaths'] = imported['BK_DEATH_COUNT']
    nyc['Cases'] = imported['BK_CASE_COUNT']
    nyc['Total Deaths'] = np.cumsum(nyc['Deaths'])
    
    average = list(np.zeros(4)) + list(np.ones(2)*0.5)
    for i in range(7,len(nyc)+1):
        average += [np.mean(nyc['Cases'][i-7:i])]

    nyc['7 day average'] = average
    
    return nyc

def get_tiles(nyc):
    print(sum(nyc['Cases']))
    return []
