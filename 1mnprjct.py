import folium
import pandas as pd
from statistics import mean, median
import matplotlib.pyplot as mpt


# ACQUIRE THE REQUISITE DATA -----------------------------------------------------------------------------------------
p1 = "E:\edX\\6.miniProject\dataset\GNI_Cntry_WB.csv"  # country wise GNI index
p2 = "E:\edX\\6.miniProject\dataset\HDI_Cntry_UNDP.csv"  # HDI index and Country name
p3 = "E:\edX\\6.miniProject\dataset\\netDevAsst2018.csv"  #
p5 = "E:\edX\\6.miniProject\dataset\SDG_2003-2017.csv"  # SDG 14 features countrywise
# =====================================================================================================================

# DATA PREPARATION ( TAKE ONLY REQUIRE FOR ANALYSIS)-------------------------------------------------------------------
df_GNI = pd.read_csv(p1, sep=",")  # SeriesName = GNI per capita, PPP (current international $), YR=2004:2017
# print(df_GNI.head()) # count = 264 , freq = 1,

# Human Development Index Data 1990-2017-----------------------------------------------------------------------------
skp_col = [str(x) for x in range(1990,2000,1)]
df_HDI = pd.read_csv(p2,sep=',',skiprows=1,  encoding='latin-1')  # latin-1,
nit_df_HDI = df_HDI.dropna(axis='columns',how='all') # All full empty columns removed
nit_df_HDI.drop(skp_col,axis=1,inplace=True)  # drop the list of unwanted column using name
nit_df_HDI_r = nit_df_HDI.dropna()  # remove rows if value is not present anywhere
# nit_df2 is a Data for 2000-2017+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Country contribution for world development in terms of Value
df_devAsst = pd.read_csv(p3,sep=',')
df_devAsst_c = df_devAsst[['LOCATION', 'TIME', 'Value']]
# print(df_devAsst_c.describe())


df5 = pd.read_csv(p5,sep=',')

# FUNCTION THAT GIVEN STRING IS NUMBER ONLY FLOAT OR INTEGER---------------------------------------------------


