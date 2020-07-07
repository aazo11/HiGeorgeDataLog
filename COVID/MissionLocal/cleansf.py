import pandas as pd
import numpy as np

cap = pd.read_csv('sfhospitalcapacity.csv')

#  cap[cap['Status'] == 'COVID-19 (Confirmed & Suspected)'].sort_values('Date', ascending=False)
icu = cap[cap['Bed Type'] == 'Intensive Care'].sort_values('Date', ascending=False)
other = icu[icu['Status'] == 'Other Patients']['Count']
covid = icu[icu['Status'] == 'COVID-19 (Confirmed & Suspected)']['Count']
avail = icu[icu['Status'] == 'Available']['Count']
date = list(set(list(icu['Date'])))
date.sort(reverse=True)
d = {'COVID': list(covid), 'Available': list(avail), 'Other': list(other)}
df = pd.DataFrame(data=d, index=date)
df.to_csv('sfhospclean.csv')

tests = pd.read_csv('sftests.csv')
tests.sort_values('specimen_collection_date', ascending = False)
rate = tests[['specimen_collection_date', 'pct', 'tests']]
rate['Positive tests rate'] = rate['pct'] * 100
rate['Total tests'] = rate['tests']
rate.to_csv('sfrateclean.csv')

sfcases = pd.read_csv('sfcases.csv')
cases = sfcases[['Specimen Collection Date', 'Case Count']].groupby('Specimen Collection Date').sum()
cases.to_csv('sfcasescleaned.csv')

deaths = sfcases[sfcases['Case Disposition'] == 'Death'][['Specimen Collection Date', 'Case Count']].groupby('Specimen Collection Date').sum()
final = cases.join(deaths, lsuffix='_caller', rsuffix='_other').fillna(0)
sumd = np.cumsum(final['Case Count_other'])
final['sum'] = sumd
final.to_csv('sfdeaths.csv')