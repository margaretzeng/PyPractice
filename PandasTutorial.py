import pandas as pd

titanic = pd.read_csv('data/titanic.csv')

titanic.head()

## How to select specific columns from DF
# if i'm interested in the age of the titanic passenger
titanic['Age']
titanic['Age'].shape

# if i'm interested in the age and sex of the Titanic passenger
titanic[['Age', 'Sex']]

## How to filter/select specific rows from DF
# if i'm interseted passengers older than 35 years.

above_35 = titanic[titanic['Age'] > 35]


titanic['Age'] > 35 # this is a pandas Series of boolean values. Such a Series of boolean values can be used to filter the DF by putting in between selection brackets []. only rows whose value is True will be selected.

# if i'm interested in the Titanic passengers from cabin class 2 and 3
titanic[(titanic['Pclass'] == 2) | (titanic['Pclass'] == 3)] #我自己写的
titanic[titanic['Pclass'].isin([2,3])]

# if i'm interested in the NAMES of the passengers older than 35 years.
testing = titanic.loc[titanic['Age']>35, 'Name']


air_quality = pd.read_csv('data/air_quality_long.csv', index_col= 'date.utc', parse_dates=True)
no2 = air_quality[air_quality['parameter'] == 'no2'].sort_index()

no2_subset = no2.sort_index().groupby(['location']).head(2) # look two row ( by head()) for each locaiton (by groupby)
no2testing = no2.sort_index().groupby(['location']).head(100)

no2.sort_index().groupby(['location']).head()


