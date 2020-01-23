# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 08:15:44 2020

@author: cgwr
"""

import pandas as pd

class AnnualReturnProcessingClass:
    def __init__(self, hgs_file_name, qe_file_name):
        self.hgs_file_name = hgs_file_name
        self.qe_file_name = qe_file_name
        self.df_qe_annual = None # raw data import from QE data
        self.df_hgs_annual = None # raw data import from HGS data
        self.total = None # combined dataset
        # FBC set definition
        self.fbc_sets  = ['FBC', 'CBC']
        # Sets to exclude from data counts
        self.sets_to_exclude = ['FBC', 'CBC', 'SI', 'SIF', 'SIP', 'SIE']
        # Tests to exclude from data counts
        self.tests_to_exclude = ['SA1', 'FA1', 'SENT', 'EXP', 'EXP2', 'SPB', 
                                 'DATE', 'TIME', 'Result', 'TSTREQ', 'UVOL', 
                                 'PCOL1', 'UVOL1', 'PCOL1', 'DB', 'POC', 'TEL', 
                                 'COPY', 'DOSE', 'EQA', 'FREQ', 'GHH2', 'SAVE', 
                                 'SE', 'FINDT', 'OCELL', 'PHONE', 'PROBL', 
                                 'ERFLAG', 'DAT', 'MALKIT', 'BF', 'DCT']
        self.gos_sets = ['QFA','QGS','GS','AGS','IMM']
        self.anti_body_ident_sets = ['AG','AC','AE']
        self.issues_sets = ['QXM', 'QX', 'ISS', 'IS', 'RI']
        self.fbc_qe = None # QE FBC Data
        self.hgs_fbc = None # HGS FBC Data
        self.hgs_k = None # HGS potassium counts
        self.qe_k = None # QE potassium counts
        self.malaria = None
        self.malaria_hgs = None
        self.malaria_qe = None
        self.dat = None
        self.dat_hgs = None
        self.dat_qe = None
        self.lab_sections_chem = ['CHEM', 'SIL', 'ENDO', 'SAL', 'ROCH', 'CHMA', 
                                  'REF', 'SPEC', 'AUTO', 'CHM']
        self.lab_sections_haematology = ['HAEM','COAG','ANTI','LAB','HAE','HAEA']
        self.lab_sections_immunology = ['SER','NEU','ANTI','IMMA','IMM']
        self.total_tests_cleaned = None# total cleaned dataset
        self.total_tests_qe_cleaned = None# total cleaned dataset qe
        self.total_tests_hgs_cleaned = None# total cleaned dataset hgs
        self.total_chemistry = None# chemistry workload
        self.total_haematology = None# haematology workload
        self.total_chemistry_hgs = None# chemistry hgs
        self.total_chemistry_qe = None# chemistry qe
        self.total_haematology_hgs = None# haematology hgs
        self.total_haematology_qe = None# haematology qe
        self.total_immunology = None
        self.total_immunology_tests_counts = None
        
        self.total_blood_bank = None
        self.total_blood_bank_hgs = None
        self.total_blood_bank_qe = None
        
        self.total_chemistry_tests_count = None
        self.total_chemistry_hgs_count = None
        self.total_chemistry_qe_count = None
        
        self.total_haematology_tests_count = None
        self.total_haematology_hgs_count = None
        self.total_haematology_qe_count = None
        
        self.total_blood_bank_tests_count = None
        self.total_blood_bank_hgs_count = None
        self.total_blood_bank_qe_count = None
        
        self.gos = None
        self.gos_hgs = None
        self.go_qe = None
        
        self.anti_body_ident = None
        self.anti_body_ident_hgs = None
        self.anti_body_ident_qe = None
        
        self.issues = None
        self.issues_hgs = None
        self.issues_qe = None
        
        self.dct = None
        self.dct_hgs = None
        self.dct_qe = None
        
    def readData(self):
        self.df_qe_annual = pd.read_excel(self.qe_file_name,  sheet_name="Sheet1", keep_default_na=False, na_values=[""])
        self.df_hgs_annual = pd.read_excel(self.hgs_file_name,  sheet_name="Sheet1", keep_default_na=False, na_values=[""])
        
        #Combine QE and HGS data
        self.total = pd.concat([self.df_qe_annual, self.df_hgs_annual])
        
    def processData(self):
        #Produce QE and HGS data
        #remove sets
        self.total_tests_cleaned = self.removeSetsFromDf(self.total, self.sets_to_exclude)
        self.total_tests_qe_cleaned = self.removeSetsFromDf(self.df_qe_annual, self.sets_to_exclude)
        self.total_tests_hgs_cleaned = self.removeSetsFromDf(self.df_hgs_annual, self.sets_to_exclude)

        #remove tests from total dataset
        self.total_tests_cleaned =  self.removeTestsFromDf(self.total_tests_cleaned, self.tests_to_exclude)
        self.total_tests_qe_cleaned =  self.removeTestsFromDf(self.total_tests_qe_cleaned, self.tests_to_exclude)
        self.total_tests_hgs_cleaned =  self.removeTestsFromDf(self.total_tests_hgs_cleaned, self.tests_to_exclude)
                
        #extract potassium to check against GRIFT
        self.hgs_k = self.extractTest(self.df_hgs_annual, 'K')
        self.qe_k = self.extractTest(self.df_qe_annual, 'K')
        
        #Get FBC Data
        self.fbc_qe = self.extractSet(self.df_qe_annual, 'CBC')
        self.fbc_hgs = self.extractSet(self.df_hgs_annual, 'FBC')
        
        self.total_chemistry = self.processLabSection(self.total_tests_cleaned, self.lab_sections_chem)
        self.total_haematology = self.processLabSection(self.total_tests_cleaned, self.lab_sections_haematology)
        
        self.total_chemistry_hgs = self.processLabSection(self.total_tests_hgs_cleaned, self.lab_sections_chem)
        self.total_chemistry_qe = self.processLabSection(self.total_tests_qe_cleaned, self.lab_sections_chem)
        
        self.total_haematology_hgs = self.processLabSection(self.total_tests_hgs_cleaned, self.lab_sections_haematology)
        self.total_haematology_qe= self.processLabSection(self.total_tests_qe_cleaned, self.lab_sections_haematology)
        
        # Clean up haematology and count samples as per rules 
        self.malaria = self.extractTest(self.total, 'MALKIT')
        self.malaria_hgs = self.extractTest(self.df_hgs_annual, 'MALKIT')
        self.malaria_qe = self.extractTest(self.df_qe_annual, 'MALKIT')
        
        
        self.dat = self.extractTest(self.total, 'DAT') 
        self.dat_hgs = self.extractTest(self.df_hgs_annual, 'DAT') 
        self.dat_qe = self.extractTest(self.df_qe_annual, 'DAT') 
                
        #Immunology
        self.total_immunology = self.processLabSection(self.total_tests_cleaned, self.lab_sections_immunology)
        
        #Blood BanKs
        self.total_blood_bank = self.total_tests_cleaned[self.total_tests_cleaned.Disc == 'B']
        self.total_blood_bank_hgs = self.total_tests_hgs_cleaned[self.total_tests_hgs_cleaned.Disc == 'B']
        self.total_blood_bank_qe = self.total_tests_qe_cleaned[self.total_tests_qe_cleaned.Disc == 'B']
        
        # select and remove gos sets
        self.gos = self.extractSets(self.total, self.gos_sets)
        self.gos_hgs = self.extractSets(self.df_hgs_annual, self.gos_sets)
        self.gos_qe = self.extractSets(self.df_qe_annual, self.gos_sets)
        
        self.anti_body_ident = self.extractSets(self.total, self.anti_body_ident_sets)
        self.anti_body_ident_hgs = self.extractSets(self.df_hgs_annual, self.anti_body_ident_sets)
        self.anti_body_ident_qe = self.extractSets(self.df_qe_annual, self.anti_body_ident_sets)
        
        self.issues = self.extractSets(self.total, self.issues_sets)
        self.issues_hgs = self.extractSets(self.df_hgs_annual, self.issues_sets)
        self.issues_qe = self.extractSets(self.df_qe_annual, self.issues_sets)
        
        self.dct = self.extractTest(self.total, 'DCT')
        self.dct_hgs = self.extractTest(self.df_hgs_annual, 'DCT')
        self.dct_qe = self.extractTest(self.df_qe_annual, 'DCT')
        
        self.totalCounts()
        
    def totalCounts(self):
        self.total_chemistry_tests_count = self.total_chemistry['Workload'].sum()
        self.total_chemistry_hgs_count = self.total_chemistry_hgs['Workload'].sum()
        self.total_chemistry_qe_count = self.total_chemistry_qe['Workload'].sum()
        
        self.total_haematology_tests_count = self.total_haematology['Workload'].sum() + \
                                             self.malaria['Workload'].sum() + \
                                             self.fbc_hgs['Workload'].sum() + \
                                             self.fbc_qe['Workload'].sum() 
                                             
        self.total_haematology_hgs_count = self.total_haematology_hgs['Workload'].sum() + \
                                           self.malaria_hgs['Workload'].sum() + \
                                           self.fbc_hgs['Workload'].sum()
                                           
        self.total_haematology_qe_count = self.total_haematology_qe['Workload'].sum() + \
                                          self.malaria_qe['Workload'].sum() + \
                                          self.fbc_qe['Workload'].sum()
        
        self.total_blood_bank_tests_count = self.total_blood_bank['Workload'].sum() + \
                                            self.dat['Workload'].sum() + \
                                            self.dct['Workload'].sum() + \
                                            self.gos['Workload'].sum() + \
                                            self.anti_body_ident['Workload'].sum() + \
                                            self.issues['Workload'].sum()
                                            
        self.total_blood_bank_hgs_count = self.total_blood_bank_hgs['Workload'].sum() + \
                                          self.dat_hgs['Workload'].sum() + \
                                          self.dct_hgs['Workload'].sum() + \
                                          self.gos_hgs['Workload'].sum() + \
                                          self.anti_body_ident_hgs['Workload'].sum() + \
                                          self.issues_hgs['Workload'].sum()
                                          
        self.total_blood_bank_qe_count = self.total_blood_bank_qe['Workload'].sum() + \
                                         self.dat_qe['Workload'].sum() + \
                                         self.dct_qe['Workload'].sum() + \
                                         self.gos_qe['Workload'].sum() + \
                                         self.anti_body_ident_qe['Workload'].sum() + \
                                         self.issues_qe['Workload'].sum()
                                         
        self.total_immunology_tests_counts = self.total_immunology['Workload'].sum()
         
    def extractSet(self, df, set_code):
        #Put Set into own data set
        return df[df.Set_Code == set_code]
    
    def extractSets(self, df, set_codes):
        #Put Set into own data set
        return df[df.Set_Code.isin(set_codes)]
    
    def extractTest(self, df, test_code):
        #Put Set into own data set
        return df[df.Test_Code == test_code]
    
    def removeSetsFromDf(self, df, sets_to_exclude):
        df = df[~df.Set_Code.isin(sets_to_exclude)]
        return df
    
    def removeTestsFromDf(self, df, tests_to_exclude):
        return df[~df.Test_Code.isin(tests_to_exclude)]
    
    def processLabSection(self, df, lab_sections):
        return df[df['Lab_Section'].isin(lab_sections)]