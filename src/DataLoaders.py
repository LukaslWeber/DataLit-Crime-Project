import os
from torch.utils.data import Dataset
import pandas as pd
import numpy as np

class T20DataLoader(Dataset):
    def __init__(self,root_dir:str='Datasets/PKS/'):
        '''Loads and formats the PKS tables of germany grouped by suspect age and sex for all available years in the root directory

        Params:
        root_dir: The root directory containing the yearly directories of tables (default: 'Datasets/PKS/')

        Returns: Iterable dataset indexed by years
        '''
        self.root_dir = root_dir

    def __len__(self):
        return len(os.listdir(self.root_dir)) # assume this table exists for each year
    
    def __getitem__(self,year:int):
        if 2012 > year or year > 2022:
                raise IndexError(f'No data for requested year: {year}.\nNote: There is no official data before 2012 for this table')

        y_path = os.path.join(self.root_dir,str(year))
        
        files_in_path = [file for file in os.listdir(y_path) if 'BU-T20-Tatverdaechtige.' in file]

        # Check whether there is T20 table in the year folder
        if(len(files_in_path) == 0):
            raise Exception(f"T20 table in the folder {y_path} could not be found")

        # If there are multiple, take the first file
        t20_file_path = os.path.join(y_path, files_in_path[0])

        df = pd.read_excel(t20_file_path,skiprows=8,thousands=',',decimal='.', usecols='A:X', names = list(range(1,25)))
        renamedCols = {1: 'Schlüssel', 
                       2: 'Straftat',
                       3: 'Sex',
                       4: 'Anzahl erfasste TV',
                       5: '0-5',
                       6: '6-7',
                       7: '8-9',
                       8: '10-11',
                       9: '12-13',
                       10: '0-13',
                       11: '14-15',
                       12: '16-17',
                       13: '14-17',
                       14: '18-20',
                       15: '0-20',
                       16: '21-22', 
                       17: '23-24',
                       18: '21-24',
                       19: '25-29',
                       20: '30-39',
                       21: '40-49',
                       22: '50-59',
                       23: '>60',
                       24: '>21'}
        df = df.rename(columns=renamedCols)
        # Ensure that keys are always interpreted as strings
        df['Schlüssel'] = df['Schlüssel'].astype(str)
        df = df.reset_index(drop=True)
        
        return df

class T08DataLoader(Dataset):
    def __init__(self,root_dir:str='Datasets/PKS/'):
        '''Loads and formats the base crime tables of germany grouped by month for all available years in the root directory

        Params:
        root_dir: The root directory containing the yearly directories of tables (default: 'Datasets/PKS/')

        Returns: Iterable dataset indexed by years
        '''
        self.root_dir = root_dir

    def __len__(self):
        return len(os.listdir(self.root_dir)) # assume this table exists for each year
    
    def __getitem__(self, year):
        if 2012 > year or year > 2022:
                raise IndexError(f'No data for requested year: {year}.\nNote: There is no official data before 2012 for this table')
        
        y_path = os.path.join(self.root_dir,str(year))
        
        files_in_path = [file for file in os.listdir(y_path) if 'BU-T08-Tatzeit.' in file]

        # Check whether there is T08 table in the year folder
        if(len(files_in_path) == 0):
            raise Exception(f"T08 table in the folder {y_path} could be found")
        
        # If there are multiple, take the first file
        t08_file_path = os.path.join(y_path, files_in_path[0])
        rows_to_skip = 6
        if year == 2015:
            rows_to_skip = 5
        df = pd.read_excel(t08_file_path, skiprows=rows_to_skip, thousands=',', decimal='.')

        # convert the column names to integers (if possible) -> Necessary because of typing errors in column numbers. 
        # Then rename them to the correct names
        df = df.rename(columns=lambda col: int(col) if (isinstance(col, str) and not col.startswith('Unnamed')) else col)
        newCols = {1: 'Schlüssel',
                   2: 'Straftat',
                   3: 'Anzahl erfasste Fälle',
                   4:'Jan.',
                   5:'Febr.',
                   6:'März',
                   7: 'April',
                   8: 'Mai',
                   9: 'Juni',
                   10: 'Juli',
                   11: 'Aug.',
                   12: 'Sept.',
                   13: 'Okt.',
                   14: 'Nov.',
                   15: 'Dez.',
                   16: 'Tatzeit unbekannt',
                   'Unnamed: 2': 'Schlüssel gültig von',
                   17: 'Schlüssel gültig von',
                   'Unnamed: 3': 'Schlüssel gültig bis',
                   18: 'Schlüssel gültig bis',
                   'Unnamed: 18': 'Sort'}
        df = df.rename(columns=newCols)
        df.reset_index(drop=True, inplace=True)

        return df

