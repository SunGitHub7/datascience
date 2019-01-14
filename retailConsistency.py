import pandas as pd
df = pd.read_csv('E:\ThinkBumble\Online Retail.csv')
df['month'] = df['InvoiceDate'].str.extract("/(\d+)/")  # month column having value extracted from data string.
# print(df)
df2= df[['CustomerID', 'revenue','month']]  # select only desire features
# print(df2)
df3 = df2.groupby(['CustomerID', 'month']).mean()  # We need to know revenue for each customer for each month
# print(df3)
df4 = df3.unstack()  # cast row of month into columns
df4.columns = df4.columns.droplevel(0)
df4 = df4.reset_index().rename_axis(None, axis=1)
df4['consistency'] = df4[['1','2','3']].std(axis=1)  # standard deviation
df5 = df4[['CustomerID', 'consistency']]
print(df4)
#
def consistent(df):
    if df > 10:
        return 'No'
    else:
        return 'Yes'


df4['consistant'] = df4['consistency'].apply(lambda x: consistent(x))

print(df4)
''' CustomerID          1          2          3  consistency consistant
0       13694   4.371667  11.991667  14.020000     5.087057        Yes
1       13758   3.218824  19.061765  15.279412     8.274084        Yes
2       14307  17.940000  45.720000  20.136000    15.443941         No
3       17908   4.297222  27.840000   7.783333    12.706201         No
4       17920   4.891500  15.013000  58.454500    28.456410         No
5       17968   5.326207  15.420690  15.398276     5.821593        Yes'''

