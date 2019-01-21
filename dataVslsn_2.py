import folium
import pandas as pd

cntry_geo = "E:\edX\week5\world-countries.json"
indctr = pd.read_csv("E:\edX\week5\Indicators.csv")

hst_CO2 = 'CO2 emissions \(metric'
hst_yr = 2011
CO2 = indctr['IndicatorName'].str.contains(hst_CO2)  # fILTER FOR CO2 Indicator Name
yr2011 = indctr['Year'].isin([hst_yr])   # Filter for Year 2011

CO2_2011 = indctr[yr2011 & CO2]  # New DataFrame having => year:2011, IndctrNm:CO2(mtpc)
CO2_2011_2 = CO2_2011[['CountryCode', 'Value']]  # 2 column require CoutryCode and Value of CO2 emission
hst_lgnd = CO2_2011.iloc[0]['IndicatorName']

# VISUALIZE CO2 EMISSION USING FOLIUM
map = folium.Map(location=[100,0],zoom_start=1.5)

# choropleth maps bind pandas data and json geometries
# lnrCM = folium.LinearColormap(['green','yellow','red'])
# print(range(len(CO2_2011_2['Value'])))
# print(CO2)
map.choropleth(geo_data=cntry_geo,data=CO2_2011_2,
               columns=['CountryCode', 'Value'],
               key_on='feature.id',legend_name=hst_lgnd,
               fill_color='OrRd')
map.save("E:\edX\week5\plots\cntry.html")  # Go to this place and click on file

# print(CO2_2011_2)