def load_BU01_2016_2022(fpath):
    df = pd.read_excel(fpath,skiprows=3,thousands=',',decimal='.')
    df = df.rename(columns={
            'erfasste Fälle':'Anzahl erfasste Fälle',
            'erfasste Fälle davon:\nVersuche':'erfasste Fälle: Anzahl Versuche',
            'von Spalte 3\nVersuche':'erfasste Fälle: Anzahl Versuche',
            'Unnamed: 5':'erfasste Fälle: Versuche in %',
            'Tatortverteilung':'Tatortverteilung: bis unter 20.000 Einwohner',
            'Unnamed: 7':'Tatortverteilung: 20.000 bis unter 100.000',
            'Unnamed: 8':'Tatortverteilung: 100.000 bis unter 500.000',
            'Unnamed: 9':'Tatortveteilung: 500.000 und mehr',
            'Unnamed: 10':'Tatortverteilung: unbekannt',
            'mit Schusswaffe':'mit Schusswaffe: gedroht',
            'Unnamed: 12':'mit Schusswaffe: geschossen',
            'Aufklärung':'Aufklärung: Anzahl Fälle',
            'Unnamed: 14':'Aufklärung: in % (AQ)',
            'Tatverdächtige':'Tatverdächtige: insgesamt',
            'Unnamed: 16':'Tatverdächtige: männlich',
            'Unnamed: 17':'Tatverdächtige: weiblich',
            'Nichtdeutsche Tatverdächtige':'Nichtdeutsche Tatverdächtige: Anzahl',
            'Unnamed: 19':'Nichtdeutsche Tatverdächtige: Anteil an TV insg. in %'})
    return df.drop(range(4)).reset_index(drop=True)

def load_BU01_2012_2015(fpath):
    df = pd.read_excel(fpath,skiprows=3,thousands=',',decimal='.')
    df = df.rename(columns={
                'Schl.':'Schlüssel', # only applies to 2015
                'Schl.-':'Schlüssel',
                'Unnamed: 1':'Straftat',
                'erfasste Fälle':'Anzahl erfasste Fälle', # 2015
                'Unnamed: 2':'Anzahl erfasste Fälle',
                'Unnamed: 3':'%-Anteil an allen Fällen',
                'Unnamed: 4':'erfasste Fälle: Anzahl Versuche',
                'Unnamed: 5':'erfasste Fälle: Versuche in %',
                'Tatortverteilung':'Tatortverteilung: bis unter 20.000 Einwohner',
                'Unnamed: 7':'Tatortverteilung: 20.000 bis unter 100.000',
                'Unnamed: 8':'Tatortverteilung: 100.000 bis unter 500.000',
                'Unnamed: 9':'Tatortveteilung: 500.000 und mehr',
                'Unnamed: 10':'Tatortverteilung: unbekannt',
                'mit Schusswaffe':'mit Schusswaffe: gedroht',
                'Unnamed: 12':'mit Schusswaffe: geschossen',
                'Aufklärung':'Aufklärung: Anzahl Fälle',
                'Unnamed: 14':'Aufklärung: in % (AQ)',
                'Gesamtzahl':'Tatverdächtige: insgesamt',
                'von Spalte 16':'Tatverdächtige: männlich',
                'Unnamed: 17':'Tatverdächtige: weiblich',
                'Unnamed: 18':'Nichtdeutsche Tatverdächtige: Anzahl',
                'Unnamed: 19':'Nichtdeutsche Tatverdächtige: Anteil an TV insg. in %'})
    return df.drop(range(4)).reset_index(drop=True)

