# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 13:36:12 2020

@author: cgwr
"""

import pyodbc
import pandas as pd
import helpers.ProcessingTelepathData as pt

# Connect to datasource
conn = pyodbc.connect('DSN=QE Telepath', autocommit=True)

# Open and read the file as a single buffer
fd = open('C:/Users/Public/SQL-Scripts/roh.sql', 'r')
sql = fd.read()
fd.close()

# Create dataframe from results
df_qe = pd.read_sql(sql, conn)

df = pt.ProcessTelepathData(df_qe)

#Set Some Targets
# In hours
turnaround_time_target = 12

# in minutes
reception_target = 15

# in minutes
travel_time_target = 15

# In percent
kpi_trigger = 98

#percentile for KPI
percentile_for_kpi = kpi_trigger / 100




