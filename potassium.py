# -*- coding: utf-8 -*-
"""
Potassium Analysis
Loads SQL File and creates a DF from both telepath systems

Created on Tue Dec 24 11:44:15 2019

@author: Craig Webster
"""
import pyodbc
import pandas as pd

# Connect to datasource
conn = pyodbc.connect('DSN=QE Telepath', autocommit=True)
conn1 = pyodbc.connect('DSN=Heartlands Telepath', autocommit=True)

# Open and read the file as a single buffer
fd = open('C:/Users/Public/SQL-Scripts/potassium.sql', 'r')
sql = fd.read()
fd.close()

# Create dataframe from results
df_qe = pd.read_sql(sql, conn)
df_hgs = pd.read_sql(sql, conn1)

# Create excel spreadsheets
df_qe.to_excel("C:/Users/Public/NHSI/potassium-apr-2019-jan-2020_qe-withspecnos.xlsx")
df_hgs.to_excel("C:/Users/Public/NHSI/potassium-apr-2019-jan-2020_hgs-withspecnos.xlsx")
