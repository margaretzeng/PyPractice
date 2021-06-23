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
