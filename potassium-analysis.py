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
import PotassiumReportingFunctions as pr

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

df_hgs, df_qe = pr.process_input(hgs_file, qe_file)

hgs_gps = pd.read_csv(hgs_gps_file, na_values=['.'], sep=";", engine='python')
qe_gps = pd.read_csv(qe_gps_file, na_values=['.'], sep=";", engine='python')

df_hgs_gps = df_hgs[df_hgs.LOC.isin(list(hgs_gps.MNumbers))]
df_qe_gps = df_qe[df_qe.LOC.isin(list(qe_gps.GNumbers))]

by_date_location_hgs = df_hgs_gps.groupby(["LOC", "FDR"])
by_date_location_qe = df_qe_gps.groupby(["LOC", "FDR"])

df = by_date_location_hgs.K.value_counts(normalize=True, dropna=False)
df_val_counts = pd.DataFrame(df)
df = pd.DataFrame(df_val_counts)
df.index.name = 'LOC'
df.columns = ['freq']

df.loc['M92035']

# Gives, FDR, K, Freq
for index, row in df.loc['M83006'].iterrows():
  print(index[0], index[1], row['freq'])

df.loc['M83006'].index.get_level_values(0)
df.loc['M83006'].index.get_level_values(1)
df.loc['M83006'].freq.values
