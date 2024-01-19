import pandas as pd

tesssst = "test"

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

def transform_df_to_list(data, years):
    df = list()
    for year in years:
        df.append((year, data[year]))
    return df

def get_monthly_cases(df_year, key, sum_duplicated_key):
    cases_curr_year = list() 
    months = get_months()           
    for month in months:
        if sum_duplicated_key:
            # summing up the entries in df that have an identical key
            cases_month = 0
            for i in range(len(df_year[month][df_year['Schlüssel'] == key])):
                cases_month += df_year[month][df_year['Schlüssel'] == key].iloc[i]
        else:
            # taking only the first entry that uses the key in df
            cases_month = df_year[month][df_year['Schlüssel'] == key].iloc[0]
        
        cases_curr_year.append(cases_month)
    return cases_curr_year
            

def transform_monthly_data_to_list(data:list[tuple[int, pd.DataFrame]], key, sum_duplicated_key:bool):
    """
        Returns list of lists. 
        Each list represents one year and contains cases of certain crime from Jan. to Dec.
        Crimes where time is uncertain are discarded
    """
    cases_by_year = list()
    prev_year = None
    for year, df_year in data:
        # This is in the first year
        if prev_year is None:
            cases_curr_year = get_monthly_cases(df_year, key, sum_duplicated_key)    
            cases_by_year.append(cases_curr_year)
            prev_year = year
            continue # Continue as yearly data for the first year has already been added
        
        # This is the case when some years are missing in the data
        while prev_year+1 != year and prev_year < year:
            prev_year = prev_year + 1
            cases_by_year.append([0,0,0,0,0,0,0,0,0,0,0,0])
            
        
        # After adding empty lists for every missing year, add the curent existing year
        cases_curr_year = get_monthly_cases(df_year, key, sum_duplicated_key)  
        cases_by_year.append(cases_curr_year)
        prev_year = year

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

# Get flattend list of months of years for the x-axis label
def create_x_labels(years):
    months_year = list()
    for i in years:
        with_year = list(month + ' ' + str(i) for month in get_months())
        months_year.append(with_year)
    
    flat_months_year = [element for year in months_year for element in year]
    return flat_months_year