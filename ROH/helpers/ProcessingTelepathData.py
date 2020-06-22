# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 15:35:39 2020

@author: cgwr
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def ProcessTelepathData(df):
  #remove SI sets
  df = df[df.Set_Code != 'SI']
  
  #calculate the time differences in hours
  df.Date_Time_Received = pd.to_datetime(df.Date_Time_Received)
  df.Date_Time_Authorised = pd.to_datetime(df.Date_Time_Authorised)
  df.Date_Time_Booked_In = pd.to_datetime(df.Date_Time_Booked_In) 
  df.Date_Time_Collected = pd.to_datetime(df.Date_Time_Collected)
  df['TAT_Received'] = (df.Date_Time_Authorised - df.Date_Time_Received).astype('timedelta64[m]')
  df['TAT_Collected'] = (df.Date_Time_Authorised - df.Date_Time_Collected).astype('timedelta64[m]')
  df['TAT_Reception'] = (df.Date_Time_Booked_In - df.Date_Time_Collected).astype('timedelta64[m]')
  df['TAT_Transport'] = (df.Date_Time_Received - df.Date_Time_Collected).astype('timedelta64[m]')
  
  return (df)

