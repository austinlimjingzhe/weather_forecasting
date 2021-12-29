# import relevant libraries
import pandas as pd
import numpy as np
import os
import geocoder
import haversine as hs
import sys
import math
import pymysql

# set the directory
os.chdir("YOUR FILE DIRECTORY")
os.getcwd()

#either use pandas to read csv if downloaded from mysql
temperature=pd.read_csv("temperature.csv")
humidity=pd.read_csv("humidity.csv")
rainfall=pd.read_csv("rainfall.csv")
windspeed=pd.read_csv("windspeed.csv")
winddirection=pd.read_csv("winddirection.csv")

'''
# or connect directly to sql database in which case note that the timestamp column is 
# already in datetime format.

_CONN = pymysql.connect(host='localhost',
                            user='root',
                            password='*************',
                            db='weather')
cursor = _CONN.cursor(pymysql.cursors.DictCursor)

cursor.execute("select * from rainfall where year(`timestamp`)>=2018 order by `timestamp`")
rainfall=pd.DataFrame(cursor.fetchall())

cursor.execute("select * from temperature where year(`timestamp`)>=2018 order by `timestamp`")
temperature=pd.DataFrame(cursor.fetchall())

cursor.execute("select * from humidity where year(`timestamp`)>=2018 order by `timestamp`")
humidity=pd.DataFrame(cursor.fetchall())

cursor.execute("select * from windspeed where year(`timestamp`)>=2018 order by `timestamp`")
windspeed=pd.DataFrame(cursor.fetchall())

cursor.execute("select * from winddirection where year(`timestamp`)>=2018 order by `timestamp`")
winddirection=pd.DataFrame(cursor.fetchall())
'''

runtimes=list(pd.date_range('2020-01-01T00:00:00Z',
                            '2020-06-30T23:59:59Z',
                            freq='60T').strftime('%Y-%m-%d %H:%M:%S'))

def cardinal_direction(degree):
    directions=["N","NNE","NE","ENE","E","ESE", "SE","SSE","S","SSW","SW","WSW", "W","WNW","NW","NNW","N"]
    return(directions[math.floor((degree+11.25)/22.5)])

rainfall['reading'] = np.where(rainfall['reading']>0,1,0)
winddirection['direction']=np.zeros(winddirection.shape[0])
for i in range(0,len(winddirection)):
    winddirection['direction'][i]=cardinal_direction(winddirection['reading'][i])

# this allows users to input the location in singapore that the user wants to check the weather for.
location=input("Please enter the address of the location you want to check: ")
g=geocoder.google(location, key="******************", components="country:singapore") #geocoder gives a latitude-longitude coordinate

data=pd.DataFrame(np.zeros(shape=(len(runtimes),6)),columns=["timestamp","temperature","humidity","windspeed","winddirection","rain"])

for runtime in runtimes:
    data["timestamp"].loc[runtimes.index(runtime)]=runtime
    
    temp_rain=rainfall[rainfall['timestamp']==runtime]
    temp_temperature=temperature[temperature['timestamp']==runtime]
    temp_humidity=humidity[humidity['timestamp']==runtime]
    temp_windspeed=windspeed[windspeed['timestamp']==runtime]
    temp_winddir=winddirection[winddirection['timestamp']==runtime]
    
    if temp_rain.shape[0]==0:
        continue
    if temp_temperature.shape[0]==0:
        continue
    if temp_humidity.shape[0]==0:
        continue
    if temp_windspeed.shape[0]==0:
        continue
    if temp_winddir.shape[0]==0:
        continue
  
    rain_station_dist=sys.maxsize
    temp_station_dist=sys.maxsize
    hum_station_dist=sys.maxsize
    windsp_station_dist=sys.maxsize
    winddir_station_dist=sys.maxsize
    
    closest_rain_station=str()
    closest_temp_station=str()
    closest_hum_station=str()
    closest_windsp_station=str()
    closest_winddir_station=str()
    
    #this code below finds the nearest reading to use out of all the readings stored
    for index,row in temp_rain.iterrows():
        dist_r=hs.haversine(g.latlng,(row["latitude"],row["longitude"]))
        if dist_r < rain_station_dist:
            rain_station_dist=dist_r
            closest_rain_station=row["station_id"]
    data["rain"].loc[runtimes.index(runtime)]=temp_rain[temp_rain["station_id"]==closest_rain_station].reading.item()
    
    for index,row in temp_temperature.iterrows():
        dist_t=hs.haversine(g.latlng,(row["latitude"],row["longitude"]))
        if dist_t < temp_station_dist:
            temp_station_dist=dist_t
            closest_temp_station=row["station_id"]
    data["temperature"].loc[runtimes.index(runtime)]=temp_temperature[temp_temperature["station_id"]==closest_temp_station].reading.item()

    for index,row in temp_humidity.iterrows():
        dist_h=hs.haversine(g.latlng,(row["latitude"],row["longitude"]))
        if dist_h < hum_station_dist:
            hum_station_dist=dist_h
            closest_hum_station=row["station_id"]
    data["humidity"].loc[runtimes.index(runtime)]=temp_humidity[temp_humidity["station_id"]==closest_hum_station].reading.item()

    for index,row in temp_windspeed.iterrows():
        dist_ws=hs.haversine(g.latlng,(row["latitude"],row["longitude"]))
        if dist_ws < windsp_station_dist:
            windsp_station_dist=dist_ws
            closest_windsp_station=row["station_id"]
    data["windspeed"].loc[runtimes.index(runtime)]=temp_windspeed[temp_windspeed["station_id"]==closest_windsp_station].reading.item()

    for index,row in temp_winddir.iterrows():
        dist_wd=hs.haversine(g.latlng,(row["latitude"],row["longitude"]))
        if dist_wd < winddir_station_dist:
            winddir_station_dist=dist_wd
            closest_winddir_station=row["station_id"]
    data["winddirection"].loc[runtimes.index(runtime)]=temp_winddir[temp_winddir["station_id"]==closest_winddir_station].direction.item()
#data.to_csv("weatherdata.csv",index=False)

final_data=data.set_index('timestamp')
final_data=final_data.drop(final_data[final_data.winddirection==0].index)
#final_data.to_csv("weatherdata_final.csv",index=False)

