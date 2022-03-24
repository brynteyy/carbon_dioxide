import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit
from scipy import stats
 
#This line takes the data from the Mlo lab and puts it into a dataframe
dfCarbonDioxide=pd.read_table('co2_mlo_surface-insitu_1_ccgg_DailyData.txt',delimiter=r"\s+",skiprows=150)
#Outlines a column for a new data table where the date is placed in to the column from the master dataframe above
dfCarbonDioxide['date']=pd.to_datetime(dfCarbonDioxide[['year', 'month', 'day', 'hour', 'minute', 'second']])
#Compares the value in the table to -999.99
boolMissing=dfCarbonDioxide['value']==-999.99
#all values that are -999.99 are replaced with nan on the dataframe via a bollean filter
dfCarbonDioxide[boolMissing]=np.nan
#Removes the data that has nan in a row
dfCarbonDioxide=dfCarbonDioxide.dropna()
#reseting the index where the old index is dropped (drop=true)
dfCarbonDioxide=dfCarbonDioxide.reset_index(drop=True)
#plotting date vs value
fig, ax = plt.subplots(figsize=(12,8))
ax.plot(dfCarbonDioxide['date'],dfCarbonDioxide['value'],'.k')
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')





