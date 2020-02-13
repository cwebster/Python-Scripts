# -*- coding: utf-8 -*- s
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

pio.renderers.default = "browser"


# Import files
hgs_file = r"hgs_k.csv"
qe_file = r"qe_k.csv"
hgs_gps_file = r"mnumbers.csv"
qe_gps_file = r"gnumbers.csv"

df_qe = pd.read_csv(qe_file, na_values=['.'], sep=";", engine='python')
df_hgs = pd.read_csv(hgs_file, na_values=['.'], sep=";", engine='python')
hgs_gps = pd.read_csv(hgs_gps_file, na_values=['.'], sep=";", engine='python')
qe_gps = pd.read_csv(qe_gps_file, na_values=['.'], sep=";", engine='python')

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

df_hgs_gps = df_hgs[df_hgs.LOC.isin(list(hgs_gps.MNumbers))]
df_qe_gps = df_qe[df_qe.LOC.isin(list(qe_gps.GNumbers))]


by_date_location_hgs = df_hgs_gps.groupby(["LOC", "FDR"])
by_date_location_qe = df_qe_gps.groupby(["LOC", "FDR"])

df = by_date_location_hgs.K.value_counts(normalize=True, dropna=False)
df_val_counts = pd.DataFrame(df)
df = pd.Dataframe(df_val_counts)
df.index.name = 'LOC'
df.columns = ['freq']

df.loc['M92035']

# Gives Potassium by Location and Date
by_date_location_hgs.K.value_counts(normalize=True)
by_date_location_qe.K.value_counts(normalize=True)
