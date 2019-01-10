import pandas as pd
import numpy as np
import matplotlib.pyplot as mpt
pd.set_option('display.width', 1000)
# -------------DATA INGESTION------------------------------------------------------------------------------------------
movies = pd.read_csv("E:\edX\\4.Pandas\ml-20m\movies.csv", sep=",")
tags = pd.read_csv("E:\edX\\4.Pandas\ml-20m\\tags.csv", sep=",")
ratings = pd.read_csv("E:\edX\\4.Pandas\ml-20m\\ratings.csv", sep=",", parse_dates=['timestamp'], engine='python')
print(movies.head(5))
# print(tags.head(5))
# print(ratings.head(5))
df_movies = pd.DataFrame(movies)

# print(ratings['rating'].describe())

# Display The Box Plot of rating column
# box_rate = pd.DataFrame(ratings)
# box_rate.boxplot(column=['rating'])
# mpt.show()

# print(ratings.corr())
#              userId   movieId    rating  timestamp
# userId     1.000000 -0.002837  0.017105  -0.009661
# movieId   -0.002837  1.000000  0.002550   0.458975
# rating     0.017105  0.002550  1.000000  -0.000916
# timestamp -0.009661  0.458975 -0.000916   1.000000


# Another Trick to fetch Big data
# rate_List = []
# for rate in pd.read_csv("E:\edX\week4\ml-20m\\ratings.csv",
#                         chunksize=20000, sep=",", parse_dates=['timestamp'], engine='python'):
#     rate_List.append(rate)
# ratings = pd.concat(rate_List,axis=0)
# If we use engine='pythpn' then only big data can be fetch


# ---------Data Cleaning------------------------------------------------------------------------------------------------

# check data size
m_shape = df_movies.shape
t_shape = tags.shape
r_shape = ratings.shape
# print(m_shape)

# print(tags.isnull().any())

# In tags file, tag column has null values so we will clean it
nit_tags = tags.dropna() # Here all null values rows will be deleted

# Here, only tags file has null values so only that need to clean+++++++++++++++++++++++++++++++++++++++++++++++++++++

# DATA VISUALIZATION-------------------------------------------------------------------------------------------------
# f1 = mpt.figure(1)
# f2 = mpt.figure(2)
# ratings.hist(column='rating')
# mpt.show()
# ratings.boxplot(column='rating')
# mpt.show()


# FREQUENT DATA OPERATIONS---------------------------------------------------------------------------------------------

# print(tags['tag'].head())  #
# print(movies[['title','genres']].head())
# print(tags['tag'].value_counts())


# DATA MERGING----------------------------------------------------------------------------------------------------------
t = movies.merge(tags, on='movieId', how='inner')
# print(t.head(10))

# DATA GROUP BY------------------------------------------------------
avg_rtgs = ratings.groupby('movieId', as_index=False).mean()
del avg_rtgs['userId']
del avg_rtgs['timestamp']
# print(avg_rtgs.head())

box_office = movies.merge(avg_rtgs, how='inner',on='movieId')


hit_bx_Offc = box_office[box_office['rating'] >= 3.5]
df = pd.DataFrame(hit_bx_Offc)

# print(df[:5].append(df[5:10]).reset_index())  # stacking two dataframes

# STRING OPERATIONS IN DATAFRAME----------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
# print(movies.head())
movies['year'] = movies['title'].str.extract('(\d+)')
movies[['name','year']] = movies['title'].str.split("(", 1, expand=True)
movies.pop('title')
movies['year'] = movies['year'].str.strip(")")

print(movies.head())
# print(movies['year'].head())

# PARSING TIMESTAMP FROM INT64 TO PYTHON FORMAT------------------------------------------------------------------------
tags['parsed Date'] = pd.to_datetime(tags['timestamp'],unit='s')
sort_tags = tags.sort_values('parsed Date')
print(sort_tags.head())



















