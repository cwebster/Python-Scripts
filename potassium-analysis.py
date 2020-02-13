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

import PotassiumReportingFunctions
import WebsterMiscFunctions
from WebsterPlotting import sparkline

# Setup of envrionment
# Use 3 decimal places in output display
pd.set_option("display.precision", 3)

# Don't wrap repr(DataFrame) across additional lines
pd.set_option("display.expand_frame_repr", False)

# Set max rows displayed in output to 25
pd.set_option("display.max_rows", 25)

hgs_file = r"hgs_k.csv"
qe_file = r"qe_k.csv"

qe, hgs = PotassiumReportingFunctions.process_input(hgs_file, qe_file)

# Flattens the DF into another DF with no Multiindex
df_grouped_hgs = hgs.groupby(["LOC", "FDR"], as_index=False)['K'].describe()

# For descriptive statistics
df_grouped_hgs = qe.groupby(["FDR", "LOC"])['NewK'].describe()

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
    return WebsterPlotting.sparkline(data.Calc)
