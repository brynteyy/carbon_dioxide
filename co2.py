import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit
from scipy import stats

def fitPly(x,c2,c1,c0):
    y=x**2*c2+x*c1+c0
    return y

def fitPly3(x,c3,c2,c1,c0):
    y=x**3*c3+x**2*c2+x*c1+c0
    return y

def fitOsc(x,amp,period,offset):
    y=amp/2 * np.cos((x + offset)  * 2 * np.pi/period)
    #y=amp*np.cos(period*(x+offset))
    return y

# def fitAll(x,c2,c1,c0,amp,period,offset,amp2,period2,offset2):
#     y=fitPly(x,c2,c1,c0)+fitOsc(x,amp,period,offset)+fitOsc(x,amp2,period2,offset2)
#     return y 

def fitAll(x,c3,c2,c1,c0,amp,period,offset):
    y=fitPly3(x,c3,c2,c1,c0)+fitOsc(x,amp,period,offset)
    return y  

def fitPart(x,c2,c1,c0,amp,period,offset):
    y=fitPly(x,c2,c1,c0)+fitOsc(x,amp,period,offset)
    return y  

dfCarbonDioxide=pd.read_table('co2_mlo.txt',delimiter=r"\s+",skiprows=151)
dfCarbonDioxide['date']=pd.to_datetime(dfCarbonDioxide[['year', 'month', 'day', 'hour', 'minute', 'second']])
boolMissing=dfCarbonDioxide['value']==-999.99
dfCarbonDioxide[boolMissing]=np.nan
dfCarbonDioxide=dfCarbonDioxide.dropna()
dfCarbonDioxide=dfCarbonDioxide.reset_index(drop=True)

fig, ax = plt.subplots(figsize=(12,8))
ax.plot(dfCarbonDioxide['date'],dfCarbonDioxide['value'],'.k')
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')

startDate=min(dfCarbonDioxide['date'])
timeElapsed=dfCarbonDioxide['date']-startDate
daysSinceStart=timeElapsed.dt.days

fitCoeffs = np.polyfit(daysSinceStart, dfCarbonDioxide['value'], 2)
fitCoeffs3 = np.polyfit(daysSinceStart, dfCarbonDioxide['value'], 3)
poptAll, pcov = curve_fit(fitAll, daysSinceStart, dfCarbonDioxide['value'],p0=[fitCoeffs3[0],fitCoeffs3[1],fitCoeffs3[2],fitCoeffs3[3],8,365.25,-144])
poptPart, pcov = curve_fit(fitPart, daysSinceStart, dfCarbonDioxide['value'],p0=[fitCoeffs[0],fitCoeffs[1],fitCoeffs[2],8,365.25,-144])

fitCO2ply=fitPly(daysSinceStart,fitCoeffs[0],fitCoeffs[1],fitCoeffs[2])
fitCO2all=fitAll(daysSinceStart,poptAll[0],poptAll[1],poptAll[2],poptAll[3],poptAll[4],poptAll[5],poptAll[6])
fitCO2part=fitPart(daysSinceStart,poptPart[0],poptPart[1],poptPart[2],poptPart[3],poptPart[4],poptPart[5])
ax.plot(dfCarbonDioxide['date'],fitCO2all,'-r')
ax.plot(dfCarbonDioxide['date'],fitCO2ply,'-g')
ax.plot(dfCarbonDioxide['date'],fitCO2part,'-b')

residualsAll=fitCO2all-dfCarbonDioxide['value']
residualsPart=fitCO2part-dfCarbonDioxide['value']
residualsPly=fitCO2ply-dfCarbonDioxide['value']
figRes,axRes=plt.subplots()
axRes.plot(daysSinceStart,residualsAll,'-r')
axRes.plot(daysSinceStart,residualsPly,'-g')
axRes.plot(daysSinceStart,residualsPart,'-b')

rss1=np.sum(residualsPart**2)
rss2=np.sum(residualsAll**2)
p1=len(poptPart)
p2=len(poptAll)
n=len(dfCarbonDioxide['value'])
fCalc=((rss1-rss2)/(p2-p1))/(rss2/(n-p2))
fTable=stats.f.ppf(1-(0.05), p2-p1,n-p2)

stdErrorAll=np.sqrt(np.sum(residualsAll**2)/(len(dfCarbonDioxide['value'])-len(poptAll)))
stdErrorPart=np.sqrt(np.sum(residualsPart**2)/(len(dfCarbonDioxide['value'])-len(poptPart)))
stdErrorPly=np.sqrt(np.sum(residualsPly**2)/(len(dfCarbonDioxide['value'])-len(fitCoeffs)))

dateToPredict=pd.to_datetime('2021-04-08 00:00:00')
dayToPredict=dateToPredict-startDate
daysSinceStartPrediction=dayToPredict.days
print(daysSinceStartPrediction)
predictedCO2=fitAll(daysSinceStartPrediction,poptAll[0],poptAll[1],poptAll[2],poptAll[3],poptAll[4],poptAll[5],poptAll[6])
#oscillationCalc=fitOsc(daysSinceStart,8,365.25,-144)
#oscillationCalc=fitOsc(daysSinceStart,4,180,-144)
#axRes.plot(daysSinceStart,oscillationCalc)

#popt, pcov = curve_fit(fitOsc, daysSinceStart, residualsPart,p0=[4,365*20,-144])
#oscillationCalc=fitOsc(daysSinceStart,popt[0],popt[1],popt[2])
#axRes.plot(daysSinceStart,oscillationCalc)





