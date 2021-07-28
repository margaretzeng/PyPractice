import numpy as np
import pandas as pd

weather = pd.read_csv('data/nyc_weather_2018.csv', parse_dates=['date'])
fb = pd.read_csv('data/fb_2018.csv', index_col='date', parse_dates=True)

fb.assign(
    abs_z_score_volume = lambda x:x.volume\
    .sub(x.volume.mean()).div(x.volume.std()).abs()
).query('abs_z_score_volume>3')

fb.assign(
    volume_pct_change=fb.volume.pct_change(),
    pct_change_rank=lambda x:\
    x.volume_pct_change.abs().rank(ascending=False)
).nsmallest(5,'pct_change_rank')

#use slicing to look at the change around the announcement
fb['2018-01-11':'2018-01-12']

(fb>215)

(fb>215).any()

volume_binded = pd.cut(
    fb.volume, bins = 3, labels = ['low', 'med', 'high']
)

volume_binded.value_counts()

fb[volume_binded=='high'].sort_values('volume', ascending = False)

fb['2018-07-25':'2018-07-26']

central_park_weather = weather.query(
    'station == "GHCND:USW00094728"'
).pivot(index = 'date', columns = 'datatype', values = 'value')

oct_weather_z_scroes = central_park_weather\
    .loc['2018-10', ['TMIN','TMAX','PRCP']]\
    .apply(lambda x:x.sub(x.mean()).div(x.std()))

oct_weather_z_scroes.describe()

oct_weather_z_scroes.query('PRCP>3').PRCP
oct_weather_z_scroes.query('PRCP>3')

central_park_weather.loc['2018-10', 'PRCP'].describe()

central_park_weather.loc['2018-10'].assign(
    rolling_PRCP=lambda x:x.PRCP.rolling('3D').sum()
)[['PRCP','rolling_PRCP']].head(7).T

central_park_weather.assign(
    AVG = lambda x:x.TMAX.rolling('30D').mean(),
    EWMA = lambda x:x.TMAX.ewm(span=30).mean()
).loc['2018-09-29':'2018-10-08',['TMAX','EWMA','AVG']]


from window_calc import window_calc

window_calc(
    central_park_weather.loc['2018-10'],
    pd.DataFrame.rolling,
    {'TMAX':'max', 'TMIN':'min',
     'AWND':'mean','PRCP':'sum'},
    '3D'
).head() # the window_calc is from the book, not a built-in package.....