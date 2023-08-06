''' Data Preparation Functions'''

from pathlib import Path
from google.colab import auth
import gspread
from google.auth import default
import pandas as pd
import numpy as np

figure_dir_iuk_smart_2023 = Path.cwd().joinpath(
    'drive','Shareddrives','Data Store','IUK Smart Grant (19921484) Figures')

def link_google_docs():
    '''
    Link to Google Docs which allows read/write access
    '''
    auth.authenticate_user()
    creds, _ = default()
    gc_docs = gspread.authorize(creds)
    return gc_docs

def open_worksheet(gc_docs, worksheet_name,worksheet_index):
    '''
    Open a Google Sheets Worksheet
    '''
    worksheet = gc_docs.open(worksheet_name).get_worksheet(worksheet_index)
    rows = worksheet.get_all_values() # get_all_values gives a list of rows.
    database = pd.DataFrame.from_records(rows) # convert to dataframe
    database.columns = database.iloc[0]
    database = database[1:]
    return database

def estimate_foam_density(diameter, a_value = -4.67112455e+03, b_value =-4.93900082e-01):
    '''
    Estimate the density of the foam from an exponential relation.
    '''
    print(f'Using exponential fitting values: a = {a_value} and b = {b_value}')
    return -a_value*np.exp(diameter*b_value)

def convert_series_to_float(database,columns):
    '''
    Converts series to float in dataframe
    '''
    for item in columns:
        database[item] = database[item].astype(float)
    return database

def remove_null_values_from_df(database,series):
    '''
    Removes rows from dataframe with null values in chosen series
    '''
    return database[pd.to_numeric(database[series], errors='coerce').notnull()]
