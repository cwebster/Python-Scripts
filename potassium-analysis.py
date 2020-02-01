# -*- coding: utf-8 -*-
"""
Potassium Analysis
Loads SQL File and creates a DF from both telepath systems

Created on Tue Dec 24 11:44:15 2019

@author: Craig Webster
"""

import pandas as pd
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import webbrowser

hgs_file = r"hgs_k.csv"

qe_file = r"qe_k.csv"


df_qe = pd.read_csv(qe_file, na_values=['.'], sep=";", engine='python')
df_hgs = pd.read_csv(hgs_file, na_values=['.'], sep=";", engine='python')

df_hgs['NewK'] = pd.to_numeric(df_hgs.K, errors='coerce')
df_qe['NewK'] = pd.to_numeric(df_qe.K, errors='coerce')

df_hgs.DTR = pd.to_datetime(df_hgs.DTR, errors='coerce')
df_qe.DTR = pd.to_datetime(df_qe.DTR, errors='coerce')

df_hgs.FDRPORT = pd.to_datetime(df_hgs.FDRPORT, errors='coerce')
df_qe.FDRPORT = pd.to_datetime(df_qe.FDRPORT, errors='coerce')

df_hgs.FDR = pd.to_datetime(df_hgs.FDR, errors='coerce')
df_qe.FDR = pd.to_datetime(df_qe.FDR, errors='coerce')

df_hgs.FDAUTH = pd.to_datetime(df_hgs.FDAUTH, errors='coerce')
df_qe.FDAUTH = pd.to_datetime(df_qe.FDAUTH, errors='coerce')

