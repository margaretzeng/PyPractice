# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 02:08:04 2021

@author: margaret
"""


import pandas as pd

long_df = pd.read_csv(
    './data/long_Data.csv',
    usecols = ['date', 'datatype', 'value']
    ).rename(columns = {'value': 'temp_C'}).assign(
        date = lambda x:pd.to_datetime(x.date),
        temp_F = lambda x: (x.temp_C * 9/5) +32)

long_df.set_index('date').head(6).T


long_df

pivoted_df = long_df.pivot(index='date', columns='datatype', values='temp_C')

pivoted_df.head()

pivoted_df.describe()

pivoted_df = long_df.pivot(
    index = 'date', columns = 'datatype',
    values= ['temp_C', 'temp_F']
)

pivoted_df.describe()

pivoted_df['temp_F']['TMIN'].head()

multi_index_df = long_df.set_index(['date', 'datatype'])

multi_index_df.head().index

multi_index_df.head()

unstacked_df = multi_index_df.unstack()

unstacked_df.head()

wide_df = pd.read_csv('data/wide_data.csv')

wide_df.head()

melted_df = wide_df.melt(
    id_vars = 'date', value_vars=['TMAX', 'TMIN', 'TOBS'],
    value_name = 'temp_C', var_name = 'measurement'
)

melted_df.head()

wide_df.set_index('date', inplace = True)
stacked_series = wide_df.stack()

stacked_series.head()

stacked_df = stacked_series.to_frame('values')

stacked_df

stacked_df.head().index
stacked_df.head().index.set_names(['date', 'datatype'], inplace=True)

stacked_df.index.names