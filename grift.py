# -*- coding: utf-8 -*-
"""
GRFIT
Created on Tue Dec 24 12:23:52 2019

@author: webstec
"""
import pyodbc
import pandas as pd

# Connect to datasource
conn=pyodbc.connect('DSN=QE Telepath', autocommit=True)
conn1=pyodbc.connect('DSN=Heartlands Telepath', autocommit=True)

# Open and read the file as a single buffer
fd = open('C:/Users/Public/SQL-Scripts/grift.sql', 'r')
sql = fd.read()
fd.close()

# Create dataframe from results
df_qe = pd.read_sql(sql, conn)
df_hgs = pd.read_sql(sql, conn1)

# Create excel spreadsheets
df_qe.to_excel("C:/Users/Public/NHSI/grift_qe.xlsx")
df_hgs.to_excel("C:/Users/Public/NHSI/grift_hgs.xlsx")