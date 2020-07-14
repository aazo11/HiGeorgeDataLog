import pandas as pd
import numpy as np

def process_data(zipc):
    finalzip = pd.DataFrame()
    finalzip['Total COVID Cases'] = zipc['COVID_CASE_COUNT']
    finalzip['Total COVID Deaths'] = zipc['COVID_DEATH_COUNT']
    finalzip['Positive test rate'] = zipc['PERCENT_POSITIVE']
    finalzip.index = zipc['MODIFIED_ZCTA']

    return finalzip

def create_smart_tiles(nyc):
    print(sum(nyc['Cases']))
    return []