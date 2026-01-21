#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# sample.py
# Maximilian Beeskow
# 03.08.2021
# ----------------------
#
## MODULES
import numpy as np
import re, os
from modules import data
import matplotlib.colors as mplcol
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import tkinter as tk
import tkinter.filedialog as fd
#
## TOOLS
#
class sampleAnalysis:
    #
    def __init__(self):
        pass
    #
    def calcConcentration(self, intensities, concentrations, xi, start, end, reference, plots):
        self.intensities = intensities
        self.concentrations = concentrations
        self.xi = xi
        self.start = start
        self.end = end
        self.reference = reference
        self.plots = plots
        #
        I_SAMP = self.intensities
        C_SAMPref = self.concentrations
        xi = self.xi
        laserOn = self.start
        laserOff = self.start + self.end
        #
        referenceData = []
        for i in range(0, len(I_SAMP)):
            if self.reference == I_SAMP[i][0]:
                referenceData.append(I_SAMP[i][0])
                referenceData.append([])
                for j in range(laserOn, laserOff):
                    referenceData[1].append(I_SAMP[i][1][j])
                referenceData.append(C_SAMPref)
            else:
                pass
        #
        C_SAMP = []
        for i in range(1, len(I_SAMP)):
            C_SAMP.append([I_SAMP[i][0], []])
        for i in range(0, len(C_SAMP)):
            for j in range(0, len(I_SAMP)):
                if C_SAMP[i][0] == I_SAMP[j][0]:
                    for k in range(laserOn, laserOff):
                        C_SAMP[i][1].append((I_SAMP[j][1][k] * referenceData[2]) / (referenceData[1][k - laserOn] * xi[i][1]))
        #
        for i in range(0, len(C_SAMP)):
            C_SAMP[i].append([np.mean(C_SAMP[i][1]), np.std(C_SAMP[i][1], ddof=1)])
        #
        dataLinRegr = []
        for i in range(0, len(C_SAMP)):
            if len(C_SAMP[i][1]) < 1:
                dataLinRegr.append([C_SAMP[i][0], []])
            elif C_SAMP[i][0] == I_SAMP[i + 1][0]:
                result = [I_SAMP[i + 1][0], stats.linregress(C_SAMP[i][1], I_SAMP[i + 1][1][laserOn:laserOff])]
                dataLinRegr.append(result)
        #for i in range(0, len(dataLinRegr)):
        #    print(dataLinRegr[i])
        #
        if self.plots == True:
            plt.figure(figsize=(8, 4), dpi=150)
            dataC = []
            dataI = []
            for i in range(0, len(C_SAMP)):
                if len(C_SAMP[i][1]) > 0:
                    dataC.extend(C_SAMP[i][1])
                    dataI.extend(I_SAMP[i + 1][1][laserOn:laserOff])
                    plt.scatter(C_SAMP[i][1], I_SAMP[i + 1][1][laserOn:laserOff], s=2.5, label=I_SAMP[i + 1][0], alpha=1.0)
                else:
                    pass
            plt.xlim(10 ** 2, 10 ** 7)
            plt.ylim(10 ** 2, 1.5 * max(dataI))
            plt.xscale("log")
            plt.yscale("log")
            plt.grid(True)
            plt.rc('axes', axisbelow=True)
            plt.xlabel("Concentration (ppm)")
            plt.ylabel("Intensity (cps)")
            plt.legend(fontsize="x-small", bbox_to_anchor=(1.0, 1.0))
            plt.show()
            #
            dataY = []
            for i in range(0, len(C_SAMP)):
                    dataY.append([C_SAMP[i][0], [dataLinRegr[i][1][0]*X + dataLinRegr[i][1][1] for X in C_SAMP[i][1]]])
            #
            for i in range(0, len(dataY)):
                if len(dataY[i][1]) == 0:
                    pass
                else:
                    plt.figure()
                    plt.plot(C_SAMP[i][1], dataY[i][1], linewidth=2.5, linestyle="solid")
                    plt.scatter(C_SAMP[i][1], I_SAMP[i+1][1][laserOn:laserOff], label=I_SAMP[i+1][0], alpha=0.75)
                    plt.xlabel("Concentration (ppm)")
                    plt.ylabel("Intensity (cps)")
                    plt.grid(True)
                    plt.rc('axes', axisbelow=True)
                    plt.legend(loc="upper left")
                    plt.tight_layout()
                    plt.show()
        else:
            pass
        #
        return C_SAMP, referenceData
    #
    def calcRSF(self, intensities, concentrations, sensitivities, limits, reference):
        """
        Calculation of the 'relative sensitivity factor' (RSF).
        :param intensities: list/numpy-array of the intensitites --> [I(STD), I(SAMP)]
        :param concentrations: list/numpy-array of the concentrations --> [C(STD), C(SAMP)]
        :param sensitivities: list/numpy-array of the sensitivites
        :param limits: list/numpy-array of the signal's start and end point
        :param reference: string, reference element
        :return: RSF: list/numpy-array of the calculated RSF values
        """
        self.I_STD = intensities[0]
        self.I_SAMP = intensities[1]
        self.C_STD = concentrations[0]
        self.C_SAMP = concentrations[1]
        self.xi = sensitivities
        self.laserOn = limits[0]
        self.laserOff = limits[0] + limits[1]
        self.reference = reference
        #
        referenceData = [self.reference]  # [reference element, intensities, concentrations, sensitivities]
        for i in range(0, len(self.I_SAMP)):
            if self.I_SAMP[i][0] == self.reference:
                referenceData.append(self.I_SAMP[i][1][self.laserOn:self.laserOff])
        for i in range(0, len(self.C_SAMP)):
            if self.C_SAMP[i][0] == self.reference:
                referenceData.append(self.C_SAMP[i][1])
        for i in range(0, len(self.xi)):
            if self.xi[i][0] == self.reference:
                referenceData.append(self.xi[i][1])
            #referenceData.append(self.xi[i][1])
        #
        RSF = []
        for i in range(1, len(self.I_SAMP)):
            RSF.append([self.I_SAMP[i][0]])
        missing = []
        elementsCSTD = []
        for i in range(0, len(self.C_STD)):
            elementsCSTD.append(self.C_STD[i][0])
        I_SAMPedit = self.I_SAMP[1:len(self.I_SAMP)]
        I_STDedit = self.I_STD[1:len(self.I_STD)]
        for i in range(0, len(self.I_SAMP)):
            if self.I_SAMP[i][0] not in elementsCSTD:
                missing.append(self.I_SAMP[i][0])
        for i in range(0, len(RSF)):
            for j in range(0, len(self.C_STD)):
                if RSF[i][0] == self.xi[i][0] and RSF[i][0] not in missing and RSF[i][0] == self.C_STD[j][0]:
                    RSF[i].append(self.xi[i][1]*(self.C_STD[j][1]*np.mean(referenceData[1]))/(np.mean(I_STDedit[i][1][self.laserOn:self.laserOff])*np.mean(referenceData[2])))
            if RSF[i][0] in missing:
                RSF[i].append(0)
        #for i in range(0, len(RSF)):
        #    print(RSF[i])
        #
        return RSF
    #
    def calculateLOD(self, RSF, intensities, C_STD, start):
        self.RSF = RSF
        self.intensities = intensities
        self.C_STD = C_STD
        self.start = start
        I_STD = self.intensities[0]
        I_SAMP = self.intensities[1]
        #
        background = []
        LOD = []
        for i in range(1, len(I_SAMP)):
            background.append([I_SAMP[i][0], np.std(I_SAMP[i][1][0:self.start], ddof=1)])
            LOD.append([I_SAMP[i][0]])
            #
        missing = []
        elementsCSTD = []
        for i in range(0, len(self.C_STD)):
            elementsCSTD.append(self.C_STD[i][0])
        I_SAMPedit = I_SAMP[1:len(I_SAMP)]
        I_STDedit = I_STD[1:len(I_STD)]
        for i in range(0, len(I_SAMP)):
            if I_SAMP[i][0] not in elementsCSTD:
                missing.append(I_SAMP[i][0])
        print(self.C_STD)
        #
        for i in range(0, len(I_SAMP)):
            for j in range(0, len(self.C_STD)):
                if I_SAMP[i][0] == self.C_STD[j][0] and I_SAMP[i][0] not in missing:
                    LOD.append(3*background[i][1] * (1/(self.start) + 1/(self.start))**(0.5) * 1/(self.RSF) * self.C_STD[j][1]/np.mean(I_STD[i][1][0:self.start]))
            if I_SAMP[i][0] in missing:
                LOD.append(0)
        #
        print(("LOD", LOD))
        #
        return LOD
    #
    def calculate_concentrations(self, I, C_ref, reference, xi, start, stop, isotopes):
        self.I = np.array(I[1:])
        self.C_ref = C_ref
        self.reference = reference
        self.xi = xi
        self.start = start
        self.stop = start + stop
        self.isotopes = isotopes
        #
        counter = 0
        while counter < 1:
            for i in range(len(self.isotopes)):
                if self.I[i][0] == self.isotopes[i]:
                    counter += 1
                else:
                    counter += 0
                    break
        self.I_new = self.I[np.arange(len(self.I))!=counter]
        #
        data_raw = []
        for i in range(len(self.I_new)):
            keyword = re.search(r"([A-Za-z]+)(\d+)", self.I_new[i][0])
            data_raw.append(pd.Series(self.I_new[i][1][self.start:self.stop]))
            if self.reference == keyword.group(1):
                isotope_ref = keyword.group(0)
        df_intensity = pd.concat(data_raw, axis=1)
        df_intensity.columns = self.isotopes
        #
        self.I_vector = df_intensity.mean()/df_intensity[isotope_ref].mean()
        self.c = self.I_vector*self.C_ref/self.xi.mean()
        #
        data_raw = []
        for i in range(len(self.c)):
            data_raw.append(pd.Series(self.c[i]))
        df_concentration = pd.concat(data_raw, axis=1)
        df_concentration.columns = self.isotopes
        #
        return self.c, df_concentration
    #
    #
    def create_dataframe(self, intensities, concentrations, isotopes):
        self.intensities = intensities
        self.concentrations = concentrations
        self.isotopes = isotopes
        #
        self.c_std_new = []
        for i in range(0, len(self.c_std)):
            for j in range(len(self.isotopes)):
                keyword_std = re.search(r"(\D+)", self.c_std[i][0])
                keyword_isotopes = re.search(r"([A-Za-z]+)(\d+)", self.isotopes[j])
                if keyword_std.group(1) == keyword_isotopes.group(1):
                    self.c_std_new.append(c_std[i][1])
        #
        counter = 0
        while counter < 1:
            for i in range(len(self.isotopes)):
                if self.i_samp[i][0] == self.isotopes[i]:
                    counter += 1
                else:
                    counter += 0
                    break
        self.i_samp_new = self.i_samp[np.arange(len(self.i_samp))!=counter]
        self.i_std_new = self.i_std[np.arange(len(self.i_std))!=counter]
        #
        data_i_samp = []
        data_i_std = []
        data_c_samp = []
        data_c_std = []
        for i in range(len(self.i_samp_new)):
            keyword = re.search(r"([A-Za-z]+)(\d+)", self.i_samp_new[i][0])
            data_i_samp.append(pd.Series(np.mean(self.i_samp_new[i][1][self.start:self.stop])))
            data_i_std.append(pd.Series(np.mean(self.i_std_new[i][1][self.start:self.stop])))
            data_c_samp.append(pd.Series(np.mean(self.c_samp[i])))
            data_c_std.append(pd.Series(np.mean(self.c_std_new[i])))
            if self.reference == keyword.group(1):
                isotope_ref = keyword.group(0)
        df_i_std = pd.concat(data_i_std, axis=1)
        df_i_std.columns = self.isotopes
        df_i_std.rename({0: "I_STD"}, axis='index')
        df_i_samp = pd.concat(data_i_samp, axis=1)
        df_i_samp.columns = self.isotopes
        df_c_samp = pd.concat(data_c_samp, axis=1)
        df_c_samp.columns = self.isotopes
        df_c_std = pd.concat(data_c_std, axis=1)
        df_c_std.columns = self.isotopes
        frames_i = [df_i_std, df_i_samp]
        frames_c = [df_c_std, df_c_samp]
        df_i = pd.concat(frames_i)
        df_i.index = ["I_STD", "I_SAMP"]
        df_c = pd.concat(frames_c)
        df_c.index = ["C_STD", "C_SAMP"]
        #
        return df_i, df_c
    #
    def calculate_rsf(self, i_samp, i_std, c_samp, c_std, reference, isotopes):
        self.i_samp = np.array(i_samp[1:])
        self.c_samp = c_samp
        self.i_std = np.array(i_std[1:])
        self.c_std = c_std
        self.reference = reference
        self.isotopes = isotopes
        #
        self.c_std_new = []
        for i in range(0, len(self.c_std)):
            for j in range(len(self.isotopes)):
                keyword_std = re.search(r"(\D+)", self.c_std[i][0])
                keyword_isotopes = re.search(r"([A-Za-z]+)(\d+)", self.isotopes[j])
                if keyword_std.group(1) == keyword_isotopes.group(1):
                    self.c_std_new.append(c_std[i][1])
                if self.reference == keyword_isotopes.group(1):
                    isotope_ref = keyword_isotopes.group(0)
        #
        counter = 0
        while counter < 1:
            for i in range(len(self.isotopes)):
                if self.i_samp[i][0] == self.isotopes[i]:
                    counter += 1
                else:
                    counter += 0
                    break
        self.i_samp_new = self.i_samp[np.arange(len(self.i_samp))!=counter]
        self.i_std_new = self.i_std[np.arange(len(self.i_std))!=counter]
        #
        data_i_samp = []
        data_i_std = []
        data_c_samp = []
        data_c_std = []
        for i in range(len(self.i_samp_new)):
            keyword = re.search(r"([A-Za-z]+)(\d+)", self.i_samp_new[i][0])
            data_i_samp.append(pd.Series(np.mean(self.i_samp_new[i][1][self.start:self.stop])))
            data_i_std.append(pd.Series(np.mean(self.i_std_new[i][1][self.start:self.stop])))
            data_c_samp.append(pd.Series(np.mean(self.c_samp[i])))
            data_c_std.append(pd.Series(np.mean(self.c_std_new[i])))
            if self.reference == keyword.group(1):
                isotope_ref = keyword.group(0)
        df_i_std = pd.concat(data_i_std, axis=1)
        df_i_std.columns = self.isotopes
        df_i_std.rename({0: "I_STD"}, axis='index')
        df_i_samp = pd.concat(data_i_samp, axis=1)
        df_i_samp.columns = self.isotopes
        df_c_samp = pd.concat(data_c_samp, axis=1)
        df_c_samp.columns = self.isotopes
        df_c_std = pd.concat(data_c_std, axis=1)
        df_c_std.columns = self.isotopes
        frames_i = [df_i_std, df_i_samp]
        frames_c = [df_c_std, df_c_samp]
        df_i = pd.concat(frames_i)
        df_i.index = ["I_STD", "I_SAMP"]
        df_c = pd.concat(frames_c)
        df_c.index = ["C_STD", "C_SAMP"]
        #
        rsf = (df_c[isotope_ref]["C_STD"])/(df_c[isotope_ref]["C_SAMP"])*(df_i[isotope_ref]["I_SAMP"])/(df_i[isotope_ref]["I_STD"])
        #
        return rsf, df_i, df_c
