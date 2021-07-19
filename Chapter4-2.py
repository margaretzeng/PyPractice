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