class T01DataLoader(Dataset):
    def __init__(self,root_dir:str='Datasets/PKS/'):
        '''Loads and formats the base crime tables of germany for all available years in the root directory

        Params:
        root_dir: The root directory containing the yearly directories of tables (default: 'Datasets/PKS/')

        Returns: Iterable dataset indexed by years
        '''
        self.root_dir = root_dir

    def __len__(self):
        return len(os.listdir(self.root_dir)) # assume this table exists for each year
    
    def __getitem__(self,year:int):
        if 2012 > year or year > 2022:
                raise IndexError(f'No data for requested year: {year}.\nNote: There is no official data before 2012 for this table')
        ypath = os.path.join(self.root_dir,str(year))
        for file in os.listdir(ypath):
            fpath = os.path.join(ypath,file)
            # load different types of tables
            if any(desi in file for desi in ['BU-T01','BU-F-01','STD-F-01']):#
                return load_BU01_2016_2022(fpath)
            elif 'tb01_FaelleGrundtabelle_excel' in file:
                return load_BU01_2012_2015(fpath)
            

### LKS Dataset ###

def load_LKS01_2019_2022(fpath:str):
    df = pd.read_excel(fpath,skiprows=3,thousands='.',decimal=',')
    df = df.rename(columns={
        'erfasste Fälle':'Anzahl erfasste Fälle', # 2019
        'erfasste Fälle davon:\nVersuche':'erfasste Fälle: Anzahl Versuche',
        'von Spalte 3\nVersuche':'erfasste Fälle: Anzahl Versuche', # 2019
        'Unnamed: 6':'erfasste Fälle: Versuche in %',
        'Tatortverteilung':'Tatortverteilung: bis unter 20.000 Einwohner',
        'Unnamed: 8':'Tatortverteilung: 20.000 bis unter 100.000',
        'Unnamed: 9':'Tatortverteilung: 100.000 bis unter 500.000',
        'Unnamed: 10': 'Tatortverteilung: 500.000 und mehr',
        'Unnamed: 11':'Tatortverteilung: unbekannt',
        'mit Schusswaffe':'mit Schusswaffe: gedroht',
        'Unnamed: 13':'mit Schusswaffe: geschossen',
        'Aufklärung':'Aufklärung: Anzahl Fälle',
        'Unnamed: 15':'Aufklärung: in % (AQ)',
        'Tatverdächtige':'Tatverdächtige: insgesamt',
        'Unnamed: 17':'Tatverdächtige: männlich',
        'von Spalte 16':'Tatverdächtige: männlich',
        'Unnamed: 18':'Tatverdächtige: weiblich',
        'Nichtdeutsche Tatverdächtige':'Nichtdeutsche Tatverdächtige: Anzahl',
        'Unnamed: 19':'Nichtdeutsche Tatverdächtige: Anzahl', # 2019
        'Unnamed: 20':'Nichtdeutsche Tatverdächtige: Anteil an TV insg. in %'
    })
    return df.drop(range(4)).reset_index(drop=True)

def load_LKS01_2015_2018(fpath):
    # confirmed for 2018,2017,2016,2015
    df = pd.read_excel(fpath,skiprows=4,thousands='.',decimal=',')
    df = df.drop(['BL-Schl.','Sort'], axis=1, errors='ignore')
    df = df.rename(columns={
        'erfasste Fälle':'Anzahl erfasste Fälle',
        'von Spalte 4 Versuche':'erfasste Fälle: Anzahl Versuche',
        'Unnamed: 6':'erfasste Fälle: Versuche in %',
        'Unnamed: 7':'erfasste Fälle: Versuche in %', # 2018
        'Aufklärung':'Aufklärung: Anzahl Fälle',
        'Unnamed: 8':'Aufklärung: in % (AQ)', # really the same?
        'Unnamed: 9':'Aufklärung: in % (AQ)', # really the same?
        'Tatver-dächtige insg.':'Tatverdächtige: insgesamt',
        'Nichtdeutsche Tat-verdächtige':'Nichtdeutsche Tatverdächtige: Anzahl',
        'Unnamed: 11':'Nichtdeutsche Tatverdächtige: Anteil an TV insg. in %',
        'Unnamed: 12':'Nichtdeutsche Tatverdächtige: Anteil an TV insg. in %' # 2018
    })
    return df.drop(range(2)).reset_index(drop=True)

