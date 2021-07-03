# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 22:33:27 2021

@author: margaret
"""


import matplotlib.pyplot as plt
import pandas as pd

wide_df = \
    pd.read_csv('./wide_data.csv', parse_dates= ['date'])
    
long_df = pd.read_csv('./long_data.csv', 
                      usecols = ['date', 'datatype', 'value'],
                      parse_dates = ['date']
                      )[['date', 'datatype', 'value']]

long_df

wide_df.describe(include = 'all', datetime_is_numeric=True)

wide_df.describe(include = 'all', datetime_is_numeric = True) # not wokring?! unexpected keyword -> datetime_is_numeric

wide_df.plot(
    x = 'date', y = ['TMAX', 'TMIN', 'TOBS'], figsize = (15,5),
    title = 'Temperature in NYC in October 2018'
    ).set_ylabel('Temperature in Celsius')

long_df.head(6)

import seaborn as sns

sns.set(rc = {'figure.figsize': (15,5)}, style = 'white')

ax = sns.lineplot(
    data = long_df, x = 'date', y = 'value', hue = 'datatype')

ax.set_ylabel('Temperature in Celsius')
ax.set_title('Temperature in NYC in October 2018')

sns.set(
        rc = {'figure.figsize' : (20,10)},
        style = 'white', font_scale = 2)

g = sns.FacetGrid(long_df, col='datatype', height=10)
g = g.map(plt.plot, 'date', 'value')
g.set_titles(size=25)
g.set_xticklabels(rotation=45)

import requests

def make_request(endpoint, payload=None):
    return requests.get(
        'http://www.ncdc.noaa.gov/cdo-web/'
        f'api/v2/{endpoint}',
        headers = {'token' : 'zBdVrWZCCyBkAknisQxCVbvWBrrLBXEb'},
        params=payload)

response = \
    make_request('datasets', {'startdate' : '2018-10-01'})
    
response.status_code

response.ok

payload = response.json()
payload.keys()

payload['metadata']
