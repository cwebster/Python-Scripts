# -*- coding: utf-8 -*-
"""
GRFIT
Created on Tue Dec 24 12:23:52 2019

@author: webstec
"""
import pandas as pd

import jaydebeapi

driver_location = "/Users/webstec/Documents/2018.1/cache-jdbc-2.0.0.jar"

# Connect to datasource
conn = jaydebeapi.connect("com.intersys.jdbc.CacheDriver", "jdbc:Cache://192.168.156.168:1972/SQH", ["tpathhrt", "tpathhrt"], driver_location,) 
curs = conn.cursor()

# Open and read the file as a single buffer
fd = open('/Users/webstec/SQL-Scripts/ed_query.sql', 'r')
sql = fd.read()
fd.close()

# Create dataframe from results
data = pd.read_sql_query(sql, conn)

# percentile list 
perc =[.5, .25, .75, .95] 

desc = data.describe(percentiles = perc) 

data.Date_Time_Received = pd.to_datetime(data.Date_Time_Received)
data.Date_Time_Authorised = pd.to_datetime(data.Date_Time_Authorised)
data.Date_Time_Booked_In = pd.to_datetime(data.Date_Time_Booked_In)
data.Date_Time_Collected = pd.to_datetime(data.Date_Time_Collected)

data['TAT_Received'] = (data.Date_Time_Authorised - data.Date_Time_Received).astype('timedelta64[m]')
data['TAT_Collected'] = (data.Date_Time_Authorised - data.Date_Time_Collected).astype('timedelta64[m]')
data['TAT_Reception'] = (data.Date_Time_Booked_In - data.Date_Time_Collected).astype('timedelta64[m]')
data['TAT_Transport'] = (data.Date_Time_Received - data.Date_Time_Collected).astype('timedelta64[m]')

x = data.groupby('Date_Received')


# Create excel spreadsheets
#df_qe.to_excel("C:/Users/Public/NHSI/grift_qe.xlsx")
#df_hgs.to_excel(curs.execute(sql)"/Users/webstec/CloudStation/Turnaround Times/grift_hgs.xlsx")