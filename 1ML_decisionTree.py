# Importing all the libraries and module here--------------------------------------------------------------------------

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from statistics import median

# Now acquire the data-------------------------------------------------------------------------------------------------
data = pd.read_csv("E:\edX\week6\Week-7-MachineLearning\weather\daily_weather.csv")
# Above data has 9am airPressure, temp, (avg,max)-wind-(dir,speed), rain-(accumln,time) and has some null values
# So we need to clean data in following way
nit_Data = data.dropna()
nit_Data.pop('number')  # we don't need number for rows

# Classify relative Humidity_3pm into 0/1 form-------------------------------------------------------------------------
class_Data = nit_Data.copy()  # @50% Quantile of relative_humdty_3pm = 24.371286
Humidity_Thr = class_Data['relative_humidity_3pm'].median()
class_Data['HighHumidityLabel'] = (class_Data['relative_humidity_3pm'] > Humidity_Thr)*1

morn_Features = [x for x in class_Data.columns.tolist() if '9am' in x]  # morning features selected using 9am condition

# Lets create new X and Y dataframe from class Data features -------------------------------------------------------
X = class_Data[morn_Features].copy()  # all the coulmns from class data having 9m str
Y = class_Data[['HighHumidityLabel']].copy()  # coulmn that contains only 0/1 value for humidity 3pm

# Perform Train and Test split---------------------------------------------------------------------------------------
# x_train = predict data part for train, x_test = predict data for test model performance,
# y_train = response data part of x_train data,y_test = response data part of x_test data,: uses for crosscheck model.

x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.20,random_state=324)  # split predict and response
humid_classfr = DecisionTreeClassifier(max_leaf_nodes=10,random_state=0)
humid_classfr.fit(x_train,y_train)  # train data of available predict and response dataframe will build model
prdct = humid_classfr.predict(x_test)  # this is the model oriented Y value corresponds to test dataset of X
prfmnc = accuracy_score(y_true=y_test,y_pred=prdct)  # (0.8779) checked the performance of model the way trained


