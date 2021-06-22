import numpy as np

data = np.genfromtxt(
    './data/example_data.csv', delimiter=';',
    names=True, dtype=None, encoding='UTF'
)

#Now having the data in a Numpy array
data


#Get the dimentsions of the array
data.shape

#Get the data types the array contains.
data.dtype

