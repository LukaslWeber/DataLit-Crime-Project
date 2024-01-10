import os
from torch.utils.data import Dataset
import pandas as pd

class TvDataLoader(Dataset):
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
            raise Exception("No file with 'BU-T20-Tatverdaechtige.' in the folder found")

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




if __name__ == '__main__':
    # Possible Tests 
    #TODO: Create test framework???
    DL = TvDataLoader()
    df  = DL[2022]
    cols_2022 = df.columns.values
    for y in range(2012, 2023):
        print(f"{y}: {all(cols_2022 == DL[y].columns.values)}")
    
    print(cols_2022)