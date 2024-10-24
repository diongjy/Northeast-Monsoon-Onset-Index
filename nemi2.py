import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
#from matplotlib.patches import Rectangle

#get the timestamp and prepare to get the file
ct = datetime.datetime.now().date()
print(ct)


def subtract_days_from_date(date, days):
    """Subtract days from a date and return the date.
    
    Args: 
        date (string): Date string in YYYY-MM-DD format. 
        days (int): Number of days to subtract from date
    
    Returns: 
        date (date): Date in YYYY-MM-DD with X days subtracted. 
    """
    
    subtracted_date = pd.to_datetime(date) - timedelta(days=days)
    subtracted_date = subtracted_date.strftime("%Y-%m-%d")

    return subtracted_date

forecast_date = subtract_days_from_date(ct, 1)

#convert forecast date to string
fdate = str(forecast_date)
year=fdate[0:4]
mon=fdate[5:7]
day=fdate[8:10]
fdate1=year+mon+day

#open the forecast file
fn1='./gefs/dly-v925_'+str(fdate1)+'_gfs_gefs_00z.txt'
print(fn1)

df1=pd.read_csv(fn1,header=None,parse_dates=True)
header=['Date','NEMI2']
df1.columns=header

#open the temporary file
df2=pd.read_csv('gefs_temp.txt',header=None,parse_dates=True)
header=['Date','NEMI2']
df2.columns=header

#merge two files
df = df2.merge(df1, on=['Date','NEMI2'], how='outer')

#df=pd.read_csv('gefs_nemi2.txt', header=None, parse_dates=True)
#header=['Date','NEMI2']
#df.columns=header
#find the first day that meet the < -2.5 m/s criterion
i=df.NEMI2.lt(-2.5).idxmax()
#print(df.loc[i])
#select next 15 days and average the next 15 days
if i < 15:  
    i2=i+14
    i3=i+9
    df_new=df.iloc[i:i2]
    average=df_new['NEMI2'].mean()
#otherwise set as 0
if i >= 15:
    i3=i+1
    average=0.0
#plot
x=df['Date']
y=df['NEMI2']
plt.figure(figsize=(10,8))
ax=plt.subplot(111)
plt.plot(x,y,marker='8')
plt.xticks(fontsize=8, rotation=90)
plt.ylabel("V-component (m/s)")
plt.title('GEFS NEMO Forecast Updated:'+str(ct))
#plt.title('NEMI2 Test')
#find the ceiling value for NEMI2
maxy=max(df['NEMI2'].apply(np.ceil))+1.0
miny=min(df['NEMI2'].apply(np.floor))
avey=(maxy+miny)/2
#find the forecast date
forecast=x.loc[14]
forecast1=x.loc[15]
#find the onset
x_date=x.iloc[26]
if average <= -1.0:
    onset=x.iloc[i3]
    plt.text(str(x_date), maxy, 'Onset Criteria = meet', fontsize=8 )
    plt.text(str(x_date), maxy-0.5, 'Onset Date :'+str(onset), fontsize=8 )
    onset_Date=x.iloc[i3]
    #ax.add_patch(Rectangle((onset_Date,-1),onset_Date,maxy+1,color="0.8"))
else :
     plt.text(str(x_date), maxy, 'Onset Criteria = not meet', fontsize=8 )
plt.axvline(str(forecast), ymin=miny, ymax=maxy-1, color='g', linestyle=':', linewidth=1)
plt.text(str(forecast1), avey, 'Forecast starts', fontsize=10 )
plt.savefig('./output/GEFS_NEMO.png')

#select data for next day forecast
df_temp=df.iloc[1:15]
df_temp.to_csv('gefs_temp.txt',header=False,index=False)



#running 15 days mean
#df['r15']=df['NEMI2'].rolling(15).mean()
#df_loc=df.loc[df['r15']<-2.5]
#idx=df.index[df['r15'] <-2.5].tolist()
#idx=df.index[df['r15'] <-2.5]
#idx1=idx-1
#print(df.loc[idx1])


