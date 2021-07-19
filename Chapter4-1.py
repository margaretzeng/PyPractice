import pandas as pd

weather = pd.read_csv('data/nyc_weather_2018.csv')

weather.head()

snow_Data = weather.query(
    'datatype == "SNOW" and value >0'
    'and station.str.contains("US1NY")'
)

station_info = pd.read_csv('data/weather_stations.csv')

station_info.head()

station_info.describe()
weather.station.describe()

station_info.shape[0], weather.shape[0]

def get_row_count(*dfs):
    return  [df.shape[0] for df in dfs]

get_row_count(station_info, weather)

inner_join = weather.merge(
    station_info, left_on = 'station', right_on='id'
)


# Sunday July 18, 2021

dirty_data = pd.read_csv(
    'data/dirty_data.csv', index_col= 'date'
).drop_duplicates().drop(columns='SNWD')

dirty_data.head()

valid_station = dirty_data.query('station != "?"')\
    .drop(columns = ['WESF', 'station'])

station_with_wesf = dirty_data.query('station == "?"')\
    .drop(columns = ['station', 'TOBS', 'TMIN', 'TMAX'])

valid_station.merge(
    station_with_wesf, how = 'left',
    left_index = True, right_index = True
).query('WESF > 0' ).head()


valid_station.merge(
    station_with_wesf, how = 'left',
    left_index = True, right_index = True,
    suffixes = ('', '_?')
).query('WESF > 0' ).head()

weather.set_index('station', inplace= True)
station_info.set_index('id', inplace=True)

weather.index.intersection(station_info.index)

station_info.index.difference(weather.index)