import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as mp

# First We will  import the dataset------------------------------------------------------------------
df = pd.read_csv('E:\ThinkBumble\\2.Dataframe,OurSurvivers\\datasetGiven.csv')
df2 = df.dropna()
# print(df2['Age'])
# mp.hist(df2['Age'], bins=10)
# mp.show()

# We are filling the null values of Age with initial reference
m1 = df['Name'].str.contains('Mr.')
m2 = df['Name'].str.contains('Mrs.')
m3 = df['Name'].str.contains('Miss.')
m4 = df['Name'].str.contains('Master.')
df.loc[m1,'Age'] = df.loc[m1, 'Age'].fillna(df.loc[m1, 'Age'].mode()[0])
df.loc[m2,'Age'] = df.loc[m2, 'Age'].fillna(df.loc[m2, 'Age'].mode()[0])
df.loc[m3,'Age'] = df.loc[m3, 'Age'].fillna(df.loc[m3, 'Age'].mode()[0])
df.loc[m4,'Age'] = df.loc[m4, 'Age'].fillna(df.loc[m4, 'Age'].mode()[0])

# Here we got age as Highest = 80, Average = 28, Min = 0.42 ( 5 Month)

print(df['Age'].mean())  # This is the Average Age of a passenger
print(df['Age'].max())   # This is the Maximum Age of a passenger
print(df['Age'].min())   # This is the Minimum Age of a passenger


# # Here Nominal features is Sex we will put Male = 1 and Female=0
le = LabelEncoder()
mask = ~df['Embarked'].isnull()
df['Embarked'][mask] = le.fit_transform(df['Embarked'][mask])
df['Sex'] = le.fit_transform(df['Sex'])


# CONVERTING AGE as CONTINUOUS VALUE INTO FOUR CATEGORY -------------------------------------------------------------


def aggrp(df):
    if df['Age'] <= 15:
        return 'Child'
    if 15 < df['Age'] <= 30:
        return 'Adult'
    if 30 < df['Age'] <= 50:
        return 'Matured'
    if 50 < df['Age']:
        return 'Aged'


df['AgeGroup'] = df.apply(lambda row: aggrp(row), axis=1)

# Here we tranform  dataframe is store locally
df.to_csv('E:\ThinkBumble\\datasetNew.csv')

# For survival statistics we required following columns only--------------------------------------------------
survive = df[['AgeGroup', 'Survived']]
surviveAge = survive.groupby('AgeGroup').sum()
totalAge = survive.groupby('AgeGroup').count()
totalAge.rename(columns={'Survived':'Total'}, inplace=True)
totalAge = totalAge.reset_index().rename_axis(None,axis=1)
surviveAge = surviveAge.reset_index().rename_axis(None,axis=1)
survive_ttl = pd.merge(surviveAge, totalAge, on='AgeGroup')
survive_ttl['Survived Percentage'] = (survive_ttl['Survived'])*100/(survive_ttl['Total'])
survive_ttl.to_csv('group-wise_survive.csv')

l = {y:x for x,y in enumerate(survive_ttl['AgeGroup'])}
print(l)
survive_ttl= survive_ttl.reindex([l['Child'], l['Adult'], l['Matured'], l['Aged']])
survive_ttl = survive_ttl.set_index('AgeGroup')
print(survive_ttl)
# Visualizing the entire data for survival and its percentage------------------------------------------
# fig = mp.figure()
# ax1 = fig.add_subplot(2,1,1)
# ax2 = fig.add_subplot(2,1,2)
# ax1.bar(survive_ttl['AgeGroup'], survive_ttl['Survived'])
# # ax1.title('Passenger Survivals')
# ax1.xlabel('Age Group')
# ax1.ylabel('Survived')
# ax1.grid()
# # mp.show()
#
# ax2.bar(survive_ttl['AgeGroup'], survive_ttl['Survived Percentage'])
# # ax2.title('Passenger Survivals')
# ax2.xlabel('Age Group')
# ax2.ylabel('Survived Percenatge')
# ax2.ylim((0,100))
# ax1.grid()
# mp.show()
survive_ttl.plot.bar(y=['Survived','Total'], rot=0)
mp.title('Passenger Audit')
mp.show()
survive_ttl.plot.bar(y='Survived Percentage', rot=0)
mp.title('Passenger Audit')
mp.ylim((0,100))
mp.show()





