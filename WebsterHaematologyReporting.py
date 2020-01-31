# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:50:39 2020

@author: cgwr
"""
from WebsterPlotting import WebsterPlotting

class WebsterHaematologyReporting(WebsterPlotting):
    def prepareTests(self):
         self.tests_total = self.processor.total_haematology.groupby('Test_Code')['Workload'].sum().to_frame().sort_values(by=['Workload']).nlargest(20, 'Workload')
         self.hgs_total = self.processor.total_haematology_hgs.groupby('Test_Code')['Workload'].sum().to_frame().sort_values(by=['Workload']).nlargest(20, 'Workload')
         self.qe_total = self.processor.total_haematology_qe.groupby('Test_Code')['Workload'].sum().to_frame().sort_values(by=['Workload']).nlargest(20, 'Workload')
            
         self.total_by_quarter = self.processor.total_haematology.groupby('Quarter')['Workload'].sum().to_frame()
         self.qe_total_by_quarter = self.processor.total_haematology_qe.groupby('Quarter')['Workload'].sum().to_frame()
         self.hgs_total_by_quarter = self.processor.total_haematology_hgs.groupby('Quarter')['Workload'].sum().to_frame()
         
         self.createPlots()
         
         self.totals_subplot.update_layout(title_text="Data Analysis For Haematology")
         self.by_quarter_suplot.update_layout(title_text="Data Analysis by Quarter For Haematology")