# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:50:39 2020

@author: cgwr
"""
from WebsterPlotting import WebsterPlotting

class WebsterBloodBankReporting(WebsterPlotting):
    def prepareTests(self):
         self.tests_total = self.processor.total_blood_bank.groupby('Test_Code')['Workload'].sum().to_frame().sort_values(by=['Workload']).nlargest(20, 'Workload')
         self.hgs_total = self.processor.total_blood_bank_hgs.groupby('Test_Code')['Workload'].sum().to_frame().sort_values(by=['Workload']).nlargest(20, 'Workload')
         self.qe_total = self.processor.total_blood_bank_qe.groupby('Test_Code')['Workload'].sum().to_frame().sort_values(by=['Workload']).nlargest(20, 'Workload')
            
         self.total_by_quarter = self.processor.total_blood_bank.groupby('Quarter')['Workload'].sum().to_frame()
         self.qe_total_by_quarter = self.processor.total_blood_bank_hgs.groupby('Quarter')['Workload'].sum().to_frame()
         self.hgs_total_by_quarter = self.processor.total_blood_bank_qe.groupby('Quarter')['Workload'].sum().to_frame()
         
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

        self.totals_subplot.update_layout(title_text="Data Analysis For Blood Bank")
        self.by_quarter_suplot.update_layout(title_text="Data Analysis by Quarter For Blood Bank")