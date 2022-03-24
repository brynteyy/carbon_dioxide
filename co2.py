import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit
from scipy import stats

def fitply(x,c2,c1,c0):
    y=x**2*c2+x*c1+c0
    return y
#This line takes the data from the Mlo lab and puts it into a dataframe
dfCarbonDioxide=pd.read_table('co2_mlo_surface-insitu_1_ccgg_DailyData.txt',delimiter=r"\s+",skiprows=150)
#Outlines a column for a new data table where the date is placed in to the column from the master dataframe above
dfCarbonDioxide['date']=pd.to_datetime(dfCarbonDioxide[['year', 'month', 'day', 'hour', 'minute', 'second']])
#this is munging the data
#Compares the value in the table to -999.99 (centinal value that means the data isn't there)
boolMissing=dfCarbonDioxide['value']==-999.99
#all values that are -999.99 are replaced with nan on the dataframe via a boolean filter
dfCarbonDioxide[boolMissing]=np.nan
#Removes the data that has nan in a row
dfCarbonDioxide=dfCarbonDioxide.dropna()
#reseting the index where the old index is dropped (drop=true)
dfCarbonDioxide=dfCarbonDioxide.reset_index(drop=True)
#plotting date vs value
fig, ax = plt.subplots(figsize=(12,8))
ax.plot(dfCarbonDioxide['date'],dfCarbonDioxide['value'],'.k')
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')

#Creating time elapsed data
startDate=min(dfCarbonDioxide['date'])
timeElapsed=dfCarbonDioxide['date']-startDate
#Dates in days
daysSinceStart=timeElapsed.dt.days

coeffs=np.polyfit(daysSinceStart,dfCarbonDioxide['value'],2)
fitCO2=fitply(daysSinceStart,coeffs[0],coeffs[1],coeffs[2])
ax.plot(dfCarbonDioxide['date'],fitCO2,'-r')



