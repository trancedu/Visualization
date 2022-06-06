''' 
    This script provides an example of how to consolidate multiple csv files into w DataFrame panel
    This is a pretty dynamic script for reading in data files, metadata, and looking up the corresponding year.
    
    data downloaded from https://data.census.gov/cedsci/table?q=Population%20Total&tid=PEPPOP2019.PEPANNRES
'''

import pandas as pd
import glob
import re

def get_year_type(check_path):
    ''' 
        This uses REGEX to figure out what year is the corresponding file being read. It also returns a flag for the metadata
    
        Regex allows searhing for patterns rather than exact occurences. In this case we want a pattern of 4 digits (years). 
        Regex allows the user to precompile a search pattern, which can improve the speed when searching patterns. 
        There are two ways to find for a pattern inside a string. 
            re.search()  -> returns only the first occurance of the pattern
            re.findall() -> returns all occurances of the pattern
        
        Ex. 
            re.compile('[0-9]{4}') used along with findall will give you both the year and the date of the data. This regex could
            be changed to re.compile('[0-9]{4}\.') to ensure the result is always the year of the population estimate
        
    '''
    pattern = re.compile('[0-9]{4}')
    year = re.search(pattern, check_path)                  # note that the pattern does not need to be compiled
    
    # This reduces the match object to the actual element only when the match is found, just to avoid the error
    if year:
        year = year[0]
    
    meta = re.search('metadata', check_path)
    if meta:
        meta = 'meta'
    else:
        meta = 'data'
    
    return(year, meta)

def fix_meta(df):
    df.columns = ['id', 'name']
    
    # expand the names into their own columns
    df = df[['id']].merge(df['name'].str.split('!!').apply(pd.Series), left_index = True, right_index = True)
    df.columns = ['id'] + ['level_{}'.format(x) for x in range(len(df.columns) - 1)]
    
    # keep only what I care about
    df = df.loc[df['level_0'].str.lower() == 'estimate']
    
    # set the corresponding index and drop id
    df.index = df['id']
    df = df.drop(columns = ['id'])
    
    return(df.reset_index())

def fix_data(df, year):
    # slice it based on the last observation
    df = df.iloc[-1]
    
    # create a multi-index level including the year. We need to create a list of tupples. 
    
    # option 1
    tuples = [(year, ind) for ind in df.index]
    
    # option 2
    tuples = list(zip(*[[year]*len(df), df.index]))
    index = pd.MultiIndex.from_tuples(tuples, names=["year", "name"])
    
    # assign the new index
    df.index = index
    
    # and just for clarity, let's name this
    df.name = 'data'
    
    return(df)

def fix_file(meta, *args):
    '''
    This is SWITCH function. The purpose is to avoid repetition in the code and to be able to assign the specific call to the 
    data type being read in. 
    
    Parameters
    ----------
    meta : STR
    *args : these are the arguments passed to the function as list

    '''
    if meta == 'meta':
        return(fix_meta(*args))
    else:
        return(fix_data(*args))
    

path = 'G:\My Drive\Visualization Class\Class 4\population_growth\*.csv'

# I want to create a dictionary that keeps the years as keys and the meta/data as elements
years = {}

# This takes care of the file reading; filtering only csv files
for file_path in glob.glob(path):
    # first, get the file type and the year
    year, meta = get_year_type(file_path)
    
    # This if is used to know if this is a first time allocation of the dict index, or if the index exists.
    if year in years.keys():
        # the key was allocated
        years[year][meta] = fix_file(meta, pd.read_csv(file_path))
    else:
        # the structure needs to be created
        years[year] = {meta: fix_file(meta, pd.read_csv(file_path), year)}

'''
    I want to make it so that the output of this script are 2 files: a data file and a meta file so that they can be used later
    I want to then consolidate all the metas and all the data files
'''

meta = pd.DataFrame()
data = pd.Series(index = pd.MultiIndex.from_tuples((), names=["year", "name"]), name = 'data')

for k, v in years.items():
    meta = meta.append(v['meta'])
    data = data.append(v['data'])

# final touches before exporting
meta = meta.drop_duplicates()
meta.index = meta.pop('id')
data = data.loc[:, meta.index]

meta.to_csv('G:\My Drive\Visualization Class\Class 4\data\metadata.csv')
data.to_csv('G:\My Drive\Visualization Class\Class 4\data\data.csv')

