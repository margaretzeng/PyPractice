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
