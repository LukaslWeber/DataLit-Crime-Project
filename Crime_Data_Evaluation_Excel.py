import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

wd = os.getcwd()
os.chdir(wd + '/Datasets/PKS/2022/Zeitliche-Gliederung')

# In the csv file commas are used to structure large numbers
# dots are used as seperator for decimal numbers eg 3.5%
# data = pd.read_csv('T01-Faelle.csv', encoding='latin_1', skiprows=0, header=1,
#                    sep=';', decimal='.', thousands=',')

data = pd.read_excel('T01-Faelle.xlsx', skiprows=14, header=0, decimal='.', thousands=',')

print(data.head())
print(data.dtypes)

# Get an overview how the crimes are distinguished
# crimes = []
# for crime in list(data['Straftat']):
#    if crime not in crimes:
#         crimes.append(crime)
#
# print(crimes)
# print('Number of different categories of crimes: %i' % len(crimes))

# Get an overview of the crime keys

keys = []
for key in list(data[1]):
    if key not in keys:
        keys.append(key)

print(keys)
print(len(keys))

Straf_geg_Leben = data[data[1].str.startswith('0')]
print(Straf_geg_Leben)


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
