# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:14:12 2020

@author: cgwr
"""

import plotly.graph_objects as go

class WebsterCharting:

    def barChart(x_data, y_data, title):
        chart = go.Figure(
        data=[go.Bar(y=y_data, x = x_data)],
        layout_title_text=title)
        return chart
        
    def addSubBarPlot(figure, row, col, x_data, y_data, name):    
        figure.add_bar(x = x_data, y = y_data, name=name, row=row, col=col)
        return figure
