import pandas as pd
from variables import months

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

def transform_data_to_list(data, years):
    df = list()
    for year in years:
        df.append((year, data[year]))
    return df

def get_monthly_cases(db_t08_list, key, years, sum_duplicated_key:bool):
    # returns list of lists. Each list represents one year and contains cases of certain crime from Jan. to Dec.
    cases_by_year = list()
    for year in years:
        df_year = db_t08_list[year]
        cases_curr_year = list()            
        for month in months:
            if sum_duplicated_key:
                # summing up the entries in df that have an identical key
                cases_month = 0
                for i in range(len(df_year[month][df['Schlüssel'] == key])):
                    cases_month += df_year[month][df['Schlüssel'] == key].iloc[i]
            else:
                # taking only the first entry that uses the key in df
                cases_month = df_year[month][df_year['Schlüssel'] == key].iloc[0]
            
            cases_curr_year.append(cases_month)
            
        cases_by_year.append(cases_curr_year)

    return(cases_by_year)