import os
import pandas as pd
import sqlite3 as sql
import time
import wget

def get_flights(year, month):
    urltext = series + '_%d_%d' %(year, month)
    flighturl = url + 'PREZIP/' + urltext + '.zip'
    datapath = '/home/pohalloran/git/airline-delays/data/'

    # Temporarily download and store a given year and month of data
    filename = wget.download(flighturl)
    os.system('unzip ./' + filename + ' -d ' + datapath)
    os.system('rm ' + filename)
    os.system('rm ' + datapath + 'readme.html')

    # Select columns and insert into SQL db
    df = pd.read_csv(datapath + urltext + '.csv', dtype={'UniqueCarrier':str})
    flightdf = pd.DataFrame({
        'Year':df.Year,
        'Quarter':df.Quarter,
        'Month':df.Month,
        'DayOfWeek':df.DayOfWeek, 
        'Date':df.FlightDate, 
        'Carrier':df.UniqueCarrier,
        'AirlineID':df.AirlineID,
        'FlightNum':df.FlightNum,
        'Origin':df.Origin,
        'OriginState':df.OriginState,
        'Dest':df.Dest, 
        'DestState':df.DestState,
        'SchDep':df.CRSDepTime, 
        'DepTime':df.DepTime, 
        'DepDelay':df.DepDelay,
        'DepDel15':df.DepDel15,
        'Cancelled':df.Cancelled,
        'SchArr':df.CRSArrTime, 
        'ArrTime':df.ArrTime, 
        'ArrDelay':df.ArrDelay,
        'ArrDel15':df.ArrDel15,
        'Diverted':df.Diverted,
        'SchTime':df.CRSElapsedTime, 
        'ActualTime':df.ActualElapsedTime,
        'Flights':df.Flights,
        'Distance':df.Distance})
    flightdf.to_sql('flights', con, flavor='sqlite', schema=None, 
             if_exists='append', index=True, index_label=None,
             chunksize=None, dtype=None)
    os.system('rm ' + datapath + '*.csv')

## set up scraping vars
url = 'http://tsdata.bts.gov/'
series = 'On_Time_On_Time_Performance'

## init SQL connection
db = './data/flights.db'
con = sql.connect(db)

## Extract and save data to SQL db
for year in range(1987,2017):
    if year==1987:
        for month in range(10,13):
            get_flights(year, month)
    elif year==2016:
        for month in range(1,7):
            get_flights(year, month)
    else:
        for month in range(1, 13):
            get_flights(year, month)
            time.sleep(60)

## Close SQL connection
con.close()

