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

# Gives Potassium by Location and Date
by_date_location_hgs.K.value_counts(normalize=True)
by_date_location_qe.K.value_counts(normalize=True)


df = by_date_location_hgs.K.value_counts(normalize=True)
x = df.iloc[df.index.get_level_values('LOC') == 'M81062']

# Flattens the DF into another DF with no Multiindex
df_grouped_hgs = df_hgs.groupby(["FDR", "LOC"], as_index=False)['K'].describe()

# For descriptive statistics
df_grouped_hgs = df_hgs.groupby(["FDR", "LOC"])['NewK'].describe()


# Flatten into dataframe
df_grouped_hgs = df_grouped_hgs.stack().reset_index()
df_grouped_hgs = df_grouped_hgs.rename(columns={0: 'Calc'})

# How to search for data
# df_grouped_hgs[(df_grouped_hgs.level_2== 'mean') &
# (df_grouped_hgs.LOC == 'WW2')]


# Get locations for HGS and QE
keys_hgs = df_hgs.LOC.unique()
keys_qe = df_qe.LOC.unique()

# find where we can do stats
df_hgs_grouped_stats = df_grouped_hgs[(df_grouped_hgs['count'] >20)]
fig = px.scatter(df_hgs_grouped_stats, x=df_hgs_grouped_stats.index.get_level_values(0), y = 'mean')


fig = go.Figure(data=go.Scatter(
        x=df_hgs_grouped_stats.index.get_level_values(0),
        y=df_hgs_grouped_stats['mean'],
        error_y=dict(
            type='percent', # value of error bar given as percentage of y value
            value=50,
            visible=True)
    ))



fig = go.Figure()

fig.add_trace(go.Line(
    y = df_grouped_hgs.loc[df_grouped_hgs.index.get_level_values('LOC') == location]['mean'].values,
    x= df_grouped_hgs.index.get_level_values(0).unique(),
    name = location))


fig = px.scatter(df_grouped_hgs, x=df_grouped_hgs.index.get_level_values(0).unique(), y=df_grouped_hgs.loc[df_grouped_hgs.index.get_level_values('LOC') == location]['mean'].values, color="species", error_x="e", error_y="e")

fig = go.Figure()

for dr in df_hgs.FDR.unique():
       fig.add_trace(go.Box(y=df_hgs[(df_hgs.FDR == dr)]['NewK'], name = str(dr)))


with open("/tmp/foo.html", "w") as file:
    for location in keys_hgs:
        file.write(f'<div>{location!r}</div>')
        file.write('<div><img src="data:image/png;base64,{}"/></div>'.format(sparklines(location)))


def sparklines(location):
    data = df_grouped_hgs.loc[df_grouped_hgs.index.get_level_values('LOC') == location]['mean']
    print(f"Done for {location!r}")
    return sparkline(data)


def sparkline(data, figsize=(4, 0.25), **kwags):
    """
    Returns a HTML image tag containing a base64 encoded sparkline style plot
    """
    data = list(data)

    fig, ax = plt.subplots(1, 1, figsize=figsize, **kwags)
    ax.plot(data)
    for k, v in ax.spines.items():
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
