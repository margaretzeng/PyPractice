import numpy as np
import pandas as pd

fb = pd.read_csv(
    'data/fb_2018.csv', index_col='date',parse_dates=True
).assign(trading_volume = lambda x:pd.cut(
    x.volume,bins = 3, labels = ['low','med','high']
))

weather = pd.read_csv(
    'data/weather_by_station.csv',
    index_col='date', parse_dates=True
)

pd.set_option('display.float_format', lambda x:'%.2f' % x)

fb.agg(
    {'open': np.mean,
     'high' : np.max}
)

fb.groupby('trading_volume').agg(['min','max','mean'])

fb_agg = fb.groupby('trading_volume').agg({
    'open':'mean','high':['min','max'],
    'low':['min','max'],'close':'mean'
})

fb_agg.loc['med','low']['min']

fb_agg.columns

weather.query('datatype == "PRCP"').groupby(
    ['station_name', pd.Grouper(freq='Q')]
).sum()