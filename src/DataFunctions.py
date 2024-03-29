import pandas as pd
import geopandas as gpd

def get_months():
    """
        Returns a list with all months in a year with the same naming schemes as the T08 DataFrame
    """
    return ['Jan.', 'Febr.', 'März', 'April', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sept.', 'Okt.', 'Nov.', 'Dez.']

def get_months_english():
    """
        Returns a list with all months in a year with the same naming schemes as the T08 DataFrame
    """
    return ['Jan.', 'Febr.', 'March', 'April', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']


def get_crime_name(data:pd.DataFrame, key:str):
    """Get crime names based on the crime names of the newest yearly report

    Args:
        data (pd.DataFrame): Crime Table
        key (str): Crime key

    Returns:
        crime name (str): Returns the crime name
    """
    return data.loc[data['Schlüssel'] == key]['Straftat'].iloc[0]

def get_column_with_value(data:pd.DataFrame, column:str, value):
    """Get column of the dataframe

    Args:
        data (pd.DataFrame): Crime Table
        column (str): Column of the dataframe in which value has to be searched
        value : value for which has be be searched in the given column

    Returns:
        data (pd.DataFrame): Returns all rows where the column matches the given value
    """
    return data[data[column] == value]
    

def get_cases_by_key(data:pd.DataFrame, key:str):
    """ 
        Returns cases of the crime table with a given crime key

    Args:
        data (pd.DataFrame): Crime Table
        key (str): crime key describing the wanted crime

    Returns:
        data (pd.DataFrame): Row(s) with given crime key
    """
    return get_column_with_value(data, 'Schlüssel', key)

def transform_df_to_list(data:pd.DataFrame, years:range):
    """returns list of tuples. Each elements represents one year the crime table of that year in the tuple

    Args:
        data (pd.DataFrame): Crime Table
        years (range): years of crime tables

    Returns:
        lists of years (list(tuple)): List of data for each year. Tuple: (year, crime table of year)
    """
    df = list()
    for year in years:
        df.append((year, data[year]))
    return df

def get_monthly_cases(df_year:pd.DataFrame, key:str, sum_duplicated_key:bool):
    """Returns Lists values of monthly granularity data.

    Args:
        df_year (pd.DataFrame): Dataframe containing crime data for the year of interest
        key (str): Crime Key
        sum_duplicated_key (bool): Whether rows with the same key should be summed up

    Returns:
        monthly data (list): Monthly data of a year comprised in a list of lists
    """
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
            

def transform_monthly_data_to_list(data:list[tuple[int, pd.DataFrame]], key:str, sum_duplicated_key:bool):
    """ Returns list of lists. 
        Each list represents one year and contains cases of certain crime from Jan. to Dec.
        Crimes where time is uncertain are discarded

    Args:
        data (list[tuple[int, pd.DataFrame]]): Generated by transform_df_to_list
        key (str): Crime key
        sum_duplicated_key (bool): Whether rows with the same key should be summed up
    
    Returns:
        Lists of Lists containing crime data in monthly granularity. Each list stands for the crime data 
        of one year and contains values for the crimes with the given key from January to December.
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



# Get flattend list of months of years for the x-axis label
def create_x_labels(years, use_english_months:bool=False):
    """Generates a flattened list of months for using it in plots. 

    Args:
        years (range): All years for which the months should be in the resulting list

    Returns:
        x axis labels list(str): List with names of months for each year in the data
    """
    months = None
    if use_english_months:
        months = get_months_english()
    else:
        months = get_months()
    months_year = list()
    for i in years:
        with_year = list(month + ' ' + str(i) for month in months)

        months_year.append(with_year)
    
    flat_months_year = [element for year in months_year for element in year]
    return flat_months_year


def get_key_col(df:pd.DataFrame,key:str,col:str=None) -> pd.Series:
    '''Copy slice of data frame specified by key and column
    
    Params:
    df: Full data frame to select from
    key: Numerical crime key
    col: Column header, optional. Returns all columns if not specified (default: None)
    
    Returns: Slice of data'''

    if col is None:
        return pd.DataFrame(df.loc[df.Schlüssel == key,:]).reset_index(drop=True)
    return pd.DataFrame(df.loc[df.Schlüssel == key, ['Bundesland',col]]).rename(columns={col:'data'}).reset_index(drop=True)


def add_geomery(df:pd.DataFrame,geo:gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    '''Adds geometry of federal states to slice of data frame
    
    Params:
    df: Data frame containing data per federal state (requires: 'Bundesland' column)
    geo: Geo data frame containing the geometry of each federal state (requires: 'Bundesland' column)
    
    Returns: Augmented data with geometry ready for plotting'''

    return gpd.GeoDataFrame(pd.merge(df,geo,on='Bundesland'),geometry='geometry')


# Methods that are not used anymore but might be needed again
def get_yearly_cases_by_key(key:str, data:tuple((int, pd.DataFrame)), sum_same_key:bool, column_of_interest:str='Anzahl erfasste Fälle'):
    """_summary_

    Args:
        key (str): _description_
        data (pd.DataFrame): _description_
        sum_same_key (bool): _description_
        years (range): _description_

    Returns:
        _type_: _description_
    """
    cases_by_year = list()
    data_years = list()
    for year, df in data:      
        if sum_same_key:
            # summing up the entries in df that have an identical key
            cases_curr_year = 0
            for i in range(len(df[column_of_interest][df['Schlüssel'] == key])):
                cases_curr_year += df[column_of_interest][df['Schlüssel'] == key].iloc[i]
        else:
            # taking only the first entry that uses the key in df
            cases_curr_year = df[column_of_interest][df['Schlüssel'] == key].iloc[0]
            
        cases_by_year.append(cases_curr_year)
        data_years.append(year)

    return data_years, cases_by_year