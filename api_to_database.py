# import relevant libraries
import pandas as pd
import requests
import os
import pymysql
import time
from datetime import datetime
import numpy as np

# set the directory
os.chdir("YOUR FILE DIRECTORY")
os.getcwd()

#connect to sql database
_CONN = pymysql.connect(host='localhost',
                            user='root',
                            password='********',
                            db='weather')
cursor = _CONN.cursor()

# initiate the sequence of runtimes as a list
# NEA's APIs take in runtimes of the format "%Y-%m-%dT%H:%M:%S+08:00" 
# e.g 2020-01-31T23:59:59+08:00s
runtimes=list(pd.date_range('2018-01-01T00:00:00Z',
                            '2020-12-31T23:59:59Z',
                            freq='60T').strftime('%Y-%m-%dT%H:%M:%S+08:00'))
for runtime in runtimes:
    print("Scrapping data for {}".format(runtime))
    params={"date_time":runtime}
    if runtimes.index(runtime)>0 and runtimes.index(runtime)%500==0:
        time.sleep(60)
    
    a=requests.get('https://api.data.gov.sg/v1/environment/air-temperature', params=params).json()
    b=requests.get('https://api.data.gov.sg/v1/environment/relative-humidity', params=params).json()
    c=requests.get('https://api.data.gov.sg/v1/environment/rainfall',params=params).json()
    d=requests.get('https://api.data.gov.sg/v1/environment/wind-speed', params=params).json()
    e=requests.get('https://api.data.gov.sg/v1/environment/wind-direction', params=params).json()

    temperature=pd.DataFrame(columns=["timestamp","station_id","latitude","longitude","reading"])
    humidity=pd.DataFrame(columns=["timestamp","station_id","latitude","longitude","reading"])
    rainfall=pd.DataFrame(columns=["timestamp","station_id","latitude","longitude","reading"])
    windspeed=pd.DataFrame(columns=["timestamp","station_id","latitude","longitude","reading"])
    winddir=pd.DataFrame(columns=["timestamp","station_id","latitude","longitude","reading"])
    
    try:    
        for w in range(0,len(a["items"][0]["readings"])):
            if "value" not in a["items"][0]["readings"][w]:
                continue            
            temperature=temperature.append({"timestamp":datetime.strptime(a["items"][0]["timestamp"],"%Y-%m-%dT%H:%M:%S+08:00"),
                         "station_id":a["items"][0]["readings"][w]["station_id"],
                         "latitude":a["metadata"]["stations"][w]["location"]["latitude"],
                         "longitude":a["metadata"]["stations"][w]["location"]["longitude"],
                         "reading":a["items"][0]["readings"][w]["value"]},ignore_index=True)
        for x in range(0,len(b["items"][0]["readings"])):
            if "value" not in b["items"][0]["readings"][w]:
                continue            
            humidity=humidity.append({"timestamp":datetime.strptime(b["items"][0]["timestamp"],"%Y-%m-%dT%H:%M:%S+08:00"),
                         "station_id":b["items"][0]["readings"][x]["station_id"],
                         "latitude":b["metadata"]["stations"][x]["location"]["latitude"],
                         "longitude":b["metadata"]["stations"][x]["location"]["longitude"],
                         "reading":b["items"][0]["readings"][x]["value"]},ignore_index=True)
        for y in range(0,len(c["items"][0]["readings"])):
            if "value" not in c["items"][0]["readings"][w]:
                continue                        
            rainfall=rainfall.append({"timestamp":datetime.strptime(c["items"][0]["timestamp"],"%Y-%m-%dT%H:%M:%S+08:00"),
                         "station_id":c["items"][0]["readings"][y]["station_id"],
                         "latitude":c["metadata"]["stations"][y]["location"]["latitude"],
                         "longitude":c["metadata"]["stations"][y]["location"]["longitude"],
                         "reading":c["items"][0]["readings"][y]["value"]},ignore_index=True)        
        for z in range(0,len(d["items"][0]["readings"])):
            if "value" not in d["items"][0]["readings"][z]:
                continue            
            windspeed=windspeed.append({"timestamp":datetime.strptime(d["items"][0]["timestamp"],"%Y-%m-%dT%H:%M:%S+08:00"),
                         "station_id":d["items"][0]["readings"][z]["station_id"],
                         "latitude":d["metadata"]["stations"][z]["location"]["latitude"],
                         "longitude":d["metadata"]["stations"][z]["location"]["longitude"],
                         "reading":d["items"][0]["readings"][z]["value"]},ignore_index=True)
        for v in range(0,len(e["items"][0]["readings"])):
            if "value" not in e["items"][0]["readings"][v]:
                continue
            winddir=winddir.append({"timestamp":datetime.strptime(e["items"][0]["timestamp"],"%Y-%m-%dT%H:%M:%S+08:00"),
                         "station_id":e["items"][0]["readings"][v]["station_id"],
                         "latitude":e["metadata"]["stations"][v]["location"]["latitude"],
                         "longitude":e["metadata"]["stations"][v]["location"]["longitude"],
                         "reading":e["items"][0]["readings"][v]["value"]},ignore_index=True)
   
    except:
        temperature=temperature.append({"timestamp":datetime.strptime(runtime,"%Y-%m-%dT%H:%M:%S+08:00"),
                                        "station_id":"",
                                        "latitude":np.nan,
                                        "longitude":np.nan,
                                        "reading":np.nan},ignore=True)
        humidity=humidity.append({"timestamp":datetime.strptime(runtime,"%Y-%m-%dT%H:%M:%S+08:00"),
                                        "station_id":"",
                                        "latitude":np.nan,
                                        "longitude":np.nan,
                                        "reading":np.nan},ignore=True)
        rainfall=rainfall.append({"timestamp":datetime.strptime(runtime,"%Y-%m-%dT%H:%M:%S+08:00"),
                                        "station_id":"",
                                        "latitude":np.nan,
                                        "longitude":np.nan,
                                        "reading":np.nan},ignore=True)
        windspeed=windspeed.append({"timestamp":datetime.strptime(runtime,"%Y-%m-%dT%H:%M:%S+08:00"),
                                        "station_id":"",
                                        "latitude":np.nan,
                                        "longitude":np.nan,
                                        "reading":np.nan},ignore=True)
        winddir=winddir.append({"timestamp":datetime.strptime(runtime,"%Y-%m-%dT%H:%M:%S+08:00"),
                                        "station_id":"",
                                        "latitude":np.nan,
                                        "longitude":np.nan,
                                        "reading":np.nan},ignore=True)
        
    for index,row in temperature.iterrows():
        cursor.execute("INSERT INTO temperature(timestamp,station_id,latitude,longitude,reading)VALUES(%s,%s,%s,%s,%s)",
                       (row["timestamp"],row["station_id"],row["latitude"],row["longitude"],row["reading"]))
        _CONN.commit()
    for index,row in humidity.iterrows():
        cursor.execute("INSERT INTO humidity(timestamp,station_id,latitude,longitude,reading)VALUES(%s,%s,%s,%s,%s)",
                       (row["timestamp"],row["station_id"],row["latitude"],row["longitude"],row["reading"]))
        _CONN.commit()
    for index,row in rainfall.iterrows():
        cursor.execute("INSERT INTO rainfall(timestamp,station_id,latitude,longitude,reading)VALUES(%s,%s,%s,%s,%s)",
                       (row["timestamp"],row["station_id"],row["latitude"],row["longitude"],row["reading"]))
        _CONN.commit()
    for index,row in windspeed.iterrows():
        cursor.execute("INSERT INTO windspeed(timestamp,station_id,latitude,longitude,reading)VALUES(%s,%s,%s,%s,%s)",
                       (row["timestamp"],row["station_id"],row["latitude"],row["longitude"],row["reading"]))
        _CONN.commit()
    for index,row in winddir.iterrows():
        cursor.execute("INSERT INTO winddirection(timestamp,station_id,latitude,longitude,reading)VALUES(%s,%s,%s,%s,%s)",
                       (row["timestamp"],row["station_id"],row["latitude"],row["longitude"],row["reading"]))
        _CONN.commit()