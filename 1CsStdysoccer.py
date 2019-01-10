import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as mpt
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from edXdTSc.customplot import *


# INGEST DATA-----------------------------------------------------------------------------------------------------------

cnx = sqlite3.connect('E:\edX\\1.Getting Started with Data Science\dataSet\database.sqlite')  # connection Object
crsr = cnx.cursor()
for tbl in crsr.execute('SELECT name FROM sqlite_master'):  # read the table present in given database
    print(tbl)   # one of the table name: Player_Attributes is needed to work ahead
df = pd.read_sql_query('select * from Player_Attributes',cnx)

nit_df = df.dropna()  # delete all rows contains null value
cols = [x for x in nit_df.columns]  # make list of columns name

numCols = nit_df.select_dtypes(include=[np.number]).columns.tolist()  # make list of columns with numeric values
numCols_ = numCols[4:]

# Check for any null value
print(nit_df.isnull().any().any())


corlts = [nit_df['overall_rating'].corr(nit_df[x]) for x in numCols_]
# print(len(corlts))

# CREATE DATAFARME WITH LIST OF SELECTED NUMERIC COLS AND CORLTS VALUES
corr_df = pd.DataFrame({'Predicts': numCols_,'Impact_Value': corlts})
# print(corr_df)

# PLOT DATAFRAME PREDICTS AS X AXIS AND CORRELATION VALUE---------------------------------------------------------------

print(corr_df.sort_values)
corrPlot = corr_df.sort_values(by='Impact_Value',ascending=False).plot.barh(x='Predicts',
                             y='Impact_Value',
                             title='Correlations of Player\'s Attributes', grid='True')

corrPlot.set_xlabel('Correlation Factor')
mpt.tight_layout()
mpt.show()

corrPlot = corr_df.plot.barh(x='Predicts',
                             y='Impact_Value',
                             title='Correlations of Player\'s Attributes', grid='True')


def show_bar(Ttl,XLbl,YLbl,XLst,YLst):
    mpt.barh(XLst,YLst)
    mpt.title(Ttl)
    mpt.xlabel(XLbl)
    mpt.ylabel(YLbl)
    mpt.tight_layout()
    return mpt.show()


show_bar('Correlations of Player\'s Attributes','Correlation with Overall Rating',   # local function call for bar plot
         'Predicts', corr_df['Predicts'], corr_df['Impact_Value'])

# **** ANALYSIS OF FINDINGS: IF WE NEED TO CHOOSE FIVE ATTRIBUTES THEN IT WILL BE BASIS ON CORRELATION PLOT *********

# CLUSTERING OF PLAYERS IN SAME GROUP-----------------------------------------------------------------------------------

# Based on domain knowledge we will select five probably independent features
core5Fchr = ['gk_kicking','potential','marking','interceptions','standing_tackle']


slctDF = nit_df[core5Fchr].copy(deep=True)  # make dataframe of above mentioned features
# print(slctDF.head())

# PERFORM KMeans CLUSERING ------------------------------------------------------------------------------------------

data = scale(slctDF) # Perform Scaling on slctDF
# print(data)
clst = 4  # Number of Cluster

model = KMeans(init='k-means++',n_init=20,n_clusters=clst).fit(data)  # Train Model
# print("Number of Players in each CLUSTER")
print(pd.value_counts(model.labels_,sort=False))

p = pd_centers(featuresUsed=core5Fchr,centers=model.cluster_centers_)
print(p)
#    gk_kicking  potential   marking  interceptions  standing_tackle  prediction
# 0    1.920534   0.037484 -1.111884      -0.653663        -1.201288           0
# 1   -0.039925   0.704706  1.027707       0.982640         1.030279           1
# 2   -0.477098   0.105698 -0.947597      -0.975163        -0.914172           2
# 3   -0.337640  -0.843239  0.548462       0.407593         0.550981           3

clstPlot = parallel_plot(p)
mpt.show()
# ANALYSIS OF FINDINGS : Group (0,2) and  behave similar except in GK_KICKING attribute

