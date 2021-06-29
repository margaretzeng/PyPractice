import numpy as np

data = np.genfromtxt(
    './data/example_data.csv', delimiter=';',
    names=True, dtype=None, encoding='UTF'
)

# Now having the data in a Numpy array
data

# Get the dimensions of the array
data.shape

# Get the data types the array contains.
data.dtype

%%timeit #没用出来，不会用QAQ

max([row[3] for row in data]) #Selecting the third index of each row and get the max one. this is called a list comprehension.

row[3] for row in data

array_dict = {
    col: np.array([row[i] for row in data])
    for i , col in enumerate(data.dtype.names)}

array_dict

# the function of enumerate()
my_list = ["apples", "pears", "oranges", "fruits"]

for x, element in enumerate(my_list):
    print(x, element)

for x in range(len(my_list)):
    print(x, my_list[x])
    
%timeit
array_dict['mag'].max()

np.array([
    value[array_dict['mag'].argmax()]
    for key, value in array_dict.items()])

import pandas as pd

place = pd.Series(array_dict['place'], name = 'place')

place.shape

place.index

place.array

place_index = place.index

place_index.values

place.values #it's valueS, not value.

place_index.is_unique

numbers = np.linspace(0, 10, num = 5)

x = pd.Series(numbers)
y = pd.Series(numbers, index = pd.Index([1,2,3,4,5])) # .index is not correct, it's .Index
x + y

df = pd.DataFrame(array_dict)
df.dtypes #.dtypeS dont forget the s

df.values

df.columns #they are stored in an Index object as well. TIL.

# the dtypes attribute if for dataframe, the dtype attribute (no s) is for array, series, index object.

df + df

help()

'---------------------

import datetime as dt
import numpy as np
import pandas as pd

testing = np.arange(5)
testing

np.random.seed(0) # set a seed for reproducibility
pd.Series(np.random.rand(5), name = 'random')

np.random.seed(0)
pd.DataFrame(
    {
     'random' : np.random.rand(5),
     'text' : ['hot', 'warm', 'cool', 'cold', None],
     'truth' : [np.random.choice([True, False])
                                 for _ in range(5)]
     },
    index=pd.date_range(
        end=dt.date(2019, 4, 21),
        freq='1D', periods = 5, name ='date'
        )
    )

pd.DataFrame([
    {'mag' : 5.2, 'place' : 'California'},
    {'mag' : 1.2, 'place' : 'Alaska'},
    {'mag' : 0.2, 'place' : 'California'},
    ])

list_of_tuples = [(n, n**2, n**3) for n in range(5)]
list_of_tuples

pd.DataFrame(
    list_of_tuples,
    columns = ['n', 'n_squared', 'n_cubed'])

#using pd.DataFrame() with Numpy arrays:
pd.DataFrame(
    np.array([
        [0,0,0],
        [1,1,1],
        [2,4,8],
        [3,9,27],
        [4,16,64]
        ]), columns = ['n', 'n_squared', 'n_cubed']
    )

!wc -l data/earthquakes.csv # not working here.

df = pd.read_csv('./data/earthquakes.csv')

df = pd.read_csv(
    'https://github.com/stefmolin/Hands-On-Data-Analysis-with-Pandas/blob/master/ch_02/data/earthquakes.csv?raw=True')

df

import sqlite3

with sqlite3.connect('data/quakes.db') as connection:
    pd.read_csv('data/tsunamis.csv').to_sql(
        'tsunamis', connection, index=False,
        if_exists='replace'
        )
    
with sqlite3.connect('data/quakes.db') as connection:
    tsunamis = \
        pd.read_sql('select * FROM tsunamis', connection)
        
tsunamis.head()

----------------------------
#Getting data based from an API

import datetime as dt
import pandas as pd
import requests

yesterday = dt.date.today() - dt.timedelta(days = 1)

api = 'https://earthquake.usgs.gov/fdsnws/event/1/query'

payload = {
    'format' : 'geojson',
    'starttime' : yesterday - dt.timedelta(days = 30),
    'endtime' : yesterday
    }

response = requests.get(api, params = payload)

#checking the request was successful, 200 means everything is ok.
response.status_code

earthquake_json = response.json()
earthquake_json.keys()

earthquake_json['metadata']

type(earthquake_json['features'])

earthquake_json['features']

earthquake_json['features'][0]


earthquake_properties_data = [
    nothing['properties']
    for nothing in earthquake_json['features']
    ]

earthquake_properties_data[0]

df = pd.DataFrame(earthquake_properties_data)

--------------------
#Inspecing a DataFrame object

import pandas as pd
import numpy as np

df = pd.read_csv('data/earthquakes.csv')

df.empty #check if the dataframe is empty

df.shape #check the number of observations(rows) and variables(columns)

df.columns # see the name of the columns

df.head() #check the top rows, and you could put number in it.

df.head(10)

df.tail() #check the bottom rows of the dataset

df.dtypes # check the data types of the columns

df.info() # check the non-null entreis of each columns

df.describe() # checking the statistical summary, also work for Series objects.