def number(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
# =================================================================================================================

# PREPARING gni DF AND HDI DF FOR CLASSIFICATION OF DEVELOPING COUNTRIES ----------------------------------------------


cntryNameCode = df_GNI[['Country Name', 'Country Code']].dropna()
cntryNameCode.rename(columns={'Country Name': 'Country'},inplace=True)
df_GNI_2017 = df_GNI[['Country Name', '2017 [YR2017]']]  # gni of only 2017
df_GNI_2017.rename(columns={'2017 [YR2017]': 'GNI_2017','Country Name': 'Country'}, inplace=True)  # rename colmumn name
nit_df_GNI_2017 = df_GNI_2017.dropna()  # Country=172 dropped which rows are null,
nit_df_GNI_2017 = nit_df_GNI_2017[nit_df_GNI_2017.GNI_2017.apply(lambda x: number(x))]  # only numeric, dropped ".."
nit_df_HDI_r_2017 = nit_df_HDI_r[['Country','2017']] # Country=172
nit_df_HDI_r_2017['Country'] = (nit_df_HDI_r_2017['Country']).str.strip()
nit_df_HDI_r_2017.rename(columns={'2017':'HDI_2017'},inplace=True)
gni = [float(x) for x in (nit_df_GNI_2017['GNI_2017'])]
hdi = [float(x) for x in nit_df_HDI_r_2017['HDI_2017']]
# ======================================================================================================================

gni_thr = median(gni)   # Threshold to divide world into two parts at median value of GNI
hdi_thr = median(hdi)  # Threshold to divide world into two parts at median value of HDI

dvlpmt = pd.merge(nit_df_GNI_2017,nit_df_HDI_r_2017,on='Country',how='inner')  # inner merge two dataframes on Country
dvlpmt = dvlpmt.dropna()

# CREATE NEW COLUMN WHICH TELLS DEVELOP LEVEL OF GIVEN COUNTRY---------------------------------------------------------


def lvl(row):
    # row['HDI_2017'] = int(row['HDI_2017'])
    row['GNI_2017'] = int(row['GNI_2017'])
    if (row['HDI_2017']) <= hdi_thr and (row['GNI_2017']) <= gni_thr :
        return 'UnDeveloped'
    if hdi_thr < (row['HDI_2017']) <= max(hdi) and (row['GNI_2017']) <= gni_thr:
        return 'UnderDeveloped'
    if (row['HDI_2017']) <= hdi_thr and gni_thr <= (row['GNI_2017']) <= max(gni):
        return 'Developed'
    if hdi_thr <= row['HDI_2017'] <= max(hdi) and gni_thr <= row['GNI_2017'] <= max(gni):
        return 'HighlyDeveloped'


dvlpmt['level'] = dvlpmt.apply(lambda row: lvl(row), axis=1)
dvlpmt_plt = pd.merge(cntryNameCode,dvlpmt,on='Country')
rplc = {'UnDeveloped': 1, 'UnderDeveloped': 2, 'Developed': 3, 'HighlyDeveloped':4}
dvlpmt_plt = dvlpmt_plt[['Country Code', 'level']]
dvlpmt_plt = dvlpmt_plt.replace({'level': rplc})

# Plot of world Map to show development measures across the glob--------------------------------------------------------

map = folium.Map(location=(100,2),zoom_start=1)
cntry_geo = "E:\edX\\5.DataVisualization\world-countries.json"
map.choropleth(geo_data=cntry_geo,data=dvlpmt_plt,
               columns=['Country Code', 'level'],fill_color='RdYlGn',
               key_on='feature.id', legend_name='Development Level[ Un,Under,Developed,Highly]')
map.save("E:\edX\\6.miniProject\plots\cntryDvlpmt.html")

# dvlpmt contains Country Name with which category they belong, ========================================================

# SDG data  ----------------------------------------------------------------------------------------------------------
df_SDG = pd.read_csv(p5,sep=",")  # Country Name, Code, Series name,code,2003-2017 [YR2017]
df_SDG_2017 = df_SDG[['Country Name','Series Name', '2017 [YR2017]']]  # Only 2017 year all indicators selected

df_SDG_2017.rename(columns={'2017 [YR2017]': 'SDG_2017'},inplace=True)  # rename column
nit_df_SDG_2017 = df_SDG_2017[~df_SDG_2017['Series Name'].isnull()]  # remove null in Series Column
nit_df_SDG_2017 = nit_df_SDG_2017[nit_df_SDG_2017.SDG_2017.apply(lambda x: number(x))]  # rows: only number in SDG_2017
# nit_df_SDG_2017.reset_index(inplace=True)  # reset index and 949 is the count

# Country, Series Name, SDG_2107=======================================================================================
trnfm_nit_df_SDG_2017 = nit_df_SDG_2017.pivot(index='Country Name', columns='Series Name', values='SDG_2017')
# Here we come to know that Most of the countries missing VALUE for below Name:
trnfm_nit_df_SDG_2017.pop('Poverty headcount ratio at $1.90 a day (2011 PPP) (% of population)')
trnfm_nit_df_SDG_2017.pop('School enrollment, tertiary (% gross)')
trnfm_nit_df_SDG_2017 = trnfm_nit_df_SDG_2017.dropna()  # now remove rows having any null value
_nit_df_SDG_2017 = trnfm_nit_df_SDG_2017.reset_index().rename_axis(None, axis=1) # reshape pivot into dataframe
_nit_df_SDG_2017.rename(columns={'Country Name': 'Country'},inplace=True)

# Here we have Country as index and Series Name as column with only valid number.=======================================

# CONDSIDER ONLY THOSE COUNTRY WHICH ARE CATEGORIES IN DEVELOPMENT LEVEL------------------------------------------------

result = pd.merge(dvlpmt,_nit_df_SDG_2017,on='Country')  # Country 139,HDI,GNI,4-Series,Levels

# convert all the require columns into numeric from string of data
for x in range(4,8):
    result.iloc[:,x] = pd.to_numeric(result.iloc[:,x],errors='coerce')
result_IND_ = result[result['Country'].str.contains('India')]  # All the Features correspond to India
result_IND = result_IND_.reset_index()
result_IND.pop('index')
result_IND.pop('GNI_2017')
result_IND.pop('HDI_2017')
result_IND.pop('level')
result_IND.rename(columns={'Country': 'level'},inplace=True)

# HERE, WE FINISHED DATA TABLE THAT WE REQUIRED NOW NEXT IS FINAL STAGE ================================================


# DATA VISUALIZATION---------------------------------------------------------------------------------------------------
result.pop('HDI_2017')
result.pop('GNI_2017')
# Here we group result by level and again reshape level from index to column format
result_level = result.groupby('level').mean()
result_level = result_level.reset_index().rename_axis(None,axis=1)  # convert level from index to column as dataframe
complete = result_level.append(result_IND, ignore_index=True)  # development classify and India
complete_idx = complete.set_index('level')
complete_idx = complete_idx.reindex(['HighlyDeveloped', 'Developed', 'UnderDeveloped', 'UnDeveloped', 'India'])

pd_plt = complete_idx.plot.bar(rot=0, subplots=True, legend=False, grid=True)
print(complete_idx)
# for i in range(len(complete_idx.columns)):
# pd_plt = complete_idx.plot.bar(y=[complete_idx.columns[0], complete_idx.columns[1]], rot=0, grid=True)
# mpt.title('Share of unpaid Family Work')
mpt.show()











