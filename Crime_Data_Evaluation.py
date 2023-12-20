import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

wd = os.getcwd()
os.chdir(wd + '/Datasets/PKS/2022/Zeitliche-Gliederung')

data = pd.read_excel('T01-Faelle.xlsx', skiprows=14, header=0, decimal='.', thousands=',')

# Get an overview how the crimes are distinguished
# crimes = []
# for crime in list(data['Straftat']):
#    if crime not in crimes:
#         crimes.append(crime)
#
# print(crimes)
# print('Number of different categories of crimes: %i' % len(crimes))

# Get an overview of the crime keys
# keys = []
# for key in list(data[1]):
#     if key not in keys:
#         keys.append(key)
#
# print(keys)
# print(len(keys))


# Rename data columns
new_names = ['Schluessel', 'Straftat', 'Jahr', 'erfasste Faelle', 'HZ', 'Versuche - Anzahl',
             'Versuche - Anteil in %', 'mit Schusswaffe gedroht', 'mit Schusswaffe geschossen',
             'Aufklaerungsquote in %', 'Tatverdaechtige insgesamt', 'Nichtdeutsche Tatverdaechtige - Anzahl',
             'Nichtdeutsche Tatverdaechtige - Anteil in %']

for old_name, new_name in zip(data.columns, new_names):
    data.rename(columns={old_name: new_name}, inplace=True)

print(data.head())


# Summarize/Categorize Crimes in new DataFrames
def get_crimes(key_val, key_col='Schluessel'):
    crime_df = data[data[key_col].str.startswith(key_val)]
    return crime_df


# TODO: Genaue Kategorisierung ueberlgen und durchfuehren
straftaten_gegen_leben = get_crimes('0')
rauschgiftdelikte_nach_BtMG = get_crimes('73')

print(rauschgiftdelikte_nach_BtMG.head())


crime_of_interest = get_crimes('0')
years = list(crime_of_interest['Jahr'])
cases = list(crime_of_interest['erfasste Faelle'])

diff_crimes = []
for crime in crime_of_interest['Straftat']:
    if crime not in diff_crimes:
        diff_crimes.append(crime)



sum_crimes = crime_of_interest.groupby('Jahr')['erfasste Faelle'].sum().reset_index()
sum_crimes_cases = list(sum_crimes['erfasste Faelle'])
sum_crimes_years = list(sum_crimes['Jahr'])

plt.plot(years, cases)
#plt.plot(sum_crimes_years, sum_crimes_cases, color='red')
plt.legend(diff_crimes)
plt.show()

# Print some crimes
# relevant_crimes = ['Straftaten gegen das Leben', 'Mord § 211 StGB darunter:',
#               'Alle übrigen (vorsätzlichen) Tötungen §§ 212, 213, 216, 217 StGB']
# crimes
# for crime in relevant_crimes:
#     data_crime = data.loc[data['Straftat'] == crime]
#     years = list(data_crime.loc[:, 'Jahr'])
#     cases = list(data_crime.loc[:, 'erfasste Faelle'])
#     # cases = [eval(case) for case in cases]
#     print(crime, str(years))
#     plt.plot(years, cases)

# plt.yscale('log')
# plt.legend(relevant_crimes, loc='upper right')
# plt.show()
