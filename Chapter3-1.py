# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 22:33:27 2021

# the last part in the script is not working, error: 'metadata'
# just skip this for now.


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

payload['metadata']['resultset']['count']

payload['results'][0].keys()

payload['results'][0]

[(data['id'], data['name'])for data in payload['results']] 

response = make_request(
    'locationcategories', payload = {'datasetid' : 'GHCND'})

response.status_code

response.json()['results']

import pprint

pprint.pprint(response.json())

def get_item(name, what, endpoint, start = 1, end = None):
    """
    Grab the JSON payload using binary search
    """
    
    # find the midpoint to cut the data in half each time
    mid = (start + (end or 1)) // 2
    
    # lowercase the name so this not ae-sentitive
    name = name.lower()
    
    # define the payload we will send with each request
    payload = {
        'datasetid' : 'GHCND', 'sortfield' : 'name',
        'offset' : mid, # we'll change the offset each time
        'limit' : 1 # we only want one value back
        }
    # make request adding addtional filters from 'what'
    response = make_request(endpoint, {**payload, **what})
    
    if response.ok:
        payload = response.json()
        
        # if ok, grab the ind index from the response
        # metadata the first time through
        end = end if end else payload['metadata']['resultset']['count']
            
        #grab the lowcase version ofo the current name
        current_name = \
            payload['results'][0]['name'].lower()
        
        # if what we are searching for is in the current name, we have found out item
        if name in current_name:
            #return the found item
            return payload['results'][0]
        else:
            if start >= end:
                # if start index is greater than or equal to end index, we couldnt find it
                return {}
            elif name < current_name:
                # name comes before the current name in the alphabet > search further to the left
                return get_item(name, what, endpoint, start, mid -1)
            
            elif name > current_name:
            # name comes after the current name in the alphabet > search further to the right
                return get_item(name, what, endpoint, mid +1, end)
        
    else:
        # response wasnt ok, use code to determine why
        print('Response not OK, '
              f'status:{response.status_code}')
        
    """
    Parameters
    ----------
    name : TYPE
        DESCRIPTION.
    what : TYPE
        DESCRIPTION.
    endpoint : TYPE
        DESCRIPTION.
    start : TYPE, optional
        DESCRIPTION. The default is 1.
    end : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    """


nyc = get_item('New York', {'locationcategoryid' : 'CITY'}, 'locations')

nyc

central_park = get_item(
    'NY City Central Park',
    {'locationid' : nyc['id']}, 'stations') # somehow it's not working!!!!

central_park1 = get_item('NY City Central Park', {'locationid' : nyc['id']}, 'stations')

response = make_request('data',
                        {'datasetid' : 'GHCND',
                         'stationid' : 'c'})
