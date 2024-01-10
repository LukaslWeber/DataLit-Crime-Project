import pandas as pd

"""
    Get crime names based on the crime names of the newest yearly report
"""
def get_crime_name(data:pd.DataFrame, key:str):
    return data.loc[data['Schlüssel'] == key]['Straftat'].iloc[0]

def get_column_with_value(data, column, value):
    return data[data[column] == value]
    
# returns list of lists. Each list represents one year and contains cases of certain crime from Jan. to Dec.
def get_cases_by_key(data, key):
    return get_column_with_value(data, 'Schlüssel', key)

