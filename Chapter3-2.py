# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 16:00:23 2021

@author: margaret
"""


import requests
import pprint

def make_request(endpoint, payload=None):
    """
    Make a request to a specific endpoint on the weather API
    passing headers and optional payload.
    
    Parameters:
        - endpoint: The endpoint of the API you want to 
                    make a GET request to.
        - payload: A dictionary of data to pass along 
                   with the request.
    
    Returns:
        Response object.
    """
    return requests.get(
        f'https://www.ncdc.noaa.gov/cdo-web/api/v2/{endpoint}',
        headers={
            'token': 'zBdVrWZCCyBkAknisQxCVbvWBrrLBXEb'
        },
        params=payload
    )

def get_item(name, what, endpoint, start=1, end=None):
    """
    Grab the JSON payload for a given field by name using binary search.

    Parameters:
        - name: The item to look for.
        - what: Dictionary specifying what the item in `name` is.
        - endpoint: Where to look for the item.
        - start: The position to start at. We don't need to touch this, but the
                 function will manipulate this with recursion.
        - end: The last position of the cities. Used to find the midpoint, but
               like `start` this is not something we need to worry about.

    Returns:
        Dictionary of the information for the item if found otherwise 
        an empty dictionary.
    """
    # find the midpoint which we use to cut the data in half each time
    mid = (start + (end if end else 1)) // 2
    
    # lowercase the name so this is not case-sensitive
    name = name.lower()
    
    # define the payload we will send with each request
    payload = {
        'datasetid' : 'GHCND',
        'sortfield' : 'name',
        'offset' : mid, # we will change the offset each time
        'limit' : 1 # we only want one value back
    }
    
    # make our request adding any additional filter parameters from `what`
    response = make_request(endpoint, {**payload, **what})
    
    if response.ok:
        # if response is ok, grab the end index from the response metadata the first time through
        end = end if end else response.json()['metadata']['resultset']['count']
        
        # grab the lowercase version of the current name
        current_name = response.json()['results'][0]['name'].lower()
        
        # if what we are searching for is in the current name, we have found our item
        if name in current_name:
            return response.json()['results'][0] # return the found item
        else:
            if start >= end: 
                # if our start index is greater than or equal to our end, we couldn't find it
                return {}
            elif name < current_name:
                # our name comes before the current name in the alphabet, so we search further to the left
                return get_item(name, what, endpoint, start, mid - 1)
            elif name > current_name:
                # our name comes after the current name in the alphabet, so we search further to the right
                return get_item(name, what, endpoint, mid + 1, end)    
    else:
        # response wasn't ok, use code to determine why
        print(f'Response not OK, status: {response.status_code}')

def get_location(name):
    """
    Grab the JSON payload for the location by name using binary search.

    Parameters:
        - name: The city to look for.

    Returns:
        Dictionary of the information for the city if found otherwise 
        an empty dictionary.
    """
    return get_item(name, {'locationcategoryid' : 'CITY'}, 'locations')

nyc = get_location('New York')

nyc2 = get_item('New York', {'locationcategoryid' : 'CITY'}, 'locations')

central_park = get_item('NY City Central Park', {'locationid' : nyc2['id']}, 'stations')

central_park

response = make_request(
    'data', 
    {
        'datasetid' : 'GHCND',
        'stationid' : central_park['id'],
        'locationid' : nyc['id'],
        'startdate' : '2018-10-01',
        'enddate' : '2018-10-31',
        'datatypeid' : ['TMIN', 'TMAX', 'TOBS'], # temperature at time of observation, min, and max
        'units' : 'metric',
        'limit' : 1000
    }
)
response.status_code

df = pd.DataFrame(response.json()['results'])


"""----------below script is nor working------------"""
"""just fixed it, I code the wrong start date"""

response = make_request(
    'data',
    {'datasetid' : 'GHCND',
     'stationid' : central_park['id'],
     'locationid' : nyc['id'],
     'startdate' : '2018-10-01',
     'enddate' : '2018-10-31',
     'datatypeid' : ['TAVG', 'TMAX', 'TMIN'],
     'units' : 'metric',
     'limit' : 1000})

response.status_code

import pandas as pd

df = pd.DataFrame(response.json()['results'])

df.head()

df.datatype.unique()

if get_item(
        'NY City Central Park',
        {'locationid':nyc['id'], 'datatypeid' : 'TAVG'},
        'stations'):
    print('Found!')
