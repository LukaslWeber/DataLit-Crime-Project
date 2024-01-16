import pandas as pd

def get_months():
    return ['Jan.', 'Febr.', 'März', 'April', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sept.', 'Okt.', 'Nov.', 'Dez.']

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

def transform_yearly_data_to_list(data, years):
    df = list()
    for year in years:
        df.append((year, data[year]))
    return df

def transform_monthly_data_to_list(db_t08, key, years, sum_duplicated_key:bool):
    # returns list of lists. Each list represents one year and contains cases of certain crime from Jan. to Dec.
    cases_by_year = list()
    for year in years:
        df_year = db_t08[year]
        cases_curr_year = list()            
        for month in get_months():
            if sum_duplicated_key:
                # summing up the entries in df that have an identical key
                cases_month = 0
                for i in range(len(df_year[month][df_year['Schlüssel'] == key])):
                    cases_month += df_year[month][df_year['Schlüssel'] == key].iloc[i]
            else:
                # taking only the first entry that uses the key in df
                cases_month = df_year[month][df_year['Schlüssel'] == key].iloc[0]
            
            cases_curr_year.append(cases_month)
            
        cases_by_year.append(cases_curr_year)

    return(cases_by_year)

def get_yearly_cases_by_key(key, data, sum_same_key, years):
    cases_by_year = list()
    data_years = list()
    for year in years:
        df = data[year]           
        if sum_same_key:
            # summing up the entries in df that have an identical key
            cases_curr_year = 0
            for i in range(len(df['Anzahl erfasste Fälle'][df['Schlüssel'] == key])):
                cases_curr_year += df['Anzahl erfasste Fälle'][df['Schlüssel'] == key].iloc[i]
        else:
            # taking only the first entry that uses the key in df
            cases_curr_year = df['Anzahl erfasste Fälle'][df['Schlüssel'] == key].iloc[0]
            
        cases_by_year.append(cases_curr_year)
        data_years.append(year)

    return data_years, cases_by_year