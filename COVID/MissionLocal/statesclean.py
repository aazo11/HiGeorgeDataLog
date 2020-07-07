import pandas as pd
import numpy as np

states = pd.read_csv('statewide_cases.csv')
date = states[states['county'] == 'San Francisco']['date']
santaclara = states[states['county'] == 'Santa Clara']['totalcountdeaths']
alam = states[states['county'] == 'Alameda']['totalcountdeaths']
cc = states[states['county'] == 'Contra Costa']['totalcountdeaths']
santacruz = states[states['county'] == 'Santa Cruz']['totalcountdeaths']
smateo = states[states['county'] == 'San Mateo']['totalcountdeaths']
sf = states[states['county'] == 'San Francisco']['totalcountdeaths']

# d = {'Date': date, 'Santa Clara': santaclara, 'Alameda': alam, 'Contra Costa': cc, 'Santa Cruz': santacruz, 'San Mateo': smateo, 'San Francisco': sf}
deaths = pd.DataFrame()
# deaths['Date'] = date
# deaths.index = date
deaths['Date'] = date.iloc[:].values
deaths['Santa Clara'] = santaclara.iloc[:].values
deaths['SF'] = sf.iloc[:].values
deaths['Alameda'] = alam.iloc[:].values
deaths['Contra Costa'] = cc.iloc[:].values
deaths['Santa Cruz'] = santacruz.iloc[:].values
deaths['San Mateo'] = smateo.iloc[:].values
deaths.to_csv('state_deaths.csv')
# deaths.index = date.T
# deaths_t = deaths.T

# deaths_t.to_csv('state_t_deaths.csv')