def load_LKS01_2014(fpath:str='Datasets/PKS/2014/tb01_FaelleGrundtabelleLaender_excel.xlsx'):
    df = pd.read_excel(fpath,skiprows=7,thousands='.',decimal=',')
    df = df.rename(columns={
        'Strft. Schl.':'Schlüssel',
        'erfasste Fälle 2014':'Anzahl erfasste Fälle',
        'Versuche absolut':'erfasste Fälle: Anzahl Versuche',
        'Versuche in %':'erfasste Fälle: Versuche in %',
        'aufgeklärte Fälle':'Aufklärung: Anzahl Fälle',
        'AQ \nin %':'Aufklärung: in % (AQ)',
        'TV insges.':'Tatverdächtige: insgesamt',
        'NDTV insges.':'Nichtdeutsche Tatverdächtige: Anzahl',
        'NDTV in %':'Nichtdeutsche Tatverdächtige: Anteil an TV insg. in %'
    })
    return df

def load_LKS01_2013(fpath:str='Datasets/PKS/2013/tb01_FaelleGrundtabelleLaender_excel.xls'):
    df = pd.read_excel(fpath,skiprows=8,thousands='.',decimal=',')
    df = df.rename(columns={
        'Strft. Schl.':'Schlüssel',
        'erfasste Fälle 2013':'Anzahl erfasste Fälle',
        'Versuche absolut':'erfasste Fälle: Anzahl Versuche',
        'Versuche in %':'erfasste Fälle: Versuche in %',
        'aufgeklärte Fälle':'Aufklärung: Anzahl Fälle',
        'AQ \nin %':'Aufklärung: in % (AQ)',
        'TV insges.':'Tatverdächtige: insgesamt',
        'NDTV insges.':'Nichtdeutsche Tatverdächtige: Anzahl',
        'NDTV in %':'Nichtdeutsche Tatverdächtige: Anteil an TV insg. in %'
    })
    return df

class LKS01(Dataset):
    def __init__(self,root_dir:str='Datasets/PKS/'):
        '''Loads and formats the base crime tables grouped by federal states for all available years in the root directory

        Params:
        root_dir: The root directory containing the yearly directories of tables (default: 'Datasets/PKS/')

        Returns: Iterable dataset indexed by years
        '''
        self.root_dir = root_dir

    def __len__(self):
        return min(len(os.listdir(self.root_dir)),10) # this table is missing in 2012, but the directory exists for other tables
    
    def __getitem__(self,year):
        if 2013 > year or year > 2022:
                raise IndexError(f'No data for requested year: {year}.\nNote: There is no official data before 2013 for this table')
        ypath = os.path.join(self.root_dir,str(year))
        for file in os.listdir(ypath):
            fpath = os.path.join(ypath,file)
            # load table for all years
            if any(desi in file for desi in ['LA','Laender']):
                if 2019 <= year <= 2022:
                    return load_LKS01_2019_2022(fpath)
                if 2015 <= year <= 2018:
                    return load_LKS01_2015_2018(fpath)
                if year == 2014:
                    return load_LKS01_2014(fpath)
                if year == 2013:
                    return load_LKS01_2013(fpath)

if __name__ == '__main__':
    # Possible Tests 
    #TODO: Create test framework???
    DL = T08DataLoader()
    df  = DL[2022]
    print(df.head())
    cols_2022 = df.columns.values
    cols_2022.sort()
    # print(cols_2022)
    for year in range(2012, 2023):
        df_year = DL[year]
        cols = df_year.columns.values
        cols.sort()
        if year != 2013 and year != 2018:
            print(f"{year}: {all(cols_2022 == cols)}")
        elif year == 2013:
            print(f"{year}: {all(cols_2022[0:-1] == cols)}")
        elif year == 2018:
            print(f"{year}: {all(cols_2022 == np.delete(cols, np.argwhere(cols == 'Sort')))}")

    DL = T20DataLoader()
    df  = DL[2022]
    cols_2022 = df.columns.values
    for y in range(2012, 2023):
        print(f"{y}: {all(cols_2022 == DL[y].columns.values)}")
        