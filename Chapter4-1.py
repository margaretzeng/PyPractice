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

