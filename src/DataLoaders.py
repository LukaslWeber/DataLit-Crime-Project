import os
from torch.utils.data import Dataset
import pandas as pd
import numpy as np

class T20DataLoader(Dataset):
    def __init__(self,root_dir:str='Datasets/PKS/'):
        self.root_dir = root_dir

    def __len__(self):
        return len(os.listdir(self.root_dir))
    
    def __getitem__(self,year:int):
        y_path = os.path.join(self.root_dir,str(year))
        
        # Check whether there is data for the year
        if(os.path.isdir(y_path) != True):
           raise Exception(f"There is no dataset folder for the year: {year}") 
        
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
        self.root_dir = root_dir

    def __len__(self):
        return len(os.listdir(self.root_dir))
    
    def __getitem__(self, year):
        y_path = os.path.join(self.root_dir,str(year))
        
        # Check whether there is data for the year
        if(os.path.isdir(y_path) != True):
           raise Exception(f"There is no dataset folder for the year: {year}") 
        
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
        