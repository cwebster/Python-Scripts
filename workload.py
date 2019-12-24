# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 11:57:44 2019

@author: cgwr
"""

import pyodbc
import pandas as pd
import numpy as np
import ast
import json

import seaborn as sns
sns.set(style="ticks", palette="pastel")


# Connect to datasource
conn=pyodbc.connect('DSN=QE Telepath', autocommit=True)

# Open and read the file as a single buffer
fd = open('C:/Users/Public/SQL-Scripts/Select-Test-hrsin-last-7-days.sql', 'r')
sql = fd.read()
fd.close()

# Create dataframe from results
df = pd.read_sql(sql, conn)



sns.boxplot(x=df.Date_Received, y=df.HrsIn, palette=["m", "g"],
            data=np.mean(ast.literal_eval(df.HrsIn)))
sns.despine(offset=10, trim=True)