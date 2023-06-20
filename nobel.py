# this project was part of the DataCamp Data Scientist with Python track 
# the dataset is the Nobel Laureate winner datset, which is available on Kaggle
# this is a simple project to load, manipulate and visualise data with
# Pandas, Matplotlib and Seaborn

# Load required libraries
import pandas as pd
import seaborn as sns
import numpy as np

# read in the Nobel Prize Data from computer (this line of code will change according to where your csv is located)
# the location of the dataset will depend on where you load it from
# the one provided below is a generic local computer location
nobel = pd.read_csv('/Udatasets/nobel.csv')

# looking at the top rows of the dataset...
print(nobel.head())

# ...or just the names of the columns, if scree space is an issue
print(nobel.columns)


# display the number of nobel prizes (rows)
display(len(nobel))

# display the number of nobels split between male and female
display(len(nobel[nobel['Sex']=='Male']))

display(len(nobel[nobel['Sex']=='Female']))

# Count the number of nobels won by the top 10 birth countries

nobel['Birth Country'].value_counts()[:10]


# in this section will find out when the USA became dominant
# let's start by adding a new boolean column for US winners
nobel['USA born winner']= nobel['Birth Country'] == 'United States of America'

# we then add a decade columns with the np.floor function
nobel['Decade']= (np.floor(nobel['Year']/10)*10).astype(int)

# finally we initiate a new dataframe, which calculates the mean US winners by decade
prop_usa_winner = nobel.groupby('Decade', as_index=False)['USA born winner'].mean()
print(prop_usa_winner)


# more libraries first
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt

# let's plot the table of US winners by decade
ax = sns.lineplot(data = prop_usa_winner, x='Decade', y='USA born winner')

# formatting y axis as percentage
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))

# display the plot
plt.show()


# we now do the same for female winners. First we create a female winner column...
nobel['Female Winner'] = nobel['Sex']=='Female'
#...then we created a new dataframe and group it by decade and category
prop_female_winner = nobel.groupby(['Decade', 'Category'],as_index=False)['Female Winner'].mean()

print(prop_female_winner)


# now we plot the proportion of female winners
# let's plot the table of US winners by decade, addin a category hue
ax = sns.lineplot(data = prop_female_winner, x='Decade', y='Female Winner', hue = 'Category')

# formatting y axis as percentage
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))

# display the plot
plt.show()

#not the cleanest plot, nor the easiest to understand


#when was the nobel first won by a female? it turns out, it was 1903

print(nobel.loc[nobel['Sex'] == 'Female'].head(1))


# and who has won the nobel more than once?

print(nobel.groupby('Full Name').filter(lambda x: len(x)>=2))


# let us now investigate the age of nobel winners
# first we need to convert the birth date colum to the right data type
# the coerce method was added
# to handle invalid or unparseable values in the datetime column

nobel['Birth Date'] = pd.to_datetime(nobel['Birth Date'], errors = 'coerce')

# then we calculate the age of the winners at the time of the award. 
nobel['age'] = nobel['Year'] - nobel['Birth Date'].dt.year
print(nobel['age'].head())

# now we plot
ax = sns.lmplot(x = 'Year', y = 'age', data = nobel, lowess=True, aspect = 2, line_kws={'color': 'black'})
plt.show()

# as an added bonus, I want to print some basic stats for age, to go with the plot

print(nobel['age'].describe())


# age trends within categories
# we can plot the ages, adding a 'row' argument

ax = sns.lmplot(x = 'Year', y = 'age', data = nobel, row = 'Category', lowess=True, aspect = 2, line_kws={'color': 'black'})

plt.show()


# we already saw the youngst and oldest ages to be awarded the nobel. But who were they?

print(nobel.loc[nobel['age'].idxmin()])
print(nobel.loc[nobel['age'].idxmax()])




