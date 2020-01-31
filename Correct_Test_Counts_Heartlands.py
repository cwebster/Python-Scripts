# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:39:52 2020

@author: cgwr
"""

import pyodbc
import pandas as pd

# Connect to datasource
conn=pyodbc.connect('DSN=Heartlands Telepath', autocommit=True)

# Open and read the file as a single buffer
fd = open('C:/Users/Public/SQL-Scripts/correct_test_counts.sql', 'r')
sql = fd.read()
fd.close()

# Create dataframe from results
df = pd.read_sql(sql, conn)

# cache this file for future reference
df.to_excel(r'C:/Users/Public/NHSI/heartlands-2019-20206.xlsx')