#
class InternalStandard:
    #
    def __init__(self, parent, color_bg):
        self.parent = parent
        self.color_bg = color_bg
        self.color_fg = "black"
        #
        padx_value = 0
        pady_value = 0
        ipadx_value = 1
        ipady_value = 1
        #
        self.is_window = tk.Toplevel(self.parent)
        self.is_window.geometry("900x675")
        self.is_window.title("Internal Standards")
        #
        for x in range(11):
            tk.Grid.columnconfigure(self.is_window, x, weight=1)
        for y in range(27):
            tk.Grid.rowconfigure(self.is_window, y, weight=1)
        #
        self.is_window.grid_columnconfigure(0, minsize=150)
        self.is_window.grid_columnconfigure(1, minsize=170)
        for i in range(2, 10, 2):
            self.is_window.grid_columnconfigure(i, minsize=60)
        for i in range(3, 10, 2):
            self.is_window.grid_columnconfigure(i, minsize=80)
        self.is_window.grid_columnconfigure(10, minsize=20)
        for i in range(0, 2):
            self.is_window.grid_rowconfigure(i, minsize=35)
        self.is_window.grid_rowconfigure(2, minsize=15)
        for i in range(3, 26):
            self.is_window.grid_rowconfigure(i, minsize=25)
        self.is_window.grid_rowconfigure(26, minsize=15)
        #
        # Buttons
        btn_01 = tk.Button(self.is_window, text="Load IS file", fg=self.color_fg, bg=self.color_bg, command=self.open_csv_is)
        btn_01.grid(row=0, column=0, padx=padx_value, pady=pady_value,
                    ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        btn_02 = tk.Button(self.is_window, text="Set IS data", fg=self.color_fg, bg=self.color_bg)
        btn_02.grid(row=1, column=0, padx=padx_value, pady=pady_value,
                    ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        #
        # Labels PSE
        lbl_H = tk.Label(self.is_window, text="H")
        lbl_H.grid(row=3, column=2, sticky="nesw")
        lbl_He = tk.Label(self.is_window, text="He")
        lbl_He.grid(row=4, column=2, sticky="nesw")
        lbl_Li = tk.Label(self.is_window, text="Li")
        lbl_Li.grid(row=5, column=2, sticky="nesw")
        lbl_Be = tk.Label(self.is_window, text="Be")
        lbl_Be.grid(row=6, column=2, sticky="nesw")
        lbl_B = tk.Label(self.is_window, text="B")
        lbl_B.grid(row=7, column=2, sticky="nesw")
        lbl_C = tk.Label(self.is_window, text="C")
        lbl_C.grid(row=8, column=2, sticky="nesw")
        lbl_N = tk.Label(self.is_window, text="N")
        lbl_N.grid(row=9, column=2, sticky="nesw")
        lbl_O = tk.Label(self.is_window, text="O")
        lbl_O.grid(row=10, column=2, sticky="nesw")
        lbl_F = tk.Label(self.is_window, text="F")
        lbl_F.grid(row=11, column=2, sticky="nesw")
        lbl_Ne = tk.Label(self.is_window, text="Ne")
        lbl_Ne.grid(row=12, column=2, sticky="nesw")
        lbl_Na = tk.Label(self.is_window, text="Na")
        lbl_Na.grid(row=13, column=2, sticky="nesw")
        lbl_Mg = tk.Label(self.is_window, text="Mg")
        lbl_Mg.grid(row=14, column=2, sticky="nesw")
        lbl_Al = tk.Label(self.is_window, text="Al")
        lbl_Al.grid(row=15, column=2, sticky="nesw")
        lbl_Si = tk.Label(self.is_window, text="Si")
        lbl_Si.grid(row=16, column=2, sticky="nesw")
        lbl_P = tk.Label(self.is_window, text="P")
        lbl_P.grid(row=17, column=2, sticky="nesw")
        lbl_S = tk.Label(self.is_window, text="S")
        lbl_S.grid(row=18, column=2, sticky="nesw")
        lbl_Cl = tk.Label(self.is_window, text="Cl")
        lbl_Cl.grid(row=19, column=2, sticky="nesw")
        lbl_Ar = tk.Label(self.is_window, text="Ar")
        lbl_Ar.grid(row=20, column=2, sticky="nesw")
        lbl_K = tk.Label(self.is_window, text="K")
        lbl_K.grid(row=21, column=2, sticky="nesw")
        lbl_Ca = tk.Label(self.is_window, text="Ca")
        lbl_Ca.grid(row=22, column=2, sticky="nesw")
        lbl_Sc = tk.Label(self.is_window, text="Sc")
        lbl_Sc.grid(row=23, column=2, sticky="nesw")
        lbl_Ti = tk.Label(self.is_window, text="Ti")
        lbl_Ti.grid(row=24, column=2, sticky="nesw")
        lbl_V = tk.Label(self.is_window, text="V")
        lbl_V.grid(row=25, column=2, sticky="nesw")
        #
        lbl_Cr = tk.Label(self.is_window, text="Cr")
        lbl_Cr.grid(row=3, column=4, sticky="nesw")
        lbl_Mn = tk.Label(self.is_window, text="Mn")
        lbl_Mn.grid(row=4, column=4, sticky="nesw")
        lbl_Fe = tk.Label(self.is_window, text="Fe")
        lbl_Fe.grid(row=5, column=4, sticky="nesw")
        lbl_Co = tk.Label(self.is_window, text="Co")
        lbl_Co.grid(row=6, column=4, sticky="nesw")
        lbl_Ni = tk.Label(self.is_window, text="Ni")
        lbl_Ni.grid(row=7, column=4, sticky="nesw")
        lbl_Cu = tk.Label(self.is_window, text="Cz")
        lbl_Cu.grid(row=8, column=4, sticky="nesw")
        lbl_Zn = tk.Label(self.is_window, text="Zm")
        lbl_Zn.grid(row=9, column=4, sticky="nesw")
        lbl_Ga = tk.Label(self.is_window, text="Ga")
        lbl_Ga.grid(row=10, column=4, sticky="nesw")
        lbl_Ge = tk.Label(self.is_window, text="Ge")
        lbl_Ge.grid(row=11, column=4, sticky="nesw")
        lbl_As = tk.Label(self.is_window, text="As")
        lbl_As.grid(row=12, column=4, sticky="nesw")
        lbl_Se = tk.Label(self.is_window, text="Se")
        lbl_Se.grid(row=13, column=4, sticky="nesw")
        lbl_Br = tk.Label(self.is_window, text="Br")
        lbl_Br.grid(row=14, column=4, sticky="nesw")
        lbl_Kr = tk.Label(self.is_window, text="Kr")
        lbl_Kr.grid(row=15, column=4, sticky="nesw")
        lbl_Rb = tk.Label(self.is_window, text="Rb")
        lbl_Rb.grid(row=16, column=4, sticky="nesw")
        lbl_Sr = tk.Label(self.is_window, text="Sr")
        lbl_Sr.grid(row=17, column=4, sticky="nesw")
        lbl_Y = tk.Label(self.is_window, text="Y")
        lbl_Y.grid(row=18, column=4, sticky="nesw")
        lbl_Zr = tk.Label(self.is_window, text="Zr")
        lbl_Zr.grid(row=19, column=4, sticky="nesw")
        lbl_Nb = tk.Label(self.is_window, text="Nb")
        lbl_Nb.grid(row=20, column=4, sticky="nesw")
        lbl_Mo = tk.Label(self.is_window, text="Mo")
        lbl_Mo.grid(row=21, column=4, sticky="nesw")
        lbl_Tc = tk.Label(self.is_window, text="Tc")
        lbl_Tc.grid(row=22, column=4, sticky="nesw")
        lbl_Ru = tk.Label(self.is_window, text="Ru")
        lbl_Ru.grid(row=23, column=4, sticky="nesw")
        lbl_Rh = tk.Label(self.is_window, text="Rh")
        lbl_Rh.grid(row=24, column=4, sticky="nesw")
        lbl_Pd = tk.Label(self.is_window, text="Pd")
        lbl_Pd.grid(row=25, column=4, sticky="nesw")
        #
        lbl_Ag = tk.Label(self.is_window, text="Ag")
        lbl_Ag.grid(row=3, column=6, sticky="nesw")
        lbl_Cd = tk.Label(self.is_window, text="Cd")
        lbl_Cd.grid(row=4, column=6, sticky="nesw")
        lbl_In = tk.Label(self.is_window, text="In")
        lbl_In.grid(row=5, column=6, sticky="nesw")
        lbl_Sn = tk.Label(self.is_window, text="Sn")
        lbl_Sn.grid(row=6, column=6, sticky="nesw")
        lbl_Sb = tk.Label(self.is_window, text="Sb")
        lbl_Sb.grid(row=7, column=6, sticky="nesw")
        lbl_Te = tk.Label(self.is_window, text="Te")
        lbl_Te.grid(row=8, column=6, sticky="nesw")
        lbl_I = tk.Label(self.is_window, text="I")
        lbl_I.grid(row=9, column=6, sticky="nesw")
        lbl_Xe = tk.Label(self.is_window, text="Xe")
        lbl_Xe.grid(row=10, column=6, sticky="nesw")
        lbl_Cs = tk.Label(self.is_window, text="Cs")
        lbl_Cs.grid(row=11, column=6, sticky="nesw")
        lbl_Ba = tk.Label(self.is_window, text="Ba")
        lbl_Ba.grid(row=12, column=6, sticky="nesw")
        lbl_La = tk.Label(self.is_window, text="La")
        lbl_La.grid(row=13, column=6, sticky="nesw")
        lbl_Ce = tk.Label(self.is_window, text="Ce")
        lbl_Ce.grid(row=14, column=6, sticky="nesw")
        lbl_Pr = tk.Label(self.is_window, text="Pr")
        lbl_Pr.grid(row=15, column=6, sticky="nesw")
        lbl_Nd = tk.Label(self.is_window, text="Nd")
        lbl_Nd.grid(row=16, column=6, sticky="nesw")
        lbl_Pm = tk.Label(self.is_window, text="Pm")
        lbl_Pm.grid(row=17, column=6, sticky="nesw")
        lbl_Sm = tk.Label(self.is_window, text="Sm")
        lbl_Sm.grid(row=18, column=6, sticky="nesw")
        lbl_Eu = tk.Label(self.is_window, text="Eu")
        lbl_Eu.grid(row=19, column=6, sticky="nesw")
        lbl_Gd = tk.Label(self.is_window, text="Gd")
        lbl_Gd.grid(row=20, column=6, sticky="nesw")
        lbl_Tb = tk.Label(self.is_window, text="Tb")
        lbl_Tb.grid(row=21, column=6, sticky="nesw")
        lbl_Dy = tk.Label(self.is_window, text="Dy")
        lbl_Dy.grid(row=22, column=6, sticky="nesw")
        lbl_Ho = tk.Label(self.is_window, text="Ho")
        lbl_Ho.grid(row=23, column=6, sticky="nesw")
        lbl_Er = tk.Label(self.is_window, text="Er")
        lbl_Er.grid(row=24, column=6, sticky="nesw")
        lbl_Tm = tk.Label(self.is_window, text="Tm")
        lbl_Tm.grid(row=25, column=6, sticky="nesw")
        #
        lbl_Yb = tk.Label(self.is_window, text="Yb")
        lbl_Yb.grid(row=3, column=8, sticky="nesw")
        lbl_Lu = tk.Label(self.is_window, text="Lu")
        lbl_Lu.grid(row=4, column=8, sticky="nesw")
        lbl_Hf = tk.Label(self.is_window, text="Hf")
        lbl_Hf.grid(row=5, column=8, sticky="nesw")
        lbl_Ta = tk.Label(self.is_window, text="Ta")
        lbl_Ta.grid(row=6, column=8, sticky="nesw")
        lbl_W = tk.Label(self.is_window, text="W")
        lbl_W.grid(row=7, column=8, sticky="nesw")
        lbl_Re = tk.Label(self.is_window, text="Re")
        lbl_Re.grid(row=8, column=8, sticky="nesw")
        lbl_Os = tk.Label(self.is_window, text="Os")
        lbl_Os.grid(row=9, column=8, sticky="nesw")
        lbl_Ir = tk.Label(self.is_window, text="Ir")
        lbl_Ir.grid(row=10, column=8, sticky="nesw")
        lbl_Pt = tk.Label(self.is_window, text="Pt")
        lbl_Pt.grid(row=11, column=8, sticky="nesw")
        lbl_Au = tk.Label(self.is_window, text="Au")
        lbl_Au.grid(row=12, column=8, sticky="nesw")
        lbl_Hg = tk.Label(self.is_window, text="Hg")
        lbl_Hg.grid(row=13, column=8, sticky="nesw")
        lbl_Tl = tk.Label(self.is_window, text="Tl")
        lbl_Tl.grid(row=14, column=8, sticky="nesw")
        lbl_Pb = tk.Label(self.is_window, text="Pb")
        lbl_Pb.grid(row=15, column=8, sticky="nesw")
        lbl_Bi = tk.Label(self.is_window, text="Bi")
        lbl_Bi.grid(row=16, column=8, sticky="nesw")
        lbl_Po = tk.Label(self.is_window, text="Po")
        lbl_Po.grid(row=17, column=8, sticky="nesw")
        lbl_At = tk.Label(self.is_window, text="At")
        lbl_At.grid(row=18, column=8, sticky="nesw")
        lbl_Rn = tk.Label(self.is_window, text="Rn")
        lbl_Rn.grid(row=19, column=8, sticky="nesw")
        lbl_Fr = tk.Label(self.is_window, text="Fr")
        lbl_Fr.grid(row=20, column=8, sticky="nesw")
        lbl_Ra = tk.Label(self.is_window, text="Ra")
        lbl_Ra.grid(row=21, column=8, sticky="nesw")
        lbl_Ac = tk.Label(self.is_window, text="Ac")
        lbl_Ac.grid(row=22, column=8, sticky="nesw")
        lbl_Th = tk.Label(self.is_window, text="Th")
        lbl_Th.grid(row=23, column=8, sticky="nesw")
        lbl_Pa = tk.Label(self.is_window, text="Pa")
        lbl_Pa.grid(row=24, column=8, sticky="nesw")
        lbl_U = tk.Label(self.is_window, text="U")
        lbl_U.grid(row=25, column=8, sticky="nesw")
        #
        # Entries PSE
        self.is_H = tk.StringVar()
        self.entr_H = tk.Entry(self.is_window, textvariable=self.is_H)
        self.entr_H.grid(row=3, column=3, sticky="nesw")
        self.is_He = tk.StringVar()
        self.entr_He = tk.Entry(self.is_window, textvariable=self.is_He)
        self.entr_He.grid(row=4, column=3, sticky="nesw")
        self.is_Li = tk.StringVar()
        self.entr_Li = tk.Entry(self.is_window, textvariable=self.is_Li)
        self.entr_Li.grid(row=5, column=3, sticky="nesw")
        self.is_Be = tk.StringVar()
        self.entr_Be = tk.Entry(self.is_window, textvariable=self.is_Be)
        self.entr_Be.grid(row=6, column=3, sticky="nesw")
        self.is_B = tk.StringVar()
        self.entr_B = tk.Entry(self.is_window, textvariable=self.is_B)
        self.entr_B.grid(row=7, column=3, sticky="nesw")
        self.is_C = tk.StringVar()
        self.entr_C = tk.Entry(self.is_window, textvariable=self.is_C)
        self.entr_C.grid(row=8, column=3, sticky="nesw")
        self.is_N = tk.StringVar()
        self.entr_N = tk.Entry(self.is_window, textvariable=self.is_N)
        self.entr_N.grid(row=9, column=3, sticky="nesw")
        self.is_O = tk.StringVar()
        self.entr_O = tk.Entry(self.is_window, textvariable=self.is_O)
        self.entr_O.grid(row=10, column=3, sticky="nesw")
        self.is_F = tk.StringVar()
        self.entr_F = tk.Entry(self.is_window, textvariable=self.is_F)
        self.entr_F.grid(row=11, column=3, sticky="nesw")
        self.is_Ne = tk.StringVar()
        self.entr_Ne = tk.Entry(self.is_window, textvariable=self.is_Ne)
        self.entr_Ne.grid(row=12, column=3, sticky="nesw")
        self.is_Na = tk.StringVar()
        self.entr_Na = tk.Entry(self.is_window, textvariable=self.is_Na)
        self.entr_Na.grid(row=13, column=3, sticky="nesw")
        self.is_Mg = tk.StringVar()
        self.entr_Mg = tk.Entry(self.is_window, textvariable=self.is_Mg)
        self.entr_Mg.grid(row=14, column=3, sticky="nesw")
        self.is_Al = tk.StringVar()
        self.entr_Al = tk.Entry(self.is_window, textvariable=self.is_Al)
        self.entr_Al.grid(row=15, column=3, sticky="nesw")
        self.is_Si = tk.StringVar()
        self.entr_Si = tk.Entry(self.is_window, textvariable=self.is_Si)
        self.entr_Si.grid(row=16, column=3, sticky="nesw")
        self.is_P = tk.StringVar()
        self.entr_P = tk.Entry(self.is_window, textvariable=self.is_P)
        self.entr_P.grid(row=17, column=3, sticky="nesw")
        self.is_S = tk.StringVar()
        self.entr_S = tk.Entry(self.is_window, textvariable=self.is_S)
        self.entr_S.grid(row=18, column=3, sticky="nesw")
        self.is_Cl = tk.StringVar()
        self.entr_Cl = tk.Entry(self.is_window, textvariable=self.is_Cl)
        self.entr_Cl.grid(row=19, column=3, sticky="nesw")
        self.is_Ar = tk.StringVar()
        self.entr_Ar = tk.Entry(self.is_window, textvariable=self.is_Ar)
        self.entr_Ar.grid(row=20, column=3, sticky="nesw")
        self.is_K = tk.StringVar()
        self.entr_K = tk.Entry(self.is_window, textvariable=self.is_K)
        self.entr_K.grid(row=21, column=3, sticky="nesw")
        self.is_Ca = tk.StringVar()
        self.entr_Ca = tk.Entry(self.is_window, textvariable=self.is_Ca)
        self.entr_Ca.grid(row=22, column=3, sticky="nesw")
        self.is_Sc = tk.StringVar()
        self.entr_Sc = tk.Entry(self.is_window, textvariable=self.is_Sc)
        self.entr_Sc.grid(row=23, column=3, sticky="nesw")
        self.is_Ti = tk.StringVar()
        self.entr_Ti = tk.Entry(self.is_window, textvariable=self.is_Ti)
        self.entr_Ti.grid(row=24, column=3, sticky="nesw")
        self.is_V = tk.StringVar()
        self.entr_V = tk.Entry(self.is_window, textvariable=self.is_V)
        self.entr_V.grid(row=25, column=3, sticky="nesw")
        #
        self.is_Cr = tk.StringVar()
        self.entr_Cr = tk.Entry(self.is_window, textvariable=self.is_Cr)
        self.entr_Cr.grid(row=3, column=5, sticky="nesw")
        self.is_Mn = tk.StringVar()
        self.entr_Mn = tk.Entry(self.is_window, textvariable=self.is_Mn)
        self.entr_Mn.grid(row=4, column=5, sticky="nesw")
        self.is_Fe = tk.StringVar()
        self.entr_Fe = tk.Entry(self.is_window, textvariable=self.is_Fe)
        self.entr_Fe.grid(row=5, column=5, sticky="nesw")
        self.is_Co = tk.StringVar()
        self.entr_Co = tk.Entry(self.is_window, textvariable=self.is_Co)
        self.entr_Co.grid(row=6, column=5, sticky="nesw")
        self.is_Ni = tk.StringVar()
        self.entr_Ni = tk.Entry(self.is_window, textvariable=self.is_Ni)
        self.entr_Ni.grid(row=7, column=5, sticky="nesw")
        self.is_Cu = tk.StringVar()
        self.entr_Cu = tk.Entry(self.is_window, textvariable=self.is_Cu)
        self.entr_Cu.grid(row=8, column=5, sticky="nesw")
        self.is_Zn = tk.StringVar()
        self.entr_Zn = tk.Entry(self.is_window, textvariable=self.is_Zn)
        self.entr_Zn.grid(row=9, column=5, sticky="nesw")
        self.is_Ga = tk.StringVar()
        self.entr_Ga = tk.Entry(self.is_window, textvariable=self.is_Ga)
        self.entr_Ga.grid(row=10, column=5, sticky="nesw")
        self.is_Ge = tk.StringVar()
        self.entr_Ge = tk.Entry(self.is_window, textvariable=self.is_Ge)
        self.entr_Ge.grid(row=11, column=5, sticky="nesw")
        self.is_As = tk.StringVar()
        self.entr_As = tk.Entry(self.is_window, textvariable=self.is_As)
        self.entr_As.grid(row=12, column=5, sticky="nesw")
        self.is_Se = tk.StringVar()
        self.entr_Se = tk.Entry(self.is_window, textvariable=self.is_Se)
        self.entr_Se.grid(row=13, column=5, sticky="nesw")
        self.is_Br = tk.StringVar()
        self.entr_Br = tk.Entry(self.is_window, textvariable=self.is_Br)
        self.entr_Br.grid(row=14, column=5, sticky="nesw")
        self.is_Kr = tk.StringVar()
        self.entr_Kr = tk.Entry(self.is_window, textvariable=self.is_Kr)
        self.entr_Kr.grid(row=15, column=5, sticky="nesw")
        self.is_Rb = tk.StringVar()
        self.entr_Rb = tk.Entry(self.is_window, textvariable=self.is_Rb)
        self.entr_Rb.grid(row=16, column=5, sticky="nesw")
        self.is_Sr = tk.StringVar()
        self.entr_Sr = tk.Entry(self.is_window, textvariable=self.is_Sr)
        self.entr_Sr.grid(row=17, column=5, sticky="nesw")
        self.is_Y = tk.StringVar()
        self.entr_Y = tk.Entry(self.is_window, textvariable=self.is_Y)
        self.entr_Y.grid(row=18, column=5, sticky="nesw")
        self.is_Zr = tk.StringVar()
        self.entr_Zr = tk.Entry(self.is_window, textvariable=self.is_Zr)
        self.entr_Zr.grid(row=19, column=5, sticky="nesw")
        self.is_Nb = tk.StringVar()
        self.entr_Nb = tk.Entry(self.is_window, textvariable=self.is_Nb)
        self.entr_Nb.grid(row=20, column=5, sticky="nesw")
        self.is_Mo = tk.StringVar()
        self.entr_Mo = tk.Entry(self.is_window, textvariable=self.is_Mo)
        self.entr_Mo.grid(row=21, column=5, sticky="nesw")
        self.is_Tc = tk.StringVar()
        self.entr_Tc = tk.Entry(self.is_window, textvariable=self.is_Tc)
        self.entr_Tc.grid(row=22, column=5, sticky="nesw")
        self.is_Ru = tk.StringVar()
        self.entr_Ru = tk.Entry(self.is_window, textvariable=self.is_Ru)
        self.entr_Ru.grid(row=23, column=5, sticky="nesw")
        self.is_Rh = tk.StringVar()
        self.entr_Rh = tk.Entry(self.is_window, textvariable=self.is_Rh)
        self.entr_Rh.grid(row=24, column=5, sticky="nesw")
        self.is_Pd = tk.StringVar()
        self.entr_Pd = tk.Entry(self.is_window, textvariable=self.is_Pd)
        self.entr_Pd.grid(row=25, column=5, sticky="nesw")
        #
        self.is_Ag = tk.StringVar()
        self.entr_Ag = tk.Entry(self.is_window, textvariable=self.is_Ag)
        self.entr_Ag.grid(row=3, column=7, sticky="nesw")
        self.is_Cd = tk.StringVar()
        self.entr_Cd = tk.Entry(self.is_window, textvariable=self.is_Cd)
        self.entr_Cd.grid(row=4, column=7, sticky="nesw")
        self.is_In = tk.StringVar()
        self.entr_In = tk.Entry(self.is_window, textvariable=self.is_In)
        self.entr_In.grid(row=5, column=7, sticky="nesw")
        self.is_Sn = tk.StringVar()
        self.entr_Sn = tk.Entry(self.is_window, textvariable=self.is_Sn)
        self.entr_Sn.grid(row=6, column=7, sticky="nesw")
        self.is_Sb = tk.StringVar()
        self.entr_Sb = tk.Entry(self.is_window, textvariable=self.is_Sb)
        self.entr_Sb.grid(row=7, column=7, sticky="nesw")
        self.is_Te = tk.StringVar()
        self.entr_Te = tk.Entry(self.is_window, textvariable=self.is_Te)
        self.entr_Te.grid(row=8, column=7, sticky="nesw")
        self.is_I = tk.StringVar()
        self.entr_I = tk.Entry(self.is_window, textvariable=self.is_I)
        self.entr_I.grid(row=9, column=7, sticky="nesw")
        self.is_Xe = tk.StringVar()
        self.entr_Xe = tk.Entry(self.is_window, textvariable=self.is_Xe)
        self.entr_Xe.grid(row=10, column=7, sticky="nesw")
        self.is_Cs = tk.StringVar()
        self.entr_Cs = tk.Entry(self.is_window, textvariable=self.is_Cs)
        self.entr_Cs.grid(row=11, column=7, sticky="nesw")
        self.is_Ba = tk.StringVar()
        self.entr_Ba = tk.Entry(self.is_window, textvariable=self.is_Ba)
        self.entr_Ba.grid(row=12, column=7, sticky="nesw")
        self.is_La = tk.StringVar()
        self.entr_La = tk.Entry(self.is_window, textvariable=self.is_La)
        self.entr_La.grid(row=13, column=7, sticky="nesw")
        self.is_Ce = tk.StringVar()
        self.entr_Ce = tk.Entry(self.is_window, textvariable=self.is_Ce)
        self.entr_Ce.grid(row=14, column=7, sticky="nesw")
        self.is_Pr = tk.StringVar()
        self.entr_Pr = tk.Entry(self.is_window, textvariable=self.is_Pr)
        self.entr_Pr.grid(row=15, column=7, sticky="nesw")
        self.is_Nd = tk.StringVar()
        self.entr_Nd = tk.Entry(self.is_window, textvariable=self.is_Nd)
        self.entr_Nd.grid(row=16, column=7, sticky="nesw")
        self.is_Pm = tk.StringVar()
        self.entr_Pm = tk.Entry(self.is_window, textvariable=self.is_Pm)
        self.entr_Pm.grid(row=17, column=7, sticky="nesw")
        self.is_Sm = tk.StringVar()
        self.entr_Sm = tk.Entry(self.is_window, textvariable=self.is_Sm)
        self.entr_Sm.grid(row=18, column=7, sticky="nesw")
        self.is_Eu = tk.StringVar()
        self.entr_Eu = tk.Entry(self.is_window, textvariable=self.is_Eu)
        self.entr_Eu.grid(row=19, column=7, sticky="nesw")
        self.is_Gd = tk.StringVar()
        self.entr_Gd = tk.Entry(self.is_window, textvariable=self.is_Gd)
        self.entr_Gd.grid(row=20, column=7, sticky="nesw")
        self.is_Tb = tk.StringVar()
        self.entr_Tb = tk.Entry(self.is_window, textvariable=self.is_Tb)
        self.entr_Tb.grid(row=21, column=7, sticky="nesw")
        self.is_Dy = tk.StringVar()
        self.entr_Dy = tk.Entry(self.is_window, textvariable=self.is_Dy)
        self.entr_Dy.grid(row=22, column=7, sticky="nesw")
        self.is_Ho = tk.StringVar()
        self.entr_Ho = tk.Entry(self.is_window, textvariable=self.is_Ho)
        self.entr_Ho.grid(row=23, column=7, sticky="nesw")
        self.is_Er = tk.StringVar()
        self.entr_Er = tk.Entry(self.is_window, textvariable=self.is_Er)
        self.entr_Er.grid(row=24, column=7, sticky="nesw")
        self.is_Tm = tk.StringVar()
        self.entr_Tm = tk.Entry(self.is_window, textvariable=self.is_Tm)
        self.entr_Tm.grid(row=25, column=7, sticky="nesw")

        self.is_Yb = tk.StringVar()
        self.entr_Yb = tk.Entry(self.is_window, textvariable=self.is_Yb)
        self.entr_Yb.grid(row=3, column=9, sticky="nesw")
        self.is_Lu = tk.StringVar()
        self.entr_Lu = tk.Entry(self.is_window, textvariable=self.is_Lu)
        self.entr_Lu.grid(row=4, column=9, sticky="nesw")
        self.is_Hf = tk.StringVar()
        self.entr_Hf = tk.Entry(self.is_window, textvariable=self.is_Hf)
        self.entr_Hf.grid(row=5, column=9, sticky="nesw")
        self.is_Ta = tk.StringVar()
        self.entr_Ta = tk.Entry(self.is_window, textvariable=self.is_Ta)
        self.entr_Ta.grid(row=6, column=9, sticky="nesw")
        self.is_W = tk.StringVar()
        self.entr_W = tk.Entry(self.is_window, textvariable=self.is_W)
        self.entr_W.grid(row=7, column=9, sticky="nesw")
        self.is_Re = tk.StringVar()
        self.entr_Re = tk.Entry(self.is_window, textvariable=self.is_Re)
        self.entr_Re.grid(row=8, column=9, sticky="nesw")
        self.is_Os = tk.StringVar()
        self.entr_Os = tk.Entry(self.is_window, textvariable=self.is_Os)
        self.entr_Os.grid(row=9, column=9, sticky="nesw")
        self.is_Ir = tk.StringVar()
        self.entr_Ir = tk.Entry(self.is_window, textvariable=self.is_Ir)
        self.entr_Ir.grid(row=10, column=9, sticky="nesw")
        self.is_Pt = tk.StringVar()
        self.entr_Pt = tk.Entry(self.is_window, textvariable=self.is_Pt)
        self.entr_Pt.grid(row=11, column=9, sticky="nesw")
        self.is_Au = tk.StringVar()
        self.entr_Au = tk.Entry(self.is_window, textvariable=self.is_Au)
        self.entr_Au.grid(row=12, column=9, sticky="nesw")
        self.is_Hg = tk.StringVar()
        self.entr_Hg = tk.Entry(self.is_window, textvariable=self.is_Hg)
        self.entr_Hg.grid(row=13, column=9, sticky="nesw")
        self.is_Tl = tk.StringVar()
        self.entr_Tl = tk.Entry(self.is_window, textvariable=self.is_Tl)
        self.entr_Tl.grid(row=14, column=9, sticky="nesw")
        self.is_Pb = tk.StringVar()
        self.entr_Pb = tk.Entry(self.is_window, textvariable=self.is_Pb)
        self.entr_Pb.grid(row=15, column=9, sticky="nesw")
        self.is_Bi = tk.StringVar()
        self.entr_Bi = tk.Entry(self.is_window, textvariable=self.is_Bi)
        self.entr_Bi.grid(row=16, column=9, sticky="nesw")
        self.is_Po = tk.StringVar()
        self.entr_Po = tk.Entry(self.is_window, textvariable=self.is_Po)
        self.entr_Po.grid(row=17, column=9, sticky="nesw")
        self.is_At = tk.StringVar()
        self.entr_At = tk.Entry(self.is_window, textvariable=self.is_At)
        self.entr_At.grid(row=18, column=9, sticky="nesw")
        self.is_Rn = tk.StringVar()
        self.entr_Rn = tk.Entry(self.is_window, textvariable=self.is_Rn)
        self.entr_Rn.grid(row=19, column=9, sticky="nesw")
        self.is_Fr = tk.StringVar()
        self.entr_Fr = tk.Entry(self.is_window, textvariable=self.is_Fr)
        self.entr_Fr.grid(row=20, column=9, sticky="nesw")
        self.is_Ra = tk.StringVar()
        self.entr_Ra = tk.Entry(self.is_window, textvariable=self.is_Ra)
        self.entr_Ra.grid(row=21, column=9, sticky="nesw")
        self.is_Ac = tk.StringVar()
        self.entr_Ac = tk.Entry(self.is_window, textvariable=self.is_Ac)
        self.entr_Ac.grid(row=22, column=9, sticky="nesw")
        self.is_Th = tk.StringVar()
        self.entr_Th = tk.Entry(self.is_window, textvariable=self.is_Th)
        self.entr_Th.grid(row=23, column=9, sticky="nesw")
        self.is_Pa = tk.StringVar()
        self.entr_Pa = tk.Entry(self.is_window, textvariable=self.is_Pa)
        self.entr_Pa.grid(row=24, column=9, sticky="nesw")
        self.is_U = tk.StringVar()
        self.entr_U = tk.Entry(self.is_window, textvariable=self.is_U)
        self.entr_U.grid(row=25, column=9, sticky="nesw")
    #
    def open_csv_is(self):
        concentrations_is = []
        filename = fd.askopenfilenames(parent=self.is_window, filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
                                       initialdir=os.getcwd())
        data_is = data.general().importis(filename=filename[0])
        self.place_concentrations(input_is=data_is, container=concentrations_is)
    #
    def place_concentrations(self, input_is, container):
        for name, conc in input_is:
            if name == "H":
                if len(self.entr_H.get()) > 0:
                    self.entr_H.delete(0, tk.END)
                self.entr_H.insert(0, conc)
                container.append(["H", conc])
            if name == "He":
                if len(self.entr_He.get()) > 0:
                    self.entr_He.delete(0, tk.END)
                self.entr_He.insert(0, conc)
                container.append(["He", conc])
            if name == "Li":
                if len(self.entr_Li.get()) > 0:
                    self.entr_Li.delete(0, tk.END)
                self.entr_Li.insert(0, conc)
                container.append(["Li", conc])
            if name == "Be":
                if len(self.entr_Be.get()) > 0:
                    self.entr_Be.delete(0, tk.END)
                self.entr_Be.insert(0, conc)
                container.append(["Be", conc])
            if name == "B":
                if len(self.entr_B.get()) > 0:
                    self.entr_B.delete(0, tk.END)
                self.entr_B.insert(0, conc)
                container.append(["B", conc])
            if name == "C":
                if len(self.entr_C.get()) > 0:
                    self.entr_C.delete(0, tk.END)
                self.entr_C.insert(0, conc)
                container.append(["C", conc])
            if name == "N":
                if len(self.entr_N.get()) > 0:
                    self.entr_N.delete(0, tk.END)
                self.entr_N.insert(0, conc)
                container.append(["N", conc])
            if name == "O":
                if len(self.entr_O.get()) > 0:
                    self.entr_O.delete(0, tk.END)
                self.entr_O.insert(0, conc)
                container.append(["O", conc])
            if name == "F":
                if len(self.entr_F.get()) > 0:
                    self.entr_F.delete(0, tk.END)
                self.entr_F.insert(0, conc)
                container.append(["F", conc])
            if name == "Ne":
                if len(self.entr_Ne.get()) > 0:
                    self.entr_Ne.delete(0, tk.END)
                self.entr_Ne.insert(0, conc)
                container.append(["Ne", conc])
            if name == "Na":
                if len(self.entr_Na.get()) > 0:
                    self.entr_Na.delete(0, tk.END)
                self.entr_Na.insert(0, conc)
                container.append(["Na", conc])
            if name == "Mg":
                if len(self.entr_Mg.get()) > 0:
                    self.entr_Mg.delete(0, tk.END)
                self.entr_Mg.insert(0, conc)
                container.append(["Mg", conc])
            if name == "Al":
                if len(self.entr_Al.get()) > 0:
                    self.entr_Al.delete(0, tk.END)
                self.entr_Al.insert(0, conc)
                container.append(["Al", conc])
            if name == "Si":
                if len(self.entr_Si.get()) > 0:
                    self.entr_Si.delete(0, tk.END)
                self.entr_Si.insert(0, conc)
                container.append(["Si", conc])
            if name == "P":
                if len(self.entr_P.get()) > 0:
                    self.entr_P.delete(0, tk.END)
                self.entr_P.insert(0, conc)
                container.append(["P", conc])
            if name == "S":
                if len(self.entr_S.get()) > 0:
                    self.entr_S.delete(0, tk.END)
                self.entr_S.insert(0, conc)
                container.append(["S", conc])
            if name == "Cl":
                if len(self.entr_Cl.get()) > 0:
                    self.entr_Cl.delete(0, tk.END)
                self.entr_Cl.insert(0, conc)
                container.append(["Cl", conc])
            if name == "Ar":
                if len(self.entr_Ar.get()) > 0:
                    self.entr_Ar.delete(0, tk.END)
                self.entr_Ar.insert(0, conc)
                container.append(["Ar", conc])
            if name == "K":
                if len(self.entr_K.get()) > 0:
                    self.entr_K.delete(0, tk.END)
                self.entr_K.insert(0, conc)
                container.append(["K", conc])
            if name == "Ca":
                if len(self.entr_Ca.get()) > 0:
                    self.entr_Ca.delete(0, tk.END)
                self.entr_Ca.insert(0, conc)
                container.append(["Ca", conc])
            if name == "Sc":
                if len(self.entr_Sc.get()) > 0:
                    self.entr_Sc.delete(0, tk.END)
                self.entr_Sc.insert(0, conc)
                container.append(["Sc", conc])
            if name == "Ti":
                if len(self.entr_Ti.get()) > 0:
                    self.entr_Ti.delete(0, tk.END)
                self.entr_Ti.insert(0, conc)
                container.append(["Ti", conc])
            if name == "V":
                if len(self.entr_V.get()) > 0:
                    self.entr_V.delete(0, tk.END)
                self.entr_V.insert(0, conc)
                container.append(["V", conc])
            if name == "Cr":
                if len(self.entr_Cr.get()) > 0:
                    self.entr_Cr.delete(0, tk.END)
                self.entr_Cr.insert(0, conc)
                container.append(["Cr", conc])
            if name == "Mn":
                if len(self.entr_Mn.get()) > 0:
                    self.entr_Mn.delete(0, tk.END)
                self.entr_Mn.insert(0, conc)
                container.append(["Mn", conc])
            if name == "Fe":
                if len(self.entr_Fe.get()) > 0:
                    self.entr_Fe.delete(0, tk.END)
                self.entr_Fe.insert(0, conc)
                container.append(["Fe", conc])
            if name == "Co":
                if len(self.entr_Co.get()) > 0:
                    self.entr_Co.delete(0, tk.END)
                self.entr_Co.insert(0, conc)
                container.append(["Co", conc])
            if name == "Ni":
                if len(self.entr_Ni.get()) > 0:
                    self.entr_Ni.delete(0, tk.END)
                self.entr_Ni.insert(0, conc)
                container.append(["Ni", conc])
            if name == "Cu":
                if len(self.entr_Cu.get()) > 0:
                    self.entr_Cu.delete(0, tk.END)
                self.entr_Cu.insert(0, conc)
                container.append(["Cu", conc])
            if name == "Zn":
                if len(self.entr_Zn.get()) > 0:
                    self.entr_Zn.delete(0, tk.END)
                self.entr_Zn.insert(0, conc)
                container.append(["Zn", conc])
            if name == "Ga":
                if len(self.entr_Ga.get()) > 0:
                    self.entr_Ga.delete(0, tk.END)
                self.entr_Ga.insert(0, conc)
                container.append(["Ga", conc])
            if name == "Ge":
                if len(self.entr_Ge.get()) > 0:
                    self.entr_Ge.delete(0, tk.END)
                self.entr_Ge.insert(0, conc)
                container.append(["Ge", conc])
            if name == "As":
                if len(self.entr_As.get()) > 0:
                    self.entr_As.delete(0, tk.END)
                self.entr_As.insert(0, conc)
                container.append(["As", conc])
            if name == "Se":
                if len(self.entr_Se.get()) > 0:
                    self.entr_Se.delete(0, tk.END)
                self.entr_Se.insert(0, conc)
                container.append(["Se", conc])
            if name == "Br":
                if len(self.entr_Br.get()) > 0:
                    self.entr_Br.delete(0, tk.END)
                self.entr_Br.insert(0, conc)
                container.append(["Br", conc])
            if name == "Kr":
                if len(self.entr_Kr.get()) > 0:
                    self.entr_Kr.delete(0, tk.END)
                self.entr_Kr.insert(0, conc)
                container.append(["Kr", conc])
            if name == "Rb":
                if len(self.entr_Rb.get()) > 0:
                    self.entr_Rb.delete(0, tk.END)
                self.entr_Rb.insert(0, conc)
                container.append(["Rb", conc])
            if name == "Sr":
                if len(self.entr_Sr.get()) > 0:
                    self.entr_Sr.delete(0, tk.END)
                self.entr_Sr.insert(0, conc)
                container.append(["Sr", conc])
            if name == "Y":
                if len(self.entr_Y.get()) > 0:
                    self.entr_Y.delete(0, tk.END)
                self.entr_Y.insert(0, conc)
                container.append(["Y", conc])
            if name == "Zr":
                if len(self.entr_Zr.get()) > 0:
                    self.entr_Zr.delete(0, tk.END)
                self.entr_Zr.insert(0, conc)
                container.append(["Zr", conc])
            if name == "Nb":
                if len(self.entr_Nb.get()) > 0:
                    self.entr_Nb.delete(0, tk.END)
                self.entr_Nb.insert(0, conc)
                container.append(["Nb", conc])
            if name == "Mo":
                if len(self.entr_Mo.get()) > 0:
                    self.entr_Mo.delete(0, tk.END)
                self.entr_Mo.insert(0, conc)
                container.append(["Mo", conc])
            if name == "Tc":
                if len(self.entr_Tc.get()) > 0:
                    self.entr_Tc.delete(0, tk.END)
                self.entr_Tc.insert(0, conc)
                container.append(["Tc", conc])
            if name == "Ru":
                if len(self.entr_Ru.get()) > 0:
                    self.entr_Ru.delete(0, tk.END)
                self.entr_Ru.insert(0, conc)
                container.append(["Ru", conc])
            if name == "Rh":
                if len(self.entr_Rh.get()) > 0:
                    self.entr_Rh.delete(0, tk.END)
                self.entr_Rh.insert(0, conc)
                container.append(["Rh", conc])
            if name == "Pd":
                if len(self.entr_Pd.get()) > 0:
                    self.entr_Pd.delete(0, tk.END)
                self.entr_Pd.insert(0, conc)
                container.append(["Pd", conc])
            if name == "Ag":
                if len(self.entr_Ag.get()) > 0:
                    self.entr_Ag.delete(0, tk.END)
                self.entr_Ag.insert(0, conc)
                container.append(["Ag", conc])
            if name == "Cd":
                if len(self.entr_Cd.get()) > 0:
                    self.entr_Cd.delete(0, tk.END)
                self.entr_Cd.insert(0, conc)
                container.append(["Cd", conc])
            if name == "In":
                if len(self.entr_In.get()) > 0:
                    self.entr_In.delete(0, tk.END)
                self.entr_In.insert(0, conc)
                container.append(["In", conc])
            if name == "Sn":
                if len(self.entr_Sn.get()) > 0:
                    self.entr_Sn.delete(0, tk.END)
                self.entr_Sn.insert(0, conc)
                container.append(["Sn", conc])
            if name == "Sb":
                if len(self.entr_Sb.get()) > 0:
                    self.entr_Sb.delete(0, tk.END)
                self.entr_Sb.insert(0, conc)
                container.append(["Sb", conc])
            if name == "Te":
                if len(self.entr_Te.get()) > 0:
                    self.entr_Te.delete(0, tk.END)
                self.entr_Te.insert(0, conc)
                container.append(["Te", conc])
            if name == "I":
                if len(self.entr_I.get()) > 0:
                    self.entr_I.delete(0, tk.END)
                self.entr_I.insert(0, conc)
                container.append(["I", conc])
            if name == "Xe":
                if len(self.entr_Xe.get()) > 0:
                    self.entr_Xe.delete(0, tk.END)
                self.entr_Xe.insert(0, conc)
                container.append(["Xe", conc])
            if name == "Cs":
                if len(self.entr_Cs.get()) > 0:
                    self.entr_Cs.delete(0, tk.END)
                self.entr_Cs.insert(0, conc)
                container.append(["Cs", conc])
            if name == "Ba":
                if len(self.entr_Ba.get()) > 0:
                    self.entr_Ba.delete(0, tk.END)
                self.entr_Ba.insert(0, conc)
                container.append(["Ba", conc])
            if name == "La":
                if len(self.entr_La.get()) > 0:
                    self.entr_La.delete(0, tk.END)
                self.entr_La.insert(0, conc)
                container.append(["La", conc])
            if name == "Ce":
                if len(self.entr_Ce.get()) > 0:
                    self.entr_Ce.delete(0, tk.END)
                self.entr_Ce.insert(0, conc)
                container.append(["Ce", conc])
            if name == "Pr":
                if len(self.entr_Pr.get()) > 0:
                    self.entr_Pr.delete(0, tk.END)
                self.entr_Pr.insert(0, conc)
                container.append(["Pr", conc])
            if name == "Nd":
                if len(self.entr_Nd.get()) > 0:
                    self.entr_Nd.delete(0, tk.END)
                self.entr_Nd.insert(0, conc)
                container.append(["Nd", conc])
            if name == "Pm":
                if len(self.entr_Pm.get()) > 0:
                    self.entr_Pm.delete(0, tk.END)
                self.entr_Pm.insert(0, conc)
                container.append(["Pm", conc])
            if name == "Sm":
                if len(self.entr_Sm.get()) > 0:
                    self.entr_Sm.delete(0, tk.END)
                self.entr_Sm.insert(0, conc)
                container.append(["Sm", conc])
            if name == "Eu":
                if len(self.entr_Eu.get()) > 0:
                    self.entr_Eu.delete(0, tk.END)
                self.entr_Eu.insert(0, conc)
                container.append(["Eu", conc])
            if name == "Gd":
                if len(self.entr_Gd.get()) > 0:
                    self.entr_Gd.delete(0, tk.END)
                self.entr_Gd.insert(0, conc)
                container.append(["Gd", conc])
            if name == "Tb":
                if len(self.entr_Tb.get()) > 0:
                    self.entr_Tb.delete(0, tk.END)
                self.entr_Tb.insert(0, conc)
                container.append(["Tb", conc])
            if name == "Dy":
                if len(self.entr_Dy.get()) > 0:
                    self.entr_Dy.delete(0, tk.END)
                self.entr_Dy.insert(0, conc)
                container.append(["Dy", conc])
            if name == "Ho":
                if len(self.entr_Ho.get()) > 0:
                    self.entr_Ho.delete(0, tk.END)
                self.entr_Ho.insert(0, conc)
                container.append(["Ho", conc])
            if name == "Er":
                if len(self.entr_Er.get()) > 0:
                    self.entr_Er.delete(0, tk.END)
                self.entr_Er.insert(0, conc)
                container.append(["Er", conc])
            if name == "Tm":
                if len(self.entr_Tm.get()) > 0:
                    self.entr_Tm.delete(0, tk.END)
                self.entr_Tm.insert(0, conc)
                container.append(["Tm", conc])
            if name == "Yb":
                if len(self.entr_Yb.get()) > 0:
                    self.entr_Yb.delete(0, tk.END)
                self.entr_Yb.insert(0, conc)
                container.append(["Yb", conc])
            if name == "Lu":
                if len(self.entr_Lu.get()) > 0:
                    self.entr_Lu.delete(0, tk.END)
                self.entr_Lu.insert(0, conc)
                container.append(["Lu", conc])
            if name == "Hf":
                if len(self.entr_Hf.get()) > 0:
                    self.entr_Hf.delete(0, tk.END)
                self.entr_Hf.insert(0, conc)
                container.append(["Hf", conc])
            if name == "Ta":
                if len(self.entr_Ta.get()) > 0:
                    self.entr_Ta.delete(0, tk.END)
                self.entr_Ta.insert(0, conc)
                container.append(["Ta", conc])
            if name == "W":
                if len(self.entr_W.get()) > 0:
                    self.entr_W.delete(0, tk.END)
                self.entr_W.insert(0, conc)
                container.append(["W", conc])
            if name == "Re":
                if len(self.entr_Re.get()) > 0:
                    self.entr_Re.delete(0, tk.END)
                self.entr_Re.insert(0, conc)
                container.append(["Re", conc])
            if name == "Os":
                if len(self.entr_Os.get()) > 0:
                    self.entr_Os.delete(0, tk.END)
                self.entr_Os.insert(0, conc)
                container.append(["Os", conc])
            if name == "Ir":
                if len(self.entr_Ir.get()) > 0:
                    self.entr_Ir.delete(0, tk.END)
                self.entr_Ir.insert(0, conc)
                container.append(["Ir", conc])
            if name == "Pt":
                if len(self.entr_Pt.get()) > 0:
                    self.entr_Pt.delete(0, tk.END)
                self.entr_Pt.insert(0, conc)
                container.append(["Pt", conc])
            if name == "Au":
                if len(self.entr_Au.get()) > 0:
                    self.entr_Au.delete(0, tk.END)
                self.entr_Au.insert(0, conc)
                container.append(["Au", conc])
            if name == "Hg":
                if len(self.entr_Hg.get()) > 0:
                    self.entr_Hg.delete(0, tk.END)
                self.entr_Hg.insert(0, conc)
                container.append(["Hg", conc])
            if name == "Tl":
                if len(self.entr_Tl.get()) > 0:
                    self.entr_Tl.delete(0, tk.END)
                self.entr_Tl.insert(0, conc)
                container.append(["Tl", conc])
            if name == "Pb":
                if len(self.entr_Pb.get()) > 0:
                    self.entr_Pb.delete(0, tk.END)
                self.entr_Pb.insert(0, conc)
                container.append(["Pb", conc])
            if name == "Bi":
                if len(self.entr_Bi.get()) > 0:
                    self.entr_Bi.delete(0, tk.END)
                self.entr_Bi.insert(0, conc)
                container.append(["Bi", conc])
            if name == "Po":
                if len(self.entr_Po.get()) > 0:
                    self.entr_Po.delete(0, tk.END)
                self.entr_Po.insert(0, conc)
                container.append(["Po", conc])
            if name == "At":
                if len(self.entr_K.get()) > 0:
                    self.entr_K.delete(0, tk.END)
                self.entr_At.insert(0, conc)
                container.append(["At", conc])
            if name == "Rn":
                if len(self.entr_Rn.get()) > 0:
                    self.entr_Rn.delete(0, tk.END)
                self.entr_Rn.insert(0, conc)
                container.append(["Rn", conc])
            if name == "Fr":
                if len(self.entr_Fr.get()) > 0:
                    self.entr_Fr.delete(0, tk.END)
                self.entr_Fr.insert(0, conc)
                container.append(["Fr", conc])
            if name == "Ra":
                if len(self.entr_Ra.get()) > 0:
                    self.entr_Ra.delete(0, tk.END)
                self.entr_Ra.insert(0, conc)
                container.append(["Ra", conc])
            if name == "Ac":
                if len(self.entr_Ac.get()) > 0:
                    self.entr_Ac.delete(0, tk.END)
                self.entr_Ac.insert(0, conc)
                container.append(["Ac", conc])
            if name == "Th":
                if len(self.entr_Th.get()) > 0:
                    self.entr_Th.delete(0, tk.END)
                self.entr_Th.insert(0, conc)
                container.append(["Th", conc])
            if name == "Pa":
                if len(self.entr_Pa.get()) > 0:
                    self.entr_Pa.delete(0, tk.END)
                self.entr_Pa.insert(0, conc)
                container.append(["Pa", conc])
            if name == "U":
                if len(self.entr_U.get()) > 0:
                    self.entr_U.delete(0, tk.END)
                self.entr_U.insert(0, conc)
                container.append(["U", conc])
        #
        return container