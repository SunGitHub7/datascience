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
    if df['consistency'] > 10:
        return 'Yes'
    else:
        return 'No'


df4['consistant'] = df4.apply(lambda x: consistent(x), axis=1)

print(df4)
