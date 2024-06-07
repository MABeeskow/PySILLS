#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# PySILLS.py
# Maximilian Beeskow
# 01.03.2021
# ----------------------
#
## MODULES
from modules import data
from modules import standard
from modules import sample
from modules import statistics
from modules import gui
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, Text
#
## IMPORT DATA
#
dataSRM = data.general()
CSTD = dataSRM.importSRM("../lib/NIST_610_Spandler.csv", ";", 0, 0)
#print("Test:\n", CSTD)
csdt = data.Data(filename="../lib/NIST_610_Spandler.csv")
cstdresults = csdt.import_data_to_pandas(delimiter=";", skip_header=None, skip_footer=0, names=["element", "concentration"])
#print(cstdresults)
dataInput = data.general()
IntensitiesData01 = dataInput.importData("../inputs/16nov14_a01.csv", ",", 3, 1)
#print(IntensitiesData01)
nRows = len(IntensitiesData01)
#print("Test (Intensities):\n", IntensitiesData01[1])
dataInput = data.general()
IntensitiesData02 = dataInput.importData("../inputs/16nov14_a02.csv", ",", 3, 1)
IntensitiesData03 = dataInput.importData("../inputs/16nov14_a03.csv", ",", 3, 1)
IntensitiesData04 = dataInput.importData("../inputs/16nov14_a04.csv", ",", 3, 1)
IntensitiesData05 = dataInput.importData("../inputs/16nov14_a05.csv", ",", 3, 1)
IntensitiesData06 = dataInput.importData("../inputs/16nov14_a06.csv", ",", 3, 1)
IntensitiesData07 = dataInput.importData("../inputs/16nov14_a07.csv", ",", 3, 1)
IntensitiesData08 = dataInput.importData("../inputs/16nov14_a08.csv", ",", 3, 1)
IntensitiesData09 = dataInput.importData("../inputs/16nov14_a09.csv", ",", 3, 1)
IntensitiesData10 = dataInput.importData("../inputs/16nov14_a10.csv", ",", 3, 1)
IntensitiesData11 = dataInput.importData("../inputs/16nov14_a11.csv", ",", 3, 1)
IntensitiesData12 = dataInput.importData("../inputs/16nov14_a12.csv", ",", 3, 1)
IntensitiesData13 = dataInput.importData("../inputs/16nov14_a13.csv", ",", 3, 1)
IntensitiesData14 = dataInput.importData("../inputs/16nov14_a14.csv", ",", 3, 1)
IntensitiesData15 = dataInput.importData("../inputs/16nov14_a15.csv", ",", 3, 1)
IntensitiesData16 = dataInput.importData("../inputs/16nov14_a16.csv", ",", 3, 1)
#
## SEGMENTATION
#
bg_time, sgn_time = data.Segmentation(IntensitiesData01).find_background()
bg_time_selected = data.Segmentation(IntensitiesData01).select_background(start_1=5.0, end_1=25.0, start_2=95.0, end_2=110.0)
sgn_time_selected = data.Segmentation(IntensitiesData01).select_signal(start=35.0, end=85.0)
dataSegmentation = data.segmentation(IntensitiesData01, False)
segments01, start01, end01 = dataSegmentation.segmentData()
print("Start 01:", start01, "End 01:", end01)
dataSegmentation = data.segmentation(IntensitiesData02, False)
segments02, start02, end02 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData03, False)
segments03, start03, end03 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData04, False)
segments04, start04, end04 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData05, False)
segments05, start05, end05 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData06, False)
segments06, start06, end06 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData07, False)
segments07, start07, end07 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData08, False)
segments08, start08, end08 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData09, False)
segments09, start09, end09 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData10, False)
segments10, start10, end10 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData11, False)
segments11, start11, end11 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData12, False)
segments12, start12, end12 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData13, False)
segments13, start13, end13 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData14, False)
segments14, start14, end14 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData15, False)
segments15, start15, end15 = dataSegmentation.segmentData()
dataSegmentation = data.segmentation(IntensitiesData16, False)
segments16, start16, end16 = dataSegmentation.segmentData()
#
## SENSITIVITIES STD
#
data = standard.standardAnalysis()
refData, xi01, Ccalc01, C_STD = data.calculateSensitivities(CSTD, IntensitiesData01, start01, end01, "Si", False)
refData, xi02, Ccalc02, C_STD = data.calculateSensitivities(CSTD, IntensitiesData02, start02, end02, "Si", False)
refData, xi15, Ccalc15, C_STD = data.calculateSensitivities(CSTD, IntensitiesData15, start15, end15, "Si", False)
refData, xi16, Ccalc16, C_STD = data.calculateSensitivities(CSTD, IntensitiesData16, start16, end16, "Si", False)
#
xi_01, isotope_list_01 = data.calculate_xi(IntensitiesData01, CSTD, "Si", start01, end01)
xi_02, isotope_list_02 = data.calculate_xi(IntensitiesData02, CSTD, "Si", start02, end02)
xi_15, isotope_list_15 = data.calculate_xi(IntensitiesData15, CSTD, "Si", start15, end15)
xi_16, isotope_list_16 = data.calculate_xi(IntensitiesData16, CSTD, "Si", start16, end16)
#
data = statistics.statisticalAnalysis([xi01, xi02, xi15, xi16])
analyzedSensitivities = data.analyzeSensitivities(reference="Si")
#
data = statistics.statisticalAnalysis([xi_01, xi_02, xi_15, xi_16])
xi_analyzed, df_xi = data.analyze_xi(reference="Si", isotopes=isotope_list_01)
#
## SAMPLE CONCENTRATIONS
#
exampleConcentration = 260774
data = sample.sampleAnalysis()
Csamp03, refData03 = data.calcConcentration(IntensitiesData03, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
C_sample_03, df_c_03 = data.calculate_concentrations(IntensitiesData03, xi=df_xi, start=start03, stop=end03, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_04, df_c_04 = data.calculate_concentrations(IntensitiesData04, xi=df_xi, start=start04, stop=end04, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_05, df_c_05 = data.calculate_concentrations(IntensitiesData05, xi=df_xi, start=start05, stop=end05, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_06, df_c_06 = data.calculate_concentrations(IntensitiesData06, xi=df_xi, start=start06, stop=end06, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_07, df_c_07 = data.calculate_concentrations(IntensitiesData07, xi=df_xi, start=start07, stop=end07, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_08, df_c_08 = data.calculate_concentrations(IntensitiesData08, xi=df_xi, start=start08, stop=end08, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_09, df_c_09 = data.calculate_concentrations(IntensitiesData09, xi=df_xi, start=start09, stop=end09, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_10, df_c_10 = data.calculate_concentrations(IntensitiesData10, xi=df_xi, start=start10, stop=end10, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_11, df_c_11 = data.calculate_concentrations(IntensitiesData11, xi=df_xi, start=start11, stop=end11, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_12, df_c_12 = data.calculate_concentrations(IntensitiesData12, xi=df_xi, start=start12, stop=end12, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_13, df_c_13 = data.calculate_concentrations(IntensitiesData13, xi=df_xi, start=start13, stop=end13, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
C_sample_14, df_c_14 = data.calculate_concentrations(IntensitiesData14, xi=df_xi, start=start14, stop=end14, C_ref=exampleConcentration, reference="Si", isotopes=isotope_list_01)
Csamp04, refData04 = data.calcConcentration(IntensitiesData04, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
Csamp05, refData05 = data.calcConcentration(IntensitiesData05, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
Csamp06, refData06 = data.calcConcentration(IntensitiesData06, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
Csamp07, refData07 = data.calcConcentration(IntensitiesData07, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
Csamp08, refData08 = data.calcConcentration(IntensitiesData08, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
Csamp09, refData09 = data.calcConcentration(IntensitiesData09, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
Csamp10, refData10 = data.calcConcentration(IntensitiesData10, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
Csamp11, refData11 = data.calcConcentration(IntensitiesData11, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
Csamp12, refData12 = data.calcConcentration(IntensitiesData12, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
Csamp13, refData13 = data.calcConcentration(IntensitiesData13, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
Csamp14, refData14 = data.calcConcentration(IntensitiesData14, exampleConcentration, analyzedSensitivities, start03, end03, "Si29", False)
#
#df_i, df_c = data.create_dataframe([IntensitiesData01, IntensitiesData02, IntensitiesData15, IntensitiesData16], [CSTD], isotope_list_01)
rsf_03, df_i_03, df_c_03 = data.calculate_rsf(IntensitiesData03, IntensitiesData01, C_sample_03, CSTD, "Si", isotope_list_01)
#
data = statistics.statisticalAnalysis([Csamp03, Csamp04, Csamp05, Csamp06, Csamp06, Csamp07, Csamp08, Csamp09, Csamp10, Csamp11, Csamp12, Csamp13, Csamp14])
analyzedConcentrations = data.analyzeConcentrations()
#
## RSF
data = sample.sampleAnalysis()
RSF03 = data.calcRSF([IntensitiesData01, IntensitiesData03], [C_STD, Csamp03], analyzedSensitivities, [start03, end03], "Si29")
#
## LOD
data = sample.sampleAnalysis()
#LOD3 = data.calculateLOD(RSF03, [IntensitiesData01, IntensitiesData03], C_STD, start03)
#