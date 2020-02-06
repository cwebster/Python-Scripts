# -*- coding: utf-8 -*-
"""
Potassium Analysis
Loads SQL File and creates a DF from both telepath systems

Created on Tue Dec 24 11:44:15 2019

@author: Craig Webster
"""

import pandas as pd
import plotly.io as pio
from plotly import graph_objs as go


import base64
import requests
import numpy as np
import pandas as pd
from time import sleep
from itertools import chain
from datetime import timedelta, date
from IPython.display import display, HTML

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

pio.renderers.default = "browser"

hgs_file = r"/Users/craigwebster/Python-Scripts/hgs_k.csv"

qe_file = r"/Users/craigwebster/Python-Scripts/qe_k.csv"


df_qe = pd.read_csv(qe_file, na_values=['.'], sep=";", engine='python')
df_hgs = pd.read_csv(hgs_file, na_values=['.'], sep=";", engine='python')

df_hgs['NewK'] = pd.to_numeric(df_hgs.K, errors='coerce')
df_qe['NewK'] = pd.to_numeric(df_qe.K, errors='coerce')

df_hgs.DTR = pd.to_datetime(df_hgs.DTR, errors='coerce')
df_qe.DTR = pd.to_datetime(df_qe.DTR, errors='coerce')
df_hgs.DTR = pd.to_datetime(df_hgs.DTR, errors='coerce')
df_qe.DTR = pd.to_datetime(df_qe.DTR, errors='coerce')

df_hgs.FDRPORT = pd.to_datetime(df_hgs.FDRPORT, errors='coerce')
df_qe.FDRPORT = pd.to_datetime(df_qe.FDRPORT, errors='coerce')

df_hgs.FDR = pd.to_datetime(df_hgs.FDR, errors='coerce')
df_qe.FDR = pd.to_datetime(df_qe.FDR, errors='coerce')

df_hgs.FDAUTH = pd.to_datetime(df_hgs.FDAUTH, errors='coerce')
df_qe.FDAUTH = pd.to_datetime(df_qe.FDAUTH, errors='coerce')
df_hgs = df_hgs.loc[:, ~df_hgs.columns.str.contains('^Unnamed')]
df_qe = df_qe.loc[:, ~df_qe.columns.str.contains('^Unnamed')]

hgs_statistics_by_day = df_hgs.groupby('FDR').describe()
qe_statistics_by_day = df_qe.groupby('FDR').describe()

# This groups by day
df_hgs.groupby(['FDR','K']).count()

# Get a DF of all K for day
web = df_hgs.groupby(['FDR','K']).count()


# Total number in day
web.query(' FDR == "2019-01-10"').sum().DTR

# Total non reportable in day
web.query(' FDR == "2019-01-10"').sum().NewK

fig = go.Figure()
for name, group in df_hgs.groupby(['FDR']):
    trace = go.Histogram()
    trace.name = name.strftime("%j")
    trace.x = group['K']
    fig.add_trace(trace)


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
    
    img = StringIO()
    plt.savefig(img)
    img.seek(0)
    plt.close()
    return '<img src="data:image/png;base64,{}"/>'.format(base64.b64encode(img.read()))