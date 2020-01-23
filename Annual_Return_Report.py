# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:08:52 2020

@author: cgwr
"""

#Set up
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import webbrowser
import WebsterChemistryReporting as chem
import WebsterHaematologyReporting as haem

#chrome_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
#webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
pio.renderers.default = "chrome"

import annual_return as ar

hgs_file = input("\n Hello, user. "
    "\n \n Please type in the path to your HGS file and press 'Enter': ")

qe_file = input("\n Hello, user. "
    "\n \n Please type in the path to your QE file and press 'Enter': ")


#Create Data Processor and process data
processor = ar.AnnualReturnProcessingClass(qe_file_name = qe_file, hgs_file_name = hgs_file)
processor.readData()
processor.processData()

# Build Chemistry Charts and Tables
chemistry_reports = chem.WebsterChemistryReporting(processor)
chemistry_reports.prepareTests()
chemistry_reports.createPlots()

# Plots
chemistry_tests_plot = chemistry_reports.totals_subplot
chemistry_workload_by_quarter_subplot = chemistry_reports.by_quarter_suplot

chemistry_tests_plot
chemistry_workload_by_quarter_subplot


# Build Haematology Charts and Tables
haem_reports = haem.WebsterHaematologyReporting(processor)
haem_reports.prepareTests()
haem_reports.createPlots()


# Build Blood Bank


# all_tests = processor.total_tests_cleaned.groupby('Test_Code')['Workload'].sum()
# all_tests = all_tests.to_frame()
# all_tests = all_tests.sort_values(by=['Workload'])

# Datasets
# chemistry_tests_total = chemistry_reports.tests_total
# chemistry_tests_hgs_total = chemistry_reports.hgs_total
# chemistry_tests_qe_total = chemistry_reports.qe_total

# chemistry_tests_total_by_quarter = chemistry_reports.total_by_quarter
# chemistry_tests_hgs_total_by_quarter = chemistry_reports.hgs_total_by_quarter
# chemistry_tests_qe_total_by_quarter = chemistry_reports.qe_total_by_quarter

