# -*- coding: utf-8 -*-
"""
Created on Wed May 20 13:12:13 2020

@author: cgwr
"""

# general outline
# load PIDs and dates from source file
# search through tpath for all lab results on that day
# if none try next n days until find record

import jaydebeapi

from jinjasql import JinjaSql
j = JinjaSql()

driver_location = "/Users/webstec/Documents/2018.1/cache-jdbc-2.0.0.jar"

# Connect to datasource
conn = jaydebeapi.connect("com.intersys.jdbc.CacheDriver", "jdbc:Cache://192.168.156.168:1972/SQH", ["tpathhrt", "tpathhrt"], driver_location,) 
curs = conn.cursor()

template = """
    select * , DATEADD('dd',-5, {{ date_of_sample }}) AS startD,
    DATEADD('dd',+5, {{ date_of_sample }}) AS endD
    from 
    iLabTP.Date_Received_Index
    where 
    Date_Received_Index.Date_Received BETWEEN DATEADD('dd',-5, {{ date_of_sample }})  AND DATEADD('dd',+5, {{ date_of_sample }}) AND
    Discipline = 'B' AND
    Registration_Number = {{ pid }}
    group by Specimen_Number
    order by Date_Received
"""
data = {
    "date_of_sample": '2020-04-01',
    "pid": "N160307"
}

query, bind_params = j.prepare_query(template, data)


