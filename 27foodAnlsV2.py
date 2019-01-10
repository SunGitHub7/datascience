import pymysql.cursors
import pandas as pd
import matplotlib.pyplot as pt
from pandas import Series

class dbcon:

    def __init__(self,qry):
        self.q=qry

    # def __init__(self,X,Y):
    #     self.x = X
    #     self.y = Y

    con = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sun@MySql7!', db='citydata')
    cur = con.cursor()


    def data(self):
        self.cur.execute(self.q)
        db = self.cur.fetchall()

        return db

    def head(self):
        self.cur.execute(self.q)
        hdb = self.cur.description

        hL = [field[0] for field in hdb] # head List

        return hL
    def present(self,Ttl,xLbl,yLbl,XLst,YLst):
        pt.barh(XLst,YLst)
        pt.title(Ttl)
        pt.xlabel(xLbl)
        pt.ylabel(yLbl)
        pt.tight_layout()
        return pt.show()

    # def best(self,):



sql = 'SELECT * FROM citydata.fooddata'

a = dbcon(sql)
dB1 = a.data()
hL = a.head() # head of database

fLn = len(hL)
vD=[]

# ! loop will create field dependent empty list inside like -> vD = [[],[],[],[]]
for x in range(fLn):
    vD.append([])

for i in dB1:
    dL = list(i) # convert data into list

    # ! this loop will give list of coulumn values
    for j in range(len(hL)): # add values into inner list respective index j
        vD[j].append(dL[j])
# print(vD)
dF = dict(zip(hL,vD))  # this will map outer list coulumnwise as values to field name as keys
print(hL)
p = pd.DataFrame.from_dict(dF)
print(p)
pT = p[p.Rating != 'n/a']
pT2 = pT.replace(['Very Bad','Bad', 'OK', 'Good','Very Good'],[1,2,3,4,5])


a.present('Qulity Survey','Rating','Food Type',list(pT['Type']), list(pT['Rating']))
a.present('Likes Survey','Rating','Food Type',pT['Type'],pT['Rating'])
a.present("Quality Survey","Fat (gm)","Food Type",pT['Type'],pT['Total Fat (g)'])

# pT3 = pT2.loc[:,['FastFood','Type','Rating','Saturated Fat (g)','Calories']]
#
# i = pT3.groupby('Saturated Fat (g)')['Rating'].idxmin
# pT4 = pT3.loc[i]
#
# j=pT4['Rating'].idxmax
# pT5 = pT4.loc[j]

# print("Best Product of the Survey based on Rating,then Fate, then Calories \n")
# print(pT5)