df.describe(percentiles = [0.05, 0.95]) # if you want only the 5th and 95th percentiles

df.describe(include=np.object) #pick those non-numeric data and get their occurance, # of unique, mode etc.

df.columns

df.alert.unique()

df["alert"].unique()

df.alert.value_counts()

df[
   ['title', 'time']
   + [col for col in df.columns if col.startswith('mag')]
   ]

#use a list comprehension to go through each of the columns in the df and only keep those starated with mag:

[col for col in df.columns if col.startswith('mag')]

col for col in df.columns if col.startswith('mag') # need to put this in a bracket as a list, otherwise won't work.

df[['title', 'time']][100:103]


df.loc[110:112, 'title'] = \
    df.loc[110:112, 'title'].str.lower()


df.loc[:, 'title']

#loc[] is inclusive, iloc[] is not inclusive.
# when using loc[], the end index is inclusive. but when iloc[], the end index is exclusive.
df.iloc[10:15, [19,8]]
df.loc[10:15, ['title' , 'mag']]

# looking up for scalar values, use at[], or iat[]
df.at[10, 'mag']

# Filtering

df.mag > 2

df[df.mag >2]

df.loc[
       df.mag >= 7.0,
       ['alert', 'mag', 'magType', 'title']]

# loc[] can handle Boolean masks as well:
df.loc[
       df.mag >= 7.0,
       ['alert', 'mag',]]


df.columns

df.loc[
       (df.place.str.contains('Alaska'))
       & (df.alert.notnull()),
       ['alert','mag']]

df.loc[
       (df.place.str.contains('Alas')) # it's contians, so not nessessary gonna be equal.
       & (df.alert.notnull()), # here's a notnull() method to get rows where alert columns was not null.
       ['alert','mag']]

df.loc[
       (df.place.str.contains('CA$' | 'California') # I got this wrong. the correct one is below.
        & df.mag >= 3.8)]

df.loc[
       (df.place.str.contains(r'CA$|California$')) # wrong again
       & df.mag >= 3.8]

df.loc[
       (df.place.str.contains( r'CA|California$')) & (df.mag >= 3.8)]  #why Iｇｅｔ　ａｎ　ｅｍｐｔｙ　ｄａｔａｆｒａｍｅ　ｈｅｒｅ？　ｗｈａｔ＇ｓ　ｔｈｅ　ｄｉｆｆ　ｗｈｅｎ　ｈａｖｉｎｇ　＄　ｗｉｔｈ　ｔｈｅ　２　ｓｔｒｉｎｇ　ｂｅｔｗｅｎ　｜？？


df.loc[
    (df.place.str.contains(r'CA|California$')) & (df.mag > 3.8),
    ['alert', 'mag', 'magType', 'title', 'tsunami', 'type']
]

df.loc[
       (df.mag.between(6.5, 7.5))]

df.loc[
       df.magType.isin(['mw', 'mwb'])]

# getting the index of the rows where max mag and min mag are
[df.mag.idxmin(), df.mag.idxmax()]
# and use these to get the rows
import pandas as pd

df.loc[
       [df.mag.idxmin(), df.mag.idxmax()],
       ['alert', 'mag', 'magType', 'title', 'tsunami', 'type']]

-----------Adding ad removing data

df = pd.read_csv(
    'data/earthquakes.csv',
    usecols = [
        'time', 'title', 'place', 'magType',
        'mag', 'alert', 'tsunami'])

df['source'] = 'USGS API'
df.head()

df['mag_negative'] = df.mag <0
df.head()

df.place.str.extract(r', (.*$)') [0].sort_values().unique()

df.columns

df['parsed_place'] = df.place.str.replace(
    r'.* of ','', regex = True
    ).str.replace(
        'the ', ''
    ).str.replace(
        r'CA$', 'California', regex = True
    ).str.replace(
        r'NV$', 'Nevada', regex = True
    ).str.replace(
        r'MX$', 'Mexico', regex = True
    ).str.replace(
        r' region$', '', regex = True
    ).str.replace(
        'northern ', ''
    ).str.replace(
        'Fiji Islands', 'Fiji'
    ).str.replace(
        r'^.*, ','', regex =True # remove anything else extraneous from start
    ).str.strip() #remove any extra spaces
        
df.parsed_place.sort_values().unique()

df.assign(
    in_ca = df.parsed_place.str.endswith('California'),
    in_alaska = df.parsed_place.str.endswith('Alaska')
    ).sample(5, random_state = 0)

df.assign(
    in_ca = df.parsed_place.str.endswith('California'),
    in_alaska = df.parsed_place.str.endswith('Alaska'),
    neither = lambda x: ~x.in_ca & ~x.in_alaska
    ).sample(5, random_state = 0)

# adding new row
tsunami = df[df.tsunami ==1]
no_tsunami = df[df.tsunami != 1]
tsunami.shape
no_tsunami.shape

additional_columns = pd.read_csv(
    'data/earthquakes.csv', usecols = ['tz', 'felt', 'ids'])

pd.concat([df.head(2), additional_columns.head(2)], axis = 1)
