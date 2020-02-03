# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 10:57:12 2020

@author: cgwr
"""

import pyodbc
import pandas as pd

# Connect to datasource
conn=pyodbc.connect('DSN=QE Telepath', autocommit=True)

# Open and read the file as a single buffer
fd = open('C:/Users/Public/SQL-Scripts/correct_test_counts.sql', 'r')
sql = fd.read()
fd.close()

# Create dataframe from results
df = pd.read_sql(sql, conn)

# cache this file for future reference
df.to_excel(r'C:/Users/Public/NHSI/qe-2019-2020.xlsx')

