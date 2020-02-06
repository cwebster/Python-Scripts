# -*- coding: utf-8 -*-
"""
Potassium Analysis
Loads SQL File and creates a DF from both telepath systems

Created on Tue Dec 24 11:44:15 2019

@author: Craig Webster
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import webbrowser
from plotly.subplots import make_subplots


import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64
import numpy as np

from io import BytesIO


# Setup of envrionment
# Use 3 decimal places in output display
pd.set_option("display.precision", 3)

# Don't wrap repr(DataFrame) across additional lines
pd.set_option("display.expand_frame_repr", False)

# Set max rows displayed in output to 25
pd.set_option("display.max_rows", 25)


# Import files
hgs_file = r"hgs_k.csv"
qe_file = r"qe_k.csv"
df_qe = pd.read_csv(qe_file, na_values=['.'], sep=";", engine='python')
df_hgs = pd.read_csv(hgs_file, na_values=['.'], sep=";", engine='python')

# Clean up data
df_hgs['NewK'] = pd.to_numeric(df_hgs.K, errors='coerce')
df_qe['NewK'] = pd.to_numeric(df_qe.K, errors='coerce')

df_hgs.DTR = pd.to_datetime(df_hgs.DTR, errors='coerce')
df_qe.DTR = pd.to_datetime(df_qe.DTR, errors='coerce')

df_hgs.DTC = pd.to_datetime(df_hgs.DTC, errors='coerce')
df_qe.DTC = pd.to_datetime(df_qe.DTC, errors='coerce')

df_hgs.FDRPORT = pd.to_datetime(df_hgs.FDRPORT, errors='coerce')
df_qe.FDRPORT = pd.to_datetime(df_qe.FDRPORT, errors='coerce')

df_hgs.FDR = pd.to_datetime(df_hgs.FDR, errors='coerce')
df_qe.FDR = pd.to_datetime(df_qe.FDR, errors='coerce')

df_hgs.FDAUTH = pd.to_datetime(df_hgs.FDAUTH, errors='coerce')
df_qe.FDAUTH = pd.to_datetime(df_qe.FDAUTH, errors='coerce')

df_qe['TravelTime'] = (df_qe.DTR-df_qe.DTC).astype('timedelta64[h]')
df_hgs['TravelTime'] = (df_hgs.DTR-df_hgs.DTC).astype('timedelta64[h]')

df_qe['TravelTime'] = (df_qe.DTR-df_qe.DTC).astype('timedelta64[h]')
df_hgs['TravelTime'] = (df_hgs.DTR-df_hgs.DTC).astype('timedelta64[h]')


df_hgs.groupby(["FDR", "LOC"])['K'].count()

# Flattens the DF into another DF with no Multiindex
df_grouped_hgs = df_hgs.groupby(["FDR", "LOC"], as_index=False)['K'].describe()

# For descriptive statistics
df_grouped_hgs = df_hgs.groupby(["FDR", "LOC"])['NewK'].describe()




# Flatten into dataframe
df_grouped_hgs = df_grouped_hgs.stack().reset_index()
df_grouped_hgs = df_grouped_hgs.rename(columns={0: 'Calc'})
df_grouped_hgs[(df_grouped_hgs.level_2== 'mean') & (df_grouped_hgs.LOC == 'WW2')]

with open("/tmp/foo.html", "w") as file:
    for location in keys:
        file.write('<div>{location}</div>')
        file.write('<div><img src="data:image/png;base64,{}"/></div>'.format(sparklines(location)))

def sparklines(location):
    data = df_grouped_hgs[(df_grouped_hgs.level_2== 'mean') & (df_grouped_hgs.LOC == location)]
    print(f"Done for {location!r}")
    return sparkline(data.Calc)
    
    


def isnotreported(idx):
    return df.loc[idx].K == 'NA'

def missing_values_table(df):
        mis_val = df.isnull().sum()
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")
        return mis_val_table_ren_columns
    
def data_frames(df):
    for dateR, frame in df_grouped_hgs:
        print(f"First 2 entries for {dateR!r}")
        print("------------------------")
        print(frame.head(2), end="\n\n")
        
        

def sparkline(data, figsize=(4, 0.25), **kwags):
    """
    Returns a HTML image tag containing a base64 encoded sparkline style plot
    """
    data = list(data)
 
    fig, ax = plt.subplots(1, 1, figsize=figsize, **kwags)
    ax.plot(data)
    for k,v in ax.spines.items():
        v.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
 
    plt.plot(len(data) - 1, data[len(data) - 1], 'r.')
 
    ax.fill_between(range(len(data)), data, len(data)*[min(data)], alpha=0.1)
 
    img = BytesIO()
    plt.savefig(img, transparent=True, bbox_inches='tight')
    img.seek(0)
    plt.close()
 
    return base64.b64encode(img.read()).decode("UTF-8")