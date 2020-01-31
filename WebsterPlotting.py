# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 14:01:10 2020

@author: cgwr
"""

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import WebsterUHBCharting as wc

class WebsterPlotting:
    def __init__(self, processor):
        self.processor = processor
        self.tests_total = None
        self.hgs_total = None
        self.qe_total = None
        self.total_by_quarter = None
        self.qe_total_by_quarter = None
        self.hgs_total_by_quarter = None
        self.totals_subplot = None
        self.by_quarter_suplot = None
        self.by_quarter_bars = None
    
    def createPlots(self):
        specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]]
    
        # Workload by test bar charts
        dataset = []
        total_data_set = {'x_data': self.tests_total.index.values, 
                          'y_data': self.tests_total.Workload.values,
                          'name': "Total Workload by Test",
                          'type' : "bar"}
        
        hgs_data_set = {'x_data': self.hgs_total.index.values, 
                        'y_data': self.hgs_total.Workload.values,
                        'name': "Total Workload by Test HGS",
                        'type' : "bar"}
        
        qe_data_set = {'x_data': self.qe_total.index.values, 
                       'y_data': self.qe_total.Workload.values,
                       'name': "Total Workload by Test QE",
                       'type' : "bar"}
         

        dataset.append(total_data_set)
        dataset.append(hgs_data_set)
        dataset.append(qe_data_set)

        self.totals_subplot = self.createTotalByTestPlots(dataset, specs)

# total workload tables
        total_data_set_by_q = {'x_data': self.total_by_quarter.index.values, 
                          'y_data': self.total_by_quarter.Workload.values,
                          'name': "Total Workload by Quarter",
                          'type' : "table"}
        
        hgs_data_set_by_q = {'x_data': self.hgs_total_by_quarter.index.values, 
                        'y_data': self.hgs_total_by_quarter.Workload.values,
                        'name': "Total Workload by Quarter HGS",
                        'type' : "table"}
        
        qe_data_set_by_q = {'x_data': self.qe_total_by_quarter.index.values, 
                       'y_data': self.qe_total_by_quarter.Workload.values,
                       'name': "Total Workload by Quarter QE",
                       'type' : "table"}

        dataset2 = []
        dataset2.append(total_data_set_by_q)
        dataset2.append(hgs_data_set_by_q)
        dataset2.append(qe_data_set_by_q)
        
        specs=[[{"type": "table"}, {"type": "table"}], [{"type": "table"}, {"type": "table"}], [{"type": "table"}, {"type": "table"}]]
        
        self.by_quarter_suplot = self.createTotalByTestPlots(dataset2, specs)

# Total Workload by Quarter bars
        total_data_set_by_q = {'x_data': self.total_by_quarter.index.values, 
                          'y_data': self.total_by_quarter.Workload.values,
                          'name': "Total Workload by Quarter",
                          'type' : "bar"}
        
        hgs_data_set_by_q = {'x_data': self.hgs_total_by_quarter.index.values, 
                        'y_data': self.hgs_total_by_quarter.Workload.values,
                        'name': "Total Workload by Quarter HGS",
                        'type' : "bar"}
        
        qe_data_set_by_q = {'x_data': self.qe_total_by_quarter.index.values, 
                       'y_data': self.qe_total_by_quarter.Workload.values,
                       'name': "Total Workload by Quarter QE",
                       'type' : "bar"}
        

        dataset3 = []
        dataset3.append(total_data_set_by_q)
        dataset3.append(hgs_data_set_by_q)
        dataset3.append(qe_data_set_by_q)

        specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]]
        
        self.by_quarter_bars = self.createTotalByTestPlots(dataset3, specs)
    
    def createTotalByTestPlots(self, x_y_data_list, specs):
        
        # x_y_data_list will be a list of dictionary elements with x data y data and title
        # specs will be a list of dictionary elements with chart layout
        number_of_rows = round(len(x_y_data_list) / 2)
        
        subplot_titles = []
        
        length = len(x_y_data_list) 
        
        for i in range(length): 
            subplot_titles.append(x_y_data_list[i]['name'])
        
        subplot = make_subplots(rows=number_of_rows + 1, 
                                       cols=2, 
                                       subplot_titles = subplot_titles,
                                       specs = specs)
        
        for i in range(length): 
            
            if (i % 2 == 0): #number is even -- insert code to execute here
                column = 1
                row = i + 1
            else: #number is odd -- insert code to execute here
                column = 2
                row = i
            
            if (x_y_data_list[i]['type'] == 'bar'):
                subplot = wc.WebsterCharting.addSubBarPlot(subplot,
                                                                  row = row,
                                                                  col = column,
                                                                  x_data = x_y_data_list[i]['x_data'], 
                                                                  y_data = x_y_data_list[i]['y_data'], 
                                                                  name = x_y_data_list[i]['name'])
            elif  (x_y_data_list[i]['type'] == 'table'):
                subplot = subplot.add_trace(
                    go.Table(
                            header=dict(values=["Test", "Workload"],
                                        fill_color='paleturquoise',
                                        align='left'),
                                        cells=dict(values=[x_y_data_list[i]['x_data'],
                                                           x_y_data_list[i]['y_data']],
                                        fill_color='lavender',
                                        align='left')), row = row, col = column
                            )
        return subplot