#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# standard.py
# Maximilian Beeskow
# 05.08.2021
# ----------------------
#
## MODULES
import tkinter as tk
import tkinter.filedialog as fd
import numpy as np
import re, os
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.colors as pltcol
from modules import data
#
## TOOLS
#
class standardAnalysis:
    #
    def __init__(self):
        pass
    #
    def calculateSensitivities(self, concentrations, intensities, start, end, reference, plots):
        self.concentrations = concentrations
        self.intensities = intensities
        self.start = start
        self.end = end
        self.reference = reference
        self.plots = plots
        #
        C_STD = self.concentrations
        I_STD = self.intensities
        I_STD = []
        for i in range(1, len(self.intensities)):
            I_STD.append([self.intensities[i][0], []])
        for i in range(0, len(I_STD)):
            for j in range(0, len(self.intensities[i + 1][1])):
                I_STD[i][1].append(self.intensities[i + 1][1][j])
        laserOn = self.start
        laserOff = self.start + self.end
        #
        referenceData = []
        for i in range(0, len(C_STD)):
            if self.reference == C_STD[i][0]:
                referenceData.append(C_STD[i][1])
                referenceData.append([])
            else:
                pass
        for i in range(0, len(I_STD)):
            if self.reference in I_STD[i][0]:
                for j in range(laserOn, laserOff):
                    referenceData[1].append(I_STD[i][1][j])
            else:
                pass
        #
        # print("Reference data:", referenceData)
        xi = []
        Cstd = []
        for i in range(0, len(I_STD)):
            xi.append([I_STD[i][0], []])
        for i in range(0, len(I_STD)):
            keyword = re.search(r"(\D+)(\d+)", I_STD[i][0])
            for j in range(0, len(C_STD)):
                if C_STD[j][0] == keyword.group(1):
                    Cstd.append([I_STD[i][0], C_STD[j][1]])
                    # print(C_STD[j][0], keyword.group(1))
                    for k in range(laserOn, laserOff):
                        xi[i][1].append(
                            (I_STD[i][1][k] * referenceData[0]) / (referenceData[1][k - laserOn] * C_STD[j][1]))
                else:
                    pass
        for i in range(0, len(xi)):
            xi[i].append([np.mean(xi[i][1]), np.std(xi[i][1], ddof=1)])
        for i in range(0, len(xi)):
           print("Sensitivities:", xi[i][0], xi[i][2], round(xi[i][2][1]/xi[i][2][0]*100,2), "%")
        #
        C_STDcalc = []
        for i in range(0, len(I_STD)):
            C_STDcalc.append([I_STD[i][0], []])
        for i in range(0, len(I_STD)):
            for j in range(0, len(xi)):
                if xi[j][0] == C_STDcalc[i][0] and len(xi[i][1]) > 0:
                    for k in range(laserOn, laserOff):
                        if xi[j][1][k - laserOn] == 0.0:
                            xi[j][1][k - laserOn] += 0.000001
                            C_STDcalc[i][1].append(I_STD[i][1][k] / xi[j][1][k - laserOn])
                        else:
                            C_STDcalc[i][1].append(I_STD[i][1][k] / xi[j][1][k - laserOn])
                else:
                    pass
        # for i in range(0, len(xi)):
        #    print("Concentrations (calc.):", C_STDcalc[i][0], np.mean(C_STDcalc[i][1]), np.std(C_STDcalc[i][1], ddof=1), round(np.std(C_STDcalc[i][1], ddof=1)/np.mean(C_STDcalc[i][1])*100,2))
        #
        dataLinRegr = []
        for i in range(0, len(I_STD)):
            if len(C_STDcalc[i][1]) < 1:
                dataLinRegr.append([C_STDcalc[i][0], []])
            else:
                result = I_STD[i][0], stats.linregress(C_STDcalc[i][1], I_STD[i][1][laserOn:laserOff])
                dataLinRegr.append([result])
        # for i in range(0, len(dataLinRegr)):
        #    print(dataLinRegr[i])
        #
        if self.plots == True:
            plt.figure(figsize=(8, 4), dpi=150)
            dataC = []
            dataI = []
            for i in range(0, len(I_STD)):
                if len(C_STDcalc[i][1]) > 0:
                    dataC.extend(C_STDcalc[i][1])
                    dataI.extend(I_STD[i][1][laserOn:laserOff])
                    plt.scatter(C_STDcalc[i][1], I_STD[i][1][laserOn:laserOff], s=2.5, label=I_STD[i][0])
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
            for i in range(0, len(C_STDcalc)):
                dataY.append([C_STDcalc[i][0], [dataLinRegr[i][0][1][0]*X + dataLinRegr[i][0][1][1] for X in C_STDcalc[i][1]]])
            #
            for i in range(0, len(dataY)):
                if len(dataY[i][1]) == 0:
                    pass
                else:
                    plt.figure()
                    plt.plot(C_STDcalc[i][1], dataY[i][1], linewidth=2.5, linestyle="solid")
                    plt.scatter(C_STDcalc[i][1], I_STD[i][1][laserOn:laserOff], label=I_STD[i][0], alpha=0.75)
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
        return referenceData, xi, C_STDcalc, Cstd
    #
    def calculate_xi(self, I, C, reference, start, stop):
        self.I = I[1:]
        self.C = C
        self.reference = reference
        self.start = start
        self.stop = start + stop
        #
        isotopes = []
        #
        for i in range(0, len(self.I)):
            #isotopes.append(self.I[i][0])
            #plt.hist(self.I[i][1][self.start:self.stop], bins=12, edgecolor="black")
            #plt.title(self.I[i][0])
            #plt.show()
            keyword = re.search(r"(\D+)(\d+)", self.I[i][0])
            if self.reference == keyword.group(1):
                self.I_reference = self.I[i][1][self.start:self.stop]
        for i in range(0, len(self.C)):
            keyword = re.search(r"(\D+)", self.C[i][0])
            if self.reference == keyword.group(1):
                self.C_reference = self.C[i][1]
        #
        self.I_vector = []
        self.C_vector = []
        #
        for i in range(0, len(self.I)):
            keyword = re.search(r"(\D+)(\d+)", self.I[i][0])
            for j in range(0, len(self.C)):
                if self.C[j][0] == keyword.group(1):
                    isotopes.append(self.I[i][0])
                    self.I_vector.append(np.mean(self.I[i][1][self.start:self.stop])/np.mean(self.I_reference))
                    self.C_vector.append(self.C_reference/self.C[j][1])
        #
        self.xi = np.array(self.I_vector)*np.array(self.C_vector)

        plt.scatter(self.I_vector, self.C_vector, c=self.xi, norm=pltcol.LogNorm())
        cbar = plt.colorbar(label="$\\xi$")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("I")
        plt.ylabel("C")
        plt.grid()
        plt.show()

        return self.xi, isotopes

class StandardReferenceMaterials:
    #
    def __init__(self, parent, color_bg):
        self.parent = parent
        self.color_bg = color_bg
        self.color_fg = "black"
        self.entries = []
        #
        padx_value = 0
        pady_value = 0
        ipadx_value = 1
        ipady_value = 1
        #
        self.srm_window = tk.Toplevel(self.parent)
        self.srm_window.geometry("900x675")
        self.srm_window.title("Standard Reference Materials")
        #
        for x in range(11):
            tk.Grid.columnconfigure(self.srm_window, x, weight=1)
        for y in range(27):
            tk.Grid.rowconfigure(self.srm_window, y, weight=1)
        #
        self.srm_window.grid_columnconfigure(0, minsize=120)
        self.srm_window.grid_columnconfigure(1, minsize=200)
        for i in range(2, 10, 2):
            self.srm_window.grid_columnconfigure(i, minsize=60)
        for i in range(3, 10, 2):
            self.srm_window.grid_columnconfigure(i, minsize=80)
        self.srm_window.grid_columnconfigure(10, minsize=20)
        for i in range(0, 2):
            self.srm_window.grid_rowconfigure(i, minsize=35)
        self.srm_window.grid_rowconfigure(2, minsize=15)
        for i in range(3, 26):
            self.srm_window.grid_rowconfigure(i, minsize=25)
        self.srm_window.grid_rowconfigure(26, minsize=15)
        #
        # Buttons
        btn_01 = tk.Button(self.srm_window, text="Load SRM file", fg=self.color_fg, bg=self.color_bg, command=self.open_csv_srm)
        btn_01.grid(row=0, column=0, padx=padx_value, pady=pady_value,
                    ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        btn_02 = tk.Button(self.srm_window, text="Set SRM data", fg=self.color_fg, bg=self.color_bg)
        btn_02.grid(row=1, column=0, padx=padx_value, pady=pady_value,
                    ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        #
        # Labels
        lbl_01 = tk.Label(self.srm_window, text="Select SRM data")
        lbl_01.grid(row=0, column=1, padx=padx_value, pady=pady_value,
                    ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        #
        # Options menus
        self.srm_glasses = np.array([["NIST 606"], ["NIST 610"], ["NIST 610 (GeoReM)"], ["NIST 610 (Spandler)"],
                                     ["NIST 611"], ["NIST 611 (GeoReM)"], ["NIST 612"], ["NIST 612 (GeoReM)"],
                                     ["NIST 613"], ["NIST 613 (GeoReM)"], ["NIST 614"], ["NIST 614 (GeoReM)"],
                                     ["NIST 615"], ["NIST 615 (GeoReM)"], ["NIST 616"], ["NIST 616 (GeoReM)"],
                                     ["NIST 617"], ["NIST 617 (GeoReM)"], ["USGS BCR-2G (GeoReM)"],
                                     ["USGS GSD-1G (GeoReM)"], ["USGS GSE-1G (GeoReM)"]])
        option_list = self.srm_glasses[:, 0]
        self.var_srm = tk.StringVar()
        #self.var_srm.set(option_list[0])
        self.var_srm.set("Select SRM")
        opt_menu = tk.OptionMenu(self.srm_window, self.var_srm, *option_list, command=self.option_changed)
        opt_menu.grid(row=1, column=1, padx=padx_value, pady=pady_value,
                      ipadx=ipadx_value, ipady=ipady_value, sticky="nesw")
        #
        # Labels PSE
        lbl_H = tk.Label(self.srm_window, text="H")
        lbl_H.grid(row=3, column=2, sticky="nesw")
        lbl_He = tk.Label(self.srm_window, text="He")
        lbl_He.grid(row=4, column=2, sticky="nesw")
        lbl_Li = tk.Label(self.srm_window, text="Li")
        lbl_Li.grid(row=5, column=2, sticky="nesw")
        lbl_Be = tk.Label(self.srm_window, text="Be")
        lbl_Be.grid(row=6, column=2, sticky="nesw")
        lbl_B = tk.Label(self.srm_window, text="B")
        lbl_B.grid(row=7, column=2, sticky="nesw")
        lbl_C = tk.Label(self.srm_window, text="C")
        lbl_C.grid(row=8, column=2, sticky="nesw")
        lbl_N = tk.Label(self.srm_window, text="N")
        lbl_N.grid(row=9, column=2, sticky="nesw")
        lbl_O = tk.Label(self.srm_window, text="O")
        lbl_O.grid(row=10, column=2, sticky="nesw")
        lbl_F = tk.Label(self.srm_window, text="F")
        lbl_F.grid(row=11, column=2, sticky="nesw")
        lbl_Ne = tk.Label(self.srm_window, text="Ne")
        lbl_Ne.grid(row=12, column=2, sticky="nesw")
        lbl_Na = tk.Label(self.srm_window, text="Na")
        lbl_Na.grid(row=13, column=2, sticky="nesw")
        lbl_Mg = tk.Label(self.srm_window, text="Mg")
        lbl_Mg.grid(row=14, column=2, sticky="nesw")
        lbl_Al = tk.Label(self.srm_window, text="Al")
        lbl_Al.grid(row=15, column=2, sticky="nesw")
        lbl_Si = tk.Label(self.srm_window, text="Si")
        lbl_Si.grid(row=16, column=2, sticky="nesw")
        lbl_P = tk.Label(self.srm_window, text="P")
        lbl_P.grid(row=17, column=2, sticky="nesw")
        lbl_S = tk.Label(self.srm_window, text="S")
        lbl_S.grid(row=18, column=2, sticky="nesw")
        lbl_Cl = tk.Label(self.srm_window, text="Cl")
        lbl_Cl.grid(row=19, column=2, sticky="nesw")
        lbl_Ar = tk.Label(self.srm_window, text="Ar")
        lbl_Ar.grid(row=20, column=2, sticky="nesw")
        lbl_K = tk.Label(self.srm_window, text="K")
        lbl_K.grid(row=21, column=2, sticky="nesw")
        lbl_Ca = tk.Label(self.srm_window, text="Ca")
        lbl_Ca.grid(row=22, column=2, sticky="nesw")
        lbl_Sc = tk.Label(self.srm_window, text="Sc")
        lbl_Sc.grid(row=23, column=2, sticky="nesw")
        lbl_Ti = tk.Label(self.srm_window, text="Ti")
        lbl_Ti.grid(row=24, column=2, sticky="nesw")
        lbl_V = tk.Label(self.srm_window, text="V")
        lbl_V.grid(row=25, column=2, sticky="nesw")
        #
        lbl_Cr = tk.Label(self.srm_window, text="Cr")
        lbl_Cr.grid(row=3, column=4, sticky="nesw")
        lbl_Mn = tk.Label(self.srm_window, text="Mn")
        lbl_Mn.grid(row=4, column=4, sticky="nesw")
        lbl_Fe = tk.Label(self.srm_window, text="Fe")
        lbl_Fe.grid(row=5, column=4, sticky="nesw")
        lbl_Co = tk.Label(self.srm_window, text="Co")
        lbl_Co.grid(row=6, column=4, sticky="nesw")
        lbl_Ni = tk.Label(self.srm_window, text="Ni")
        lbl_Ni.grid(row=7, column=4, sticky="nesw")
        lbl_Cu = tk.Label(self.srm_window, text="Cz")
        lbl_Cu.grid(row=8, column=4, sticky="nesw")
        lbl_Zn = tk.Label(self.srm_window, text="Zm")
        lbl_Zn.grid(row=9, column=4, sticky="nesw")
        lbl_Ga = tk.Label(self.srm_window, text="Ga")
        lbl_Ga.grid(row=10, column=4, sticky="nesw")
        lbl_Ge = tk.Label(self.srm_window, text="Ge")
        lbl_Ge.grid(row=11, column=4, sticky="nesw")
        lbl_As = tk.Label(self.srm_window, text="As")
        lbl_As.grid(row=12, column=4, sticky="nesw")
        lbl_Se = tk.Label(self.srm_window, text="Se")
        lbl_Se.grid(row=13, column=4, sticky="nesw")
        lbl_Br = tk.Label(self.srm_window, text="Br")
        lbl_Br.grid(row=14, column=4, sticky="nesw")
        lbl_Kr = tk.Label(self.srm_window, text="Kr")
        lbl_Kr.grid(row=15, column=4, sticky="nesw")
        lbl_Rb = tk.Label(self.srm_window, text="Rb")
        lbl_Rb.grid(row=16, column=4, sticky="nesw")
        lbl_Sr = tk.Label(self.srm_window, text="Sr")
        lbl_Sr.grid(row=17, column=4, sticky="nesw")
        lbl_Y = tk.Label(self.srm_window, text="Y")
        lbl_Y.grid(row=18, column=4, sticky="nesw")
        lbl_Zr = tk.Label(self.srm_window, text="Zr")
        lbl_Zr.grid(row=19, column=4, sticky="nesw")
        lbl_Nb = tk.Label(self.srm_window, text="Nb")
        lbl_Nb.grid(row=20, column=4, sticky="nesw")
        lbl_Mo = tk.Label(self.srm_window, text="Mo")
        lbl_Mo.grid(row=21, column=4, sticky="nesw")
        lbl_Tc = tk.Label(self.srm_window, text="Tc")
        lbl_Tc.grid(row=22, column=4, sticky="nesw")
        lbl_Ru = tk.Label(self.srm_window, text="Ru")
        lbl_Ru.grid(row=23, column=4, sticky="nesw")
        lbl_Rh = tk.Label(self.srm_window, text="Rh")
        lbl_Rh.grid(row=24, column=4, sticky="nesw")
        lbl_Pd = tk.Label(self.srm_window, text="Pd")
        lbl_Pd.grid(row=25, column=4, sticky="nesw")
        #
        lbl_Ag = tk.Label(self.srm_window, text="Ag")
        lbl_Ag.grid(row=3, column=6, sticky="nesw")
        lbl_Cd = tk.Label(self.srm_window, text="Cd")
        lbl_Cd.grid(row=4, column=6, sticky="nesw")
        lbl_In = tk.Label(self.srm_window, text="In")
        lbl_In.grid(row=5, column=6, sticky="nesw")
        lbl_Sn = tk.Label(self.srm_window, text="Sn")
        lbl_Sn.grid(row=6, column=6, sticky="nesw")
        lbl_Sb = tk.Label(self.srm_window, text="Sb")
        lbl_Sb.grid(row=7, column=6, sticky="nesw")
        lbl_Te = tk.Label(self.srm_window, text="Te")
        lbl_Te.grid(row=8, column=6, sticky="nesw")
        lbl_I = tk.Label(self.srm_window, text="I")
        lbl_I.grid(row=9, column=6, sticky="nesw")
        lbl_Xe = tk.Label(self.srm_window, text="Xe")
        lbl_Xe.grid(row=10, column=6, sticky="nesw")
        lbl_Cs = tk.Label(self.srm_window, text="Cs")
        lbl_Cs.grid(row=11, column=6, sticky="nesw")
        lbl_Ba = tk.Label(self.srm_window, text="Ba")
        lbl_Ba.grid(row=12, column=6, sticky="nesw")
        lbl_La = tk.Label(self.srm_window, text="La")
        lbl_La.grid(row=13, column=6, sticky="nesw")
        lbl_Ce = tk.Label(self.srm_window, text="Ce")
        lbl_Ce.grid(row=14, column=6, sticky="nesw")
        lbl_Pr = tk.Label(self.srm_window, text="Pr")
        lbl_Pr.grid(row=15, column=6, sticky="nesw")
        lbl_Nd = tk.Label(self.srm_window, text="Nd")
        lbl_Nd.grid(row=16, column=6, sticky="nesw")
        lbl_Pm = tk.Label(self.srm_window, text="Pm")
        lbl_Pm.grid(row=17, column=6, sticky="nesw")
        lbl_Sm = tk.Label(self.srm_window, text="Sm")
        lbl_Sm.grid(row=18, column=6, sticky="nesw")
        lbl_Eu = tk.Label(self.srm_window, text="Eu")
        lbl_Eu.grid(row=19, column=6, sticky="nesw")
        lbl_Gd = tk.Label(self.srm_window, text="Gd")
        lbl_Gd.grid(row=20, column=6, sticky="nesw")
        lbl_Tb = tk.Label(self.srm_window, text="Tb")
        lbl_Tb.grid(row=21, column=6, sticky="nesw")
        lbl_Dy = tk.Label(self.srm_window, text="Dy")
        lbl_Dy.grid(row=22, column=6, sticky="nesw")
        lbl_Ho = tk.Label(self.srm_window, text="Ho")
        lbl_Ho.grid(row=23, column=6, sticky="nesw")
        lbl_Er = tk.Label(self.srm_window, text="Er")
        lbl_Er.grid(row=24, column=6, sticky="nesw")
        lbl_Tm = tk.Label(self.srm_window, text="Tm")
        lbl_Tm.grid(row=25, column=6, sticky="nesw")
        #
        lbl_Yb = tk.Label(self.srm_window, text="Yb")
        lbl_Yb.grid(row=3, column=8, sticky="nesw")
        lbl_Lu = tk.Label(self.srm_window, text="Lu")
        lbl_Lu.grid(row=4, column=8, sticky="nesw")
        lbl_Hf = tk.Label(self.srm_window, text="Hf")
        lbl_Hf.grid(row=5, column=8, sticky="nesw")
        lbl_Ta = tk.Label(self.srm_window, text="Ta")
        lbl_Ta.grid(row=6, column=8, sticky="nesw")
        lbl_W = tk.Label(self.srm_window, text="W")
        lbl_W.grid(row=7, column=8, sticky="nesw")
        lbl_Re = tk.Label(self.srm_window, text="Re")
        lbl_Re.grid(row=8, column=8, sticky="nesw")
        lbl_Os = tk.Label(self.srm_window, text="Os")
        lbl_Os.grid(row=9, column=8, sticky="nesw")
        lbl_Ir = tk.Label(self.srm_window, text="Ir")
        lbl_Ir.grid(row=10, column=8, sticky="nesw")
        lbl_Pt = tk.Label(self.srm_window, text="Pt")
        lbl_Pt.grid(row=11, column=8, sticky="nesw")
        lbl_Au = tk.Label(self.srm_window, text="Au")
        lbl_Au.grid(row=12, column=8, sticky="nesw")
        lbl_Hg = tk.Label(self.srm_window, text="Hg")
        lbl_Hg.grid(row=13, column=8, sticky="nesw")
        lbl_Tl = tk.Label(self.srm_window, text="Tl")
        lbl_Tl.grid(row=14, column=8, sticky="nesw")
        lbl_Pb = tk.Label(self.srm_window, text="Pb")
        lbl_Pb.grid(row=15, column=8, sticky="nesw")
        lbl_Bi = tk.Label(self.srm_window, text="Bi")
        lbl_Bi.grid(row=16, column=8, sticky="nesw")
        lbl_Po = tk.Label(self.srm_window, text="Po")
        lbl_Po.grid(row=17, column=8, sticky="nesw")
        lbl_At = tk.Label(self.srm_window, text="At")
        lbl_At.grid(row=18, column=8, sticky="nesw")
        lbl_Rn = tk.Label(self.srm_window, text="Rn")
        lbl_Rn.grid(row=19, column=8, sticky="nesw")
        lbl_Fr = tk.Label(self.srm_window, text="Fr")
        lbl_Fr.grid(row=20, column=8, sticky="nesw")
        lbl_Ra = tk.Label(self.srm_window, text="Ra")
        lbl_Ra.grid(row=21, column=8, sticky="nesw")
        lbl_Ac = tk.Label(self.srm_window, text="Ac")
        lbl_Ac.grid(row=22, column=8, sticky="nesw")
        lbl_Th = tk.Label(self.srm_window, text="Th")
        lbl_Th.grid(row=23, column=8, sticky="nesw")
        lbl_Pa = tk.Label(self.srm_window, text="Pa")
        lbl_Pa.grid(row=24, column=8, sticky="nesw")
        lbl_U = tk.Label(self.srm_window, text="U")
        lbl_U.grid(row=25, column=8, sticky="nesw")
        #
        # Entries PSE
        self.srm_H = tk.StringVar()
        self.entr_H = tk.Entry(self.srm_window, textvariable=self.srm_H)
        self.entr_H.grid(row=3, column=3, sticky="nesw")
        self.srm_He = tk.StringVar()
        self.entr_He = tk.Entry(self.srm_window, textvariable=self.srm_He)
        self.entr_He.grid(row=4, column=3, sticky="nesw")
        self.srm_Li = tk.StringVar()
        self.entr_Li = tk.Entry(self.srm_window, textvariable=self.srm_Li)
        self.entr_Li.grid(row=5, column=3, sticky="nesw")
        self.srm_Be = tk.StringVar()
        self.entr_Be = tk.Entry(self.srm_window, textvariable=self.srm_Be)
        self.entr_Be.grid(row=6, column=3, sticky="nesw")
        self.srm_B = tk.StringVar()
        self.entr_B = tk.Entry(self.srm_window, textvariable=self.srm_B)
        self.entr_B.grid(row=7, column=3, sticky="nesw")
        self.srm_C = tk.StringVar()
        self.entr_C = tk.Entry(self.srm_window, textvariable=self.srm_C)
        self.entr_C.grid(row=8, column=3, sticky="nesw")
        self.srm_N = tk.StringVar()
        self.entr_N = tk.Entry(self.srm_window, textvariable=self.srm_N)
        self.entr_N.grid(row=9, column=3, sticky="nesw")
        self.srm_O = tk.StringVar()
        self.entr_O = tk.Entry(self.srm_window, textvariable=self.srm_O)
        self.entr_O.grid(row=10, column=3, sticky="nesw")
        self.srm_F = tk.StringVar()
        self.entr_F = tk.Entry(self.srm_window, textvariable=self.srm_F)
        self.entr_F.grid(row=11, column=3, sticky="nesw")
        self.srm_Ne = tk.StringVar()
        self.entr_Ne = tk.Entry(self.srm_window, textvariable=self.srm_Ne)
        self.entr_Ne.grid(row=12, column=3, sticky="nesw")
        self.srm_Na = tk.StringVar()
        self.entr_Na = tk.Entry(self.srm_window, textvariable=self.srm_Na)
        self.entr_Na.grid(row=13, column=3, sticky="nesw")
        self.srm_Mg = tk.StringVar()
        self.entr_Mg = tk.Entry(self.srm_window, textvariable=self.srm_Mg)
        self.entr_Mg.grid(row=14, column=3, sticky="nesw")
        self.srm_Al = tk.StringVar()
        self.entr_Al = tk.Entry(self.srm_window, textvariable=self.srm_Al)
        self.entr_Al.grid(row=15, column=3, sticky="nesw")
        self.srm_Si = tk.StringVar()
        self.entr_Si = tk.Entry(self.srm_window, textvariable=self.srm_Si)
        self.entr_Si.grid(row=16, column=3, sticky="nesw")
        self.srm_P = tk.StringVar()
        self.entr_P = tk.Entry(self.srm_window, textvariable=self.srm_P)
        self.entr_P.grid(row=17, column=3, sticky="nesw")
        self.srm_S = tk.StringVar()
        self.entr_S = tk.Entry(self.srm_window, textvariable=self.srm_S)
        self.entr_S.grid(row=18, column=3, sticky="nesw")
        self.srm_Cl = tk.StringVar()
        self.entr_Cl = tk.Entry(self.srm_window, textvariable=self.srm_Cl)
        self.entr_Cl.grid(row=19, column=3, sticky="nesw")
        self.srm_Ar = tk.StringVar()
        self.entr_Ar = tk.Entry(self.srm_window, textvariable=self.srm_Ar)
        self.entr_Ar.grid(row=20, column=3, sticky="nesw")
        self.srm_K = tk.StringVar()
        self.entr_K = tk.Entry(self.srm_window, textvariable=self.srm_K)
        self.entr_K.grid(row=21, column=3, sticky="nesw")
        self.srm_Ca = tk.StringVar()
        self.entr_Ca = tk.Entry(self.srm_window, textvariable=self.srm_Ca)
        self.entr_Ca.grid(row=22, column=3, sticky="nesw")
        self.srm_Sc = tk.StringVar()
        self.entr_Sc = tk.Entry(self.srm_window, textvariable=self.srm_Sc)
        self.entr_Sc.grid(row=23, column=3, sticky="nesw")
        self.srm_Ti = tk.StringVar()
        self.entr_Ti = tk.Entry(self.srm_window, textvariable=self.srm_Ti)
        self.entr_Ti.grid(row=24, column=3, sticky="nesw")
        self.srm_V = tk.StringVar()
        self.entr_V = tk.Entry(self.srm_window, textvariable=self.srm_V)
        self.entr_V.grid(row=25, column=3, sticky="nesw")
        #
        self.srm_Cr = tk.StringVar()
        self.entr_Cr = tk.Entry(self.srm_window, textvariable=self.srm_Cr)
        self.entr_Cr.grid(row=3, column=5, sticky="nesw")
        self.srm_Mn = tk.StringVar()
        self.entr_Mn = tk.Entry(self.srm_window, textvariable=self.srm_Mn)
        self.entr_Mn.grid(row=4, column=5, sticky="nesw")
        self.srm_Fe = tk.StringVar()
        self.entr_Fe = tk.Entry(self.srm_window, textvariable=self.srm_Fe)
        self.entr_Fe.grid(row=5, column=5, sticky="nesw")
        self.srm_Co = tk.StringVar()
        self.entr_Co = tk.Entry(self.srm_window, textvariable=self.srm_Co)
        self.entr_Co.grid(row=6, column=5, sticky="nesw")
        self.srm_Ni = tk.StringVar()
        self.entr_Ni = tk.Entry(self.srm_window, textvariable=self.srm_Ni)
        self.entr_Ni.grid(row=7, column=5, sticky="nesw")
        self.srm_Cu = tk.StringVar()
        self.entr_Cu = tk.Entry(self.srm_window, textvariable=self.srm_Cu)
        self.entr_Cu.grid(row=8, column=5, sticky="nesw")
        self.srm_Zn = tk.StringVar()
        self.entr_Zn = tk.Entry(self.srm_window, textvariable=self.srm_Zn)
        self.entr_Zn.grid(row=9, column=5, sticky="nesw")
        self.srm_Ga = tk.StringVar()
        self.entr_Ga = tk.Entry(self.srm_window, textvariable=self.srm_Ga)
        self.entr_Ga.grid(row=10, column=5, sticky="nesw")
        self.srm_Ge = tk.StringVar()
        self.entr_Ge = tk.Entry(self.srm_window, textvariable=self.srm_Ge)
        self.entr_Ge.grid(row=11, column=5, sticky="nesw")
        self.srm_As = tk.StringVar()
        self.entr_As = tk.Entry(self.srm_window, textvariable=self.srm_As)
        self.entr_As.grid(row=12, column=5, sticky="nesw")
        self.srm_Se = tk.StringVar()
        self.entr_Se = tk.Entry(self.srm_window, textvariable=self.srm_Se)
        self.entr_Se.grid(row=13, column=5, sticky="nesw")
        self.srm_Br = tk.StringVar()
        self.entr_Br = tk.Entry(self.srm_window, textvariable=self.srm_Br)
        self.entr_Br.grid(row=14, column=5, sticky="nesw")
        self.srm_Kr = tk.StringVar()
        self.entr_Kr = tk.Entry(self.srm_window, textvariable=self.srm_Kr)
        self.entr_Kr.grid(row=15, column=5, sticky="nesw")
        self.srm_Rb = tk.StringVar()
        self.entr_Rb = tk.Entry(self.srm_window, textvariable=self.srm_Rb)
        self.entr_Rb.grid(row=16, column=5, sticky="nesw")
        self.srm_Sr = tk.StringVar()
        self.entr_Sr = tk.Entry(self.srm_window, textvariable=self.srm_Sr)
        self.entr_Sr.grid(row=17, column=5, sticky="nesw")
        self.srm_Y = tk.StringVar()
        self.entr_Y = tk.Entry(self.srm_window, textvariable=self.srm_Y)
        self.entr_Y.grid(row=18, column=5, sticky="nesw")
        self.srm_Zr = tk.StringVar()
        self.entr_Zr = tk.Entry(self.srm_window, textvariable=self.srm_Zr)
        self.entr_Zr.grid(row=19, column=5, sticky="nesw")
        self.srm_Nb = tk.StringVar()
        self.entr_Nb = tk.Entry(self.srm_window, textvariable=self.srm_Nb)
        self.entr_Nb.grid(row=20, column=5, sticky="nesw")
        self.srm_Mo = tk.StringVar()
        self.entr_Mo = tk.Entry(self.srm_window, textvariable=self.srm_Mo)
        self.entr_Mo.grid(row=21, column=5, sticky="nesw")
        self.srm_Tc = tk.StringVar()
        self.entr_Tc = tk.Entry(self.srm_window, textvariable=self.srm_Tc)
        self.entr_Tc.grid(row=22, column=5, sticky="nesw")
        self.srm_Ru = tk.StringVar()
        self.entr_Ru = tk.Entry(self.srm_window, textvariable=self.srm_Ru)
        self.entr_Ru.grid(row=23, column=5, sticky="nesw")
        self.srm_Rh = tk.StringVar()
        self.entr_Rh = tk.Entry(self.srm_window, textvariable=self.srm_Rh)
        self.entr_Rh.grid(row=24, column=5, sticky="nesw")
        self.srm_Pd = tk.StringVar()
        self.entr_Pd = tk.Entry(self.srm_window, textvariable=self.srm_Pd)
        self.entr_Pd.grid(row=25, column=5, sticky="nesw")
        #
        self.srm_Ag = tk.StringVar()
        self.entr_Ag = tk.Entry(self.srm_window, textvariable=self.srm_Ag)
        self.entr_Ag.grid(row=3, column=7, sticky="nesw")
        self.srm_Cd = tk.StringVar()
        self.entr_Cd = tk.Entry(self.srm_window, textvariable=self.srm_Cd)
        self.entr_Cd.grid(row=4, column=7, sticky="nesw")
        self.srm_In = tk.StringVar()
        self.entr_In = tk.Entry(self.srm_window, textvariable=self.srm_In)
        self.entr_In.grid(row=5, column=7, sticky="nesw")
        self.srm_Sn = tk.StringVar()
        self.entr_Sn = tk.Entry(self.srm_window, textvariable=self.srm_Sn)
        self.entr_Sn.grid(row=6, column=7, sticky="nesw")
        self.srm_Sb = tk.StringVar()
        self.entr_Sb = tk.Entry(self.srm_window, textvariable=self.srm_Sb)
        self.entr_Sb.grid(row=7, column=7, sticky="nesw")
        self.srm_Te = tk.StringVar()
        self.entr_Te = tk.Entry(self.srm_window, textvariable=self.srm_Te)
        self.entr_Te.grid(row=8, column=7, sticky="nesw")
        self.srm_I = tk.StringVar()
        self.entr_I = tk.Entry(self.srm_window, textvariable=self.srm_I)
        self.entr_I.grid(row=9, column=7, sticky="nesw")
        self.srm_Xe = tk.StringVar()
        self.entr_Xe = tk.Entry(self.srm_window, textvariable=self.srm_Xe)
        self.entr_Xe.grid(row=10, column=7, sticky="nesw")
        self.srm_Cs = tk.StringVar()
        self.entr_Cs = tk.Entry(self.srm_window, textvariable=self.srm_Cs)
        self.entr_Cs.grid(row=11, column=7, sticky="nesw")
        self.srm_Ba = tk.StringVar()
        self.entr_Ba = tk.Entry(self.srm_window, textvariable=self.srm_Ba)
        self.entr_Ba.grid(row=12, column=7, sticky="nesw")
        self.srm_La = tk.StringVar()
        self.entr_La = tk.Entry(self.srm_window, textvariable=self.srm_La)
        self.entr_La.grid(row=13, column=7, sticky="nesw")
        self.srm_Ce = tk.StringVar()
        self.entr_Ce = tk.Entry(self.srm_window, textvariable=self.srm_Ce)
        self.entr_Ce.grid(row=14, column=7, sticky="nesw")
        self.srm_Pr = tk.StringVar()
        self.entr_Pr = tk.Entry(self.srm_window, textvariable=self.srm_Pr)
        self.entr_Pr.grid(row=15, column=7, sticky="nesw")
        self.srm_Nd = tk.StringVar()
        self.entr_Nd = tk.Entry(self.srm_window, textvariable=self.srm_Nd)
        self.entr_Nd.grid(row=16, column=7, sticky="nesw")
        self.srm_Pm = tk.StringVar()
        self.entr_Pm = tk.Entry(self.srm_window, textvariable=self.srm_Pm)
        self.entr_Pm.grid(row=17, column=7, sticky="nesw")
        self.srm_Sm = tk.StringVar()
        self.entr_Sm = tk.Entry(self.srm_window, textvariable=self.srm_Sm)
        self.entr_Sm.grid(row=18, column=7, sticky="nesw")
        self.srm_Eu = tk.StringVar()
        self.entr_Eu = tk.Entry(self.srm_window, textvariable=self.srm_Eu)
        self.entr_Eu.grid(row=19, column=7, sticky="nesw")
        self.srm_Gd = tk.StringVar()
        self.entr_Gd = tk.Entry(self.srm_window, textvariable=self.srm_Gd)
        self.entr_Gd.grid(row=20, column=7, sticky="nesw")
        self.srm_Tb = tk.StringVar()
        self.entr_Tb = tk.Entry(self.srm_window, textvariable=self.srm_Tb)
        self.entr_Tb.grid(row=21, column=7, sticky="nesw")
        self.srm_Dy = tk.StringVar()
        self.entr_Dy = tk.Entry(self.srm_window, textvariable=self.srm_Dy)
        self.entr_Dy.grid(row=22, column=7, sticky="nesw")
        self.srm_Ho = tk.StringVar()
        self.entr_Ho = tk.Entry(self.srm_window, textvariable=self.srm_Ho)
        self.entr_Ho.grid(row=23, column=7, sticky="nesw")
        self.srm_Er = tk.StringVar()
        self.entr_Er = tk.Entry(self.srm_window, textvariable=self.srm_Er)
        self.entr_Er.grid(row=24, column=7, sticky="nesw")
        self.srm_Tm = tk.StringVar()
        self.entr_Tm = tk.Entry(self.srm_window, textvariable=self.srm_Tm)
        self.entr_Tm.grid(row=25, column=7, sticky="nesw")

        self.srm_Yb = tk.StringVar()
        self.entr_Yb = tk.Entry(self.srm_window, textvariable=self.srm_Yb)
        self.entr_Yb.grid(row=3, column=9, sticky="nesw")
        self.srm_Lu = tk.StringVar()
        self.entr_Lu = tk.Entry(self.srm_window, textvariable=self.srm_Lu)
        self.entr_Lu.grid(row=4, column=9, sticky="nesw")
        self.srm_Hf = tk.StringVar()
        self.entr_Hf = tk.Entry(self.srm_window, textvariable=self.srm_Hf)
        self.entr_Hf.grid(row=5, column=9, sticky="nesw")
        self.srm_Ta = tk.StringVar()
        self.entr_Ta = tk.Entry(self.srm_window, textvariable=self.srm_Ta)
        self.entr_Ta.grid(row=6, column=9, sticky="nesw")
        self.srm_W = tk.StringVar()
        self.entr_W = tk.Entry(self.srm_window, textvariable=self.srm_W)
        self.entr_W.grid(row=7, column=9, sticky="nesw")
        self.srm_Re = tk.StringVar()
        self.entr_Re = tk.Entry(self.srm_window, textvariable=self.srm_Re)
        self.entr_Re.grid(row=8, column=9, sticky="nesw")
        self.srm_Os = tk.StringVar()
        self.entr_Os = tk.Entry(self.srm_window, textvariable=self.srm_Os)
        self.entr_Os.grid(row=9, column=9, sticky="nesw")
        self.srm_Ir = tk.StringVar()
        self.entr_Ir = tk.Entry(self.srm_window, textvariable=self.srm_Ir)
        self.entr_Ir.grid(row=10, column=9, sticky="nesw")
        self.srm_Pt = tk.StringVar()
        self.entr_Pt = tk.Entry(self.srm_window, textvariable=self.srm_Pt)
        self.entr_Pt.grid(row=11, column=9, sticky="nesw")
        self.srm_Au = tk.StringVar()
        self.entr_Au = tk.Entry(self.srm_window, textvariable=self.srm_Au)
        self.entr_Au.grid(row=12, column=9, sticky="nesw")
        self.srm_Hg = tk.StringVar()
        self.entr_Hg = tk.Entry(self.srm_window, textvariable=self.srm_Hg)
        self.entr_Hg.grid(row=13, column=9, sticky="nesw")
        self.srm_Tl = tk.StringVar()
        self.entr_Tl = tk.Entry(self.srm_window, textvariable=self.srm_Tl)
        self.entr_Tl.grid(row=14, column=9, sticky="nesw")
        self.srm_Pb = tk.StringVar()
        self.entr_Pb = tk.Entry(self.srm_window, textvariable=self.srm_Pb)
        self.entr_Pb.grid(row=15, column=9, sticky="nesw")
        self.srm_Bi = tk.StringVar()
        self.entr_Bi = tk.Entry(self.srm_window, textvariable=self.srm_Bi)
        self.entr_Bi.grid(row=16, column=9, sticky="nesw")
        self.srm_Po = tk.StringVar()
        self.entr_Po = tk.Entry(self.srm_window, textvariable=self.srm_Po)
        self.entr_Po.grid(row=17, column=9, sticky="nesw")
        self.srm_At = tk.StringVar()
        self.entr_At = tk.Entry(self.srm_window, textvariable=self.srm_At)
        self.entr_At.grid(row=18, column=9, sticky="nesw")
        self.srm_Rn = tk.StringVar()
        self.entr_Rn = tk.Entry(self.srm_window, textvariable=self.srm_Rn)
        self.entr_Rn.grid(row=19, column=9, sticky="nesw")
        self.srm_Fr = tk.StringVar()
        self.entr_Fr = tk.Entry(self.srm_window, textvariable=self.srm_Fr)
        self.entr_Fr.grid(row=20, column=9, sticky="nesw")
        self.srm_Ra = tk.StringVar()
        self.entr_Ra = tk.Entry(self.srm_window, textvariable=self.srm_Ra)
        self.entr_Ra.grid(row=21, column=9, sticky="nesw")
        self.srm_Ac = tk.StringVar()
        self.entr_Ac = tk.Entry(self.srm_window, textvariable=self.srm_Ac)
        self.entr_Ac.grid(row=22, column=9, sticky="nesw")
        self.srm_Th = tk.StringVar()
        self.entr_Th = tk.Entry(self.srm_window, textvariable=self.srm_Th)
        self.entr_Th.grid(row=23, column=9, sticky="nesw")
        self.srm_Pa = tk.StringVar()
        self.entr_Pa = tk.Entry(self.srm_window, textvariable=self.srm_Pa)
        self.entr_Pa.grid(row=24, column=9, sticky="nesw")
        self.srm_U = tk.StringVar()
        self.entr_U = tk.Entry(self.srm_window, textvariable=self.srm_U)
        self.entr_U.grid(row=25, column=9, sticky="nesw")

    def option_changed(self, op):
        path = os.getcwd()
        parent = os.path.dirname(path)
        if self.var_srm.get() == "NIST 606":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_606.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 610":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 610 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 610 (Spandler)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610_Spandler.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 611":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_611.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 611 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_611_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 612":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_612.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 612 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_612_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 613":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_613.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 613 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_613_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 614":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_614.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 614 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_614_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 615":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_615.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 615 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_615_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 616":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_616.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 616 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_616_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 617":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_617.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "NIST 617 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_617_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "USGS BCR-2G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_BCR2G_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "USGS GSD-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_GSD1G_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "USGS GSE-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_GSE1G_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif self.var_srm.get() == "B6":
            data_srm = data.general().importSRM(filename=parent+str("/lib/B6.csv"))
            self.place_concentrations(input_srm=data_srm)
    #
    def open_csv_srm(self):
        filename = fd.askopenfilenames(parent=self.srm_window, filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
                                       initialdir=os.getcwd())
        data_srm = data.general().importSRM(filename=filename[0])
        self.place_concentrations(input_srm=data_srm)
    #
    def place_concentrations(self, input_srm):
        isotopes_measured = np.array(input_srm)[:, 0]
        for name, conc in input_srm:
            if name == "H":
                if len(self.entr_H.get()) > 0:
                    self.entr_H.delete(0, tk.END)
                self.entr_H.insert(0, conc)
            if name == "He":
                if len(self.entr_He.get()) > 0:
                    self.entr_He.delete(0, tk.END)
                self.entr_He.insert(0, conc)
            if name == "Li":
                if len(self.entr_Li.get()) > 0:
                    self.entr_Li.delete(0, tk.END)
                self.entr_Li.insert(0, conc)
            if name == "Be":
                if len(self.entr_Be.get()) > 0:
                    self.entr_Be.delete(0, tk.END)
                self.entr_Be.insert(0, conc)
            if name == "B":
                if len(self.entr_B.get()) > 0:
                    self.entr_B.delete(0, tk.END)
                self.entr_B.insert(0, conc)
            if name == "C":
                if len(self.entr_C.get()) > 0:
                    self.entr_C.delete(0, tk.END)
                self.entr_C.insert(0, conc)
            if name == "N":
                if len(self.entr_N.get()) > 0:
                    self.entr_N.delete(0, tk.END)
                self.entr_N.insert(0, conc)
            if name == "O":
                if len(self.entr_O.get()) > 0:
                    self.entr_O.delete(0, tk.END)
                self.entr_O.insert(0, conc)
            if name == "F":
                if len(self.entr_F.get()) > 0:
                    self.entr_F.delete(0, tk.END)
                self.entr_F.insert(0, conc)
            if name == "Ne":
                if len(self.entr_Ne.get()) > 0:
                    self.entr_Ne.delete(0, tk.END)
                self.entr_Ne.insert(0, conc)
            if name == "Na":
                if len(self.entr_Na.get()) > 0:
                    self.entr_Na.delete(0, tk.END)
                self.entr_Na.insert(0, conc)
            if name == "Mg":
                if len(self.entr_Mg.get()) > 0:
                    self.entr_Mg.delete(0, tk.END)
                self.entr_Mg.insert(0, conc)
            if name == "Al":
                if len(self.entr_Al.get()) > 0:
                    self.entr_Al.delete(0, tk.END)
                self.entr_Al.insert(0, conc)
            if name == "Si":
                if len(self.entr_Si.get()) > 0:
                    self.entr_Si.delete(0, tk.END)
                self.entr_Si.insert(0, conc)
            if name == "P":
                if len(self.entr_P.get()) > 0:
                    self.entr_P.delete(0, tk.END)
                self.entr_P.insert(0, conc)
            if name == "S":
                if len(self.entr_S.get()) > 0:
                    self.entr_S.delete(0, tk.END)
                self.entr_S.insert(0, conc)
            if name == "Cl":
                if len(self.entr_Cl.get()) > 0:
                    self.entr_Cl.delete(0, tk.END)
                self.entr_Cl.insert(0, conc)
            if name == "Ar":
                if len(self.entr_Ar.get()) > 0:
                    self.entr_Ar.delete(0, tk.END)
                self.entr_Ar.insert(0, conc)
            if name == "K":
                if len(self.entr_K.get()) > 0:
                    self.entr_K.delete(0, tk.END)
                self.entr_K.insert(0, conc)
            if name == "Ca":
                if len(self.entr_Ca.get()) > 0:
                    self.entr_Ca.delete(0, tk.END)
                self.entr_Ca.insert(0, conc)
            if name == "Sc":
                if len(self.entr_Sc.get()) > 0:
                    self.entr_Sc.delete(0, tk.END)
                self.entr_Sc.insert(0, conc)
            if name == "Ti":
                if len(self.entr_Ti.get()) > 0:
                    self.entr_Ti.delete(0, tk.END)
                self.entr_Ti.insert(0, conc)
            if name == "V":
                if len(self.entr_V.get()) > 0:
                    self.entr_V.delete(0, tk.END)
                self.entr_V.insert(0, conc)
            if name == "Cr":
                if len(self.entr_Cr.get()) > 0:
                    self.entr_Cr.delete(0, tk.END)
                self.entr_Cr.insert(0, conc)
            if name == "Mn":
                if len(self.entr_Mn.get()) > 0:
                    self.entr_Mn.delete(0, tk.END)
                self.entr_Mn.insert(0, conc)
            if name == "Fe":
                if len(self.entr_Fe.get()) > 0:
                    self.entr_Fe.delete(0, tk.END)
                self.entr_Fe.insert(0, conc)
            if name == "Co":
                if len(self.entr_Co.get()) > 0:
                    self.entr_Co.delete(0, tk.END)
                self.entr_Co.insert(0, conc)
            if name == "Ni":
                if len(self.entr_Ni.get()) > 0:
                    self.entr_Ni.delete(0, tk.END)
                self.entr_Ni.insert(0, conc)
            if name == "Cu":
                if len(self.entr_Cu.get()) > 0:
                    self.entr_Cu.delete(0, tk.END)
                self.entr_Cu.insert(0, conc)
            if name == "Zn":
                if len(self.entr_Zn.get()) > 0:
                    self.entr_Zn.delete(0, tk.END)
                self.entr_Zn.insert(0, conc)
            if name == "Ga":
                if len(self.entr_Ga.get()) > 0:
                    self.entr_Ga.delete(0, tk.END)
                self.entr_Ga.insert(0, conc)
            if name == "Ge":
                if len(self.entr_Ge.get()) > 0:
                    self.entr_Ge.delete(0, tk.END)
                self.entr_Ge.insert(0, conc)
            if name == "As":
                if len(self.entr_As.get()) > 0:
                    self.entr_As.delete(0, tk.END)
                self.entr_As.insert(0, conc)
            if name == "Se":
                if len(self.entr_Se.get()) > 0:
                    self.entr_Se.delete(0, tk.END)
                self.entr_Se.insert(0, conc)
            if name == "Br":
                if len(self.entr_Br.get()) > 0:
                    self.entr_Br.delete(0, tk.END)
                self.entr_Br.insert(0, conc)
            if name == "Kr":
                if len(self.entr_Kr.get()) > 0:
                    self.entr_Kr.delete(0, tk.END)
                self.entr_Kr.insert(0, conc)
            if name == "Rb":
                if len(self.entr_Rb.get()) > 0:
                    self.entr_Rb.delete(0, tk.END)
                self.entr_Rb.insert(0, conc)
            if name == "Sr":
                if len(self.entr_Sr.get()) > 0:
                    self.entr_Sr.delete(0, tk.END)
                self.entr_Sr.insert(0, conc)
            if name == "Y":
                if len(self.entr_Y.get()) > 0:
                    self.entr_Y.delete(0, tk.END)
                self.entr_Y.insert(0, conc)
            if name == "Zr":
                if len(self.entr_Zr.get()) > 0:
                    self.entr_Zr.delete(0, tk.END)
                self.entr_Zr.insert(0, conc)
            if name == "Nb":
                if len(self.entr_Nb.get()) > 0:
                    self.entr_Nb.delete(0, tk.END)
                self.entr_Nb.insert(0, conc)
            if name == "Mo":
                if len(self.entr_Mo.get()) > 0:
                    self.entr_Mo.delete(0, tk.END)
                self.entr_Mo.insert(0, conc)
            if name == "Tc":
                if len(self.entr_Tc.get()) > 0:
                    self.entr_Tc.delete(0, tk.END)
                self.entr_Tc.insert(0, conc)
            if name == "Ru":
                if len(self.entr_Ru.get()) > 0:
                    self.entr_Ru.delete(0, tk.END)
                self.entr_Ru.insert(0, conc)
            if name == "Rh":
                if len(self.entr_Rh.get()) > 0:
                    self.entr_Rh.delete(0, tk.END)
                self.entr_Rh.insert(0, conc)
            if name == "Pd":
                if len(self.entr_Pd.get()) > 0:
                    self.entr_Pd.delete(0, tk.END)
                self.entr_Pd.insert(0, conc)
            if name == "Ag":
                if len(self.entr_Ag.get()) > 0:
                    self.entr_Ag.delete(0, tk.END)
                self.entr_Ag.insert(0, conc)
            if name == "Cd":
                if len(self.entr_Cd.get()) > 0:
                    self.entr_Cd.delete(0, tk.END)
                self.entr_Cd.insert(0, conc)
            if name == "In":
                if len(self.entr_In.get()) > 0:
                    self.entr_In.delete(0, tk.END)
                self.entr_In.insert(0, conc)
            if name == "Sn":
                if len(self.entr_Sn.get()) > 0:
                    self.entr_Sn.delete(0, tk.END)
                self.entr_Sn.insert(0, conc)
            if name == "Sb":
                if len(self.entr_Sb.get()) > 0:
                    self.entr_Sb.delete(0, tk.END)
                self.entr_Sb.insert(0, conc)
            if name == "Te":
                if len(self.entr_Te.get()) > 0:
                    self.entr_Te.delete(0, tk.END)
                self.entr_Te.insert(0, conc)
            if name == "I":
                if len(self.entr_I.get()) > 0:
                    self.entr_I.delete(0, tk.END)
                self.entr_I.insert(0, conc)
            if name == "Xe":
                if len(self.entr_Xe.get()) > 0:
                    self.entr_Xe.delete(0, tk.END)
                self.entr_Xe.insert(0, conc)
            if name == "Cs":
                if len(self.entr_Cs.get()) > 0:
                    self.entr_Cs.delete(0, tk.END)
                self.entr_Cs.insert(0, conc)
            if name == "Ba":
                if len(self.entr_Ba.get()) > 0:
                    self.entr_Ba.delete(0, tk.END)
                self.entr_Ba.insert(0, conc)
            if name == "La":
                if len(self.entr_La.get()) > 0:
                    self.entr_La.delete(0, tk.END)
                self.entr_La.insert(0, conc)
            if name == "Ce":
                if len(self.entr_Ce.get()) > 0:
                    self.entr_Ce.delete(0, tk.END)
                self.entr_Ce.insert(0, conc)
            if name == "Pr":
                if len(self.entr_Pr.get()) > 0:
                    self.entr_Pr.delete(0, tk.END)
                self.entr_Pr.insert(0, conc)
            if name == "Nd":
                if len(self.entr_Nd.get()) > 0:
                    self.entr_Nd.delete(0, tk.END)
                self.entr_Nd.insert(0, conc)
            if name == "Pm":
                if len(self.entr_Pm.get()) > 0:
                    self.entr_Pm.delete(0, tk.END)
                self.entr_Pm.insert(0, conc)
            if name == "Sm":
                if len(self.entr_Sm.get()) > 0:
                    self.entr_Sm.delete(0, tk.END)
                self.entr_Sm.insert(0, conc)
            if name == "Eu":
                if len(self.entr_Eu.get()) > 0:
                    self.entr_Eu.delete(0, tk.END)
                self.entr_Eu.insert(0, conc)
            if name == "Gd":
                if len(self.entr_Gd.get()) > 0:
                    self.entr_Gd.delete(0, tk.END)
                self.entr_Gd.insert(0, conc)
            if name == "Tb":
                if len(self.entr_Tb.get()) > 0:
                    self.entr_Tb.delete(0, tk.END)
                self.entr_Tb.insert(0, conc)
            if name == "Dy":
                if len(self.entr_Dy.get()) > 0:
                    self.entr_Dy.delete(0, tk.END)
                self.entr_Dy.insert(0, conc)
            if name == "Ho":
                if len(self.entr_Ho.get()) > 0:
                    self.entr_Ho.delete(0, tk.END)
                self.entr_Ho.insert(0, conc)
            if name == "Er":
                if len(self.entr_Er.get()) > 0:
                    self.entr_Er.delete(0, tk.END)
                self.entr_Er.insert(0, conc)
            if name == "Tm":
                if len(self.entr_Tm.get()) > 0:
                    self.entr_Tm.delete(0, tk.END)
                self.entr_Tm.insert(0, conc)
            if name == "Yb":
                if len(self.entr_Yb.get()) > 0:
                    self.entr_Yb.delete(0, tk.END)
                self.entr_Yb.insert(0, conc)
            if name == "Lu":
                if len(self.entr_Lu.get()) > 0:
                    self.entr_Lu.delete(0, tk.END)
                self.entr_Lu.insert(0, conc)
            if name == "Hf":
                if len(self.entr_Hf.get()) > 0:
                    self.entr_Hf.delete(0, tk.END)
                self.entr_Hf.insert(0, conc)
            if name == "Ta":
                if len(self.entr_Ta.get()) > 0:
                    self.entr_Ta.delete(0, tk.END)
                self.entr_Ta.insert(0, conc)
            if name == "W":
                if len(self.entr_W.get()) > 0:
                    self.entr_W.delete(0, tk.END)
                self.entr_W.insert(0, conc)
            if name == "Re":
                if len(self.entr_Re.get()) > 0:
                    self.entr_Re.delete(0, tk.END)
                self.entr_Re.insert(0, conc)
            if name == "Os":
                if len(self.entr_Os.get()) > 0:
                    self.entr_Os.delete(0, tk.END)
                self.entr_Os.insert(0, conc)
            if name == "Ir":
                if len(self.entr_Ir.get()) > 0:
                    self.entr_Ir.delete(0, tk.END)
                self.entr_Ir.insert(0, conc)
            if name == "Pt":
                if len(self.entr_Pt.get()) > 0:
                    self.entr_Pt.delete(0, tk.END)
                self.entr_Pt.insert(0, conc)
            if name == "Au":
                if len(self.entr_Au.get()) > 0:
                    self.entr_Au.delete(0, tk.END)
                self.entr_Au.insert(0, conc)
            if name == "Hg":
                if len(self.entr_Hg.get()) > 0:
                    self.entr_Hg.delete(0, tk.END)
                self.entr_Hg.insert(0, conc)
            if name == "Tl":
                if len(self.entr_Tl.get()) > 0:
                    self.entr_Tl.delete(0, tk.END)
                self.entr_Tl.insert(0, conc)
            if name == "Pb":
                if len(self.entr_Pb.get()) > 0:
                    self.entr_Pb.delete(0, tk.END)
                self.entr_Pb.insert(0, conc)
            if name == "Bi":
                if len(self.entr_Bi.get()) > 0:
                    self.entr_Bi.delete(0, tk.END)
                self.entr_Bi.insert(0, conc)
            if name == "Po":
                if len(self.entr_Po.get()) > 0:
                    self.entr_Po.delete(0, tk.END)
                self.entr_Po.insert(0, conc)
            if name == "At":
                if len(self.entr_K.get()) > 0:
                    self.entr_K.delete(0, tk.END)
                self.entr_At.insert(0, conc)
            if name == "Rn":
                if len(self.entr_Rn.get()) > 0:
                    self.entr_Rn.delete(0, tk.END)
                self.entr_Rn.insert(0, conc)
            if name == "Fr":
                if len(self.entr_Fr.get()) > 0:
                    self.entr_Fr.delete(0, tk.END)
                self.entr_Fr.insert(0, conc)
            if name == "Ra":
                if len(self.entr_Ra.get()) > 0:
                    self.entr_Ra.delete(0, tk.END)
                self.entr_Ra.insert(0, conc)
            if name == "Ac":
                if len(self.entr_Ac.get()) > 0:
                    self.entr_Ac.delete(0, tk.END)
                self.entr_Ac.insert(0, conc)
            if name == "Th":
                if len(self.entr_Th.get()) > 0:
                    self.entr_Th.delete(0, tk.END)
                self.entr_Th.insert(0, conc)
            if name == "Pa":
                if len(self.entr_Pa.get()) > 0:
                    self.entr_Pa.delete(0, tk.END)
                self.entr_Pa.insert(0, conc)
            if name == "U":
                if len(self.entr_U.get()) > 0:
                    self.entr_U.delete(0, tk.END)
                self.entr_U.insert(0, conc)
        #
        if "H" not in isotopes_measured:
            self.entr_H.delete(0, tk.END)
            self.entr_H.insert(0, 0.0)
        if "He" not in isotopes_measured:
            self.entr_He.delete(0, tk.END)
            self.entr_He.insert(0, 0.0)
        if "Li" not in isotopes_measured:
            self.entr_Li.delete(0, tk.END)
            self.entr_Li.insert(0, 0.0)
        if "Be" not in isotopes_measured:
            self.entr_Be.delete(0, tk.END)
            self.entr_Be.insert(0, 0.0)
        if "B" not in isotopes_measured:
            self.entr_B.delete(0, tk.END)
            self.entr_B.insert(0, 0.0)
        if "C" not in isotopes_measured:
            self.entr_C.delete(0, tk.END)
            self.entr_C.insert(0, 0.0)
        if "N" not in isotopes_measured:
            self.entr_N.delete(0, tk.END)
            self.entr_N.insert(0, 0.0)
        if "O" not in isotopes_measured:
            self.entr_O.delete(0, tk.END)
            self.entr_O.insert(0, 0.0)
        if "F" not in isotopes_measured:
            self.entr_F.delete(0, tk.END)
            self.entr_F.insert(0, 0.0)
        if "Ne" not in isotopes_measured:
            self.entr_Ne.delete(0, tk.END)
            self.entr_Ne.insert(0, 0.0)
        if "Na" not in isotopes_measured:
            self.entr_Na.delete(0, tk.END)
            self.entr_Na.insert(0, 0.0)
        if "Mg" not in isotopes_measured:
            self.entr_Mg.delete(0, tk.END)
            self.entr_Mg.insert(0, 0.0)
        if "Al" not in isotopes_measured:
            self.entr_Al.delete(0, tk.END)
            self.entr_Al.insert(0, 0.0)
        if "Si" not in isotopes_measured:
            self.entr_Si.delete(0, tk.END)
            self.entr_Si.insert(0, 0.0)
        if "P" not in isotopes_measured:
            self.entr_P.delete(0, tk.END)
            self.entr_P.insert(0, 0.0)
        if "S" not in isotopes_measured:
            self.entr_S.delete(0, tk.END)
            self.entr_S.insert(0, 0.0)
        if "Cl" not in isotopes_measured:
            self.entr_Cl.delete(0, tk.END)
            self.entr_Cl.insert(0, 0.0)
        if "Ar" not in isotopes_measured:
            self.entr_Ar.delete(0, tk.END)
            self.entr_Ar.insert(0, 0.0)
        if "K" not in isotopes_measured:
            self.entr_K.delete(0, tk.END)
            self.entr_K.insert(0, 0.0)
        if "Ca" not in isotopes_measured:
            self.entr_Ca.delete(0, tk.END)
            self.entr_Ca.insert(0, 0.0)
        if "Sc" not in isotopes_measured:
            self.entr_Sc.delete(0, tk.END)
            self.entr_Sc.insert(0, 0.0)
        if "Ti" not in isotopes_measured:
            self.entr_Ti.delete(0, tk.END)
            self.entr_Ti.insert(0, 0.0)
        if "V" not in isotopes_measured:
            self.entr_V.delete(0, tk.END)
            self.entr_V.insert(0, 0.0)
        if "Cr" not in isotopes_measured:
            self.entr_Cr.delete(0, tk.END)
            self.entr_Cr.insert(0, 0.0)
        if "Mn" not in isotopes_measured:
            self.entr_Mn.delete(0, tk.END)
            self.entr_Mn.insert(0, 0.0)
        if "Fe" not in isotopes_measured:
            self.entr_Fe.delete(0, tk.END)
            self.entr_Fe.insert(0, 0.0)
        if "Co" not in isotopes_measured:
            self.entr_Co.delete(0, tk.END)
            self.entr_Co.insert(0, 0.0)
        if "Ni" not in isotopes_measured:
            self.entr_Ni.delete(0, tk.END)
            self.entr_Ni.insert(0, 0.0)
        if "Cu" not in isotopes_measured:
            self.entr_Cu.delete(0, tk.END)
            self.entr_Cu.insert(0, 0.0)
        if "Zn" not in isotopes_measured:
            self.entr_Zn.delete(0, tk.END)
            self.entr_Zn.insert(0, 0.0)
        if "Ga" not in isotopes_measured:
            self.entr_Ga.delete(0, tk.END)
            self.entr_Ga.insert(0, 0.0)
        if "Ge" not in isotopes_measured:
            self.entr_Ge.delete(0, tk.END)
            self.entr_Ge.insert(0, 0.0)
        if "As" not in isotopes_measured:
            self.entr_As.delete(0, tk.END)
            self.entr_As.insert(0, 0.0)
        if "Se" not in isotopes_measured:
            self.entr_Se.delete(0, tk.END)
            self.entr_Se.insert(0, 0.0)
        if "Br" not in isotopes_measured:
            self.entr_Br.delete(0, tk.END)
            self.entr_Br.insert(0, 0.0)
        if "Kr" not in isotopes_measured:
            self.entr_Kr.delete(0, tk.END)
            self.entr_Kr.insert(0, 0.0)
        if "Rb" not in isotopes_measured:
            self.entr_Rb.delete(0, tk.END)
            self.entr_Rb.insert(0, 0.0)
        if "Sr" not in isotopes_measured:
            self.entr_Sr.delete(0, tk.END)
            self.entr_Sr.insert(0, 0.0)
        if "Y" not in isotopes_measured:
            self.entr_Y.delete(0, tk.END)
            self.entr_Y.insert(0, 0.0)
        if "Zr" not in isotopes_measured:
            self.entr_Zr.delete(0, tk.END)
            self.entr_Zr.insert(0, 0.0)
        if "Nb" not in isotopes_measured:
            self.entr_Nb.delete(0, tk.END)
            self.entr_Nb.insert(0, 0.0)
        if "Mo" not in isotopes_measured:
            self.entr_Mo.delete(0, tk.END)
            self.entr_Mo.insert(0, 0.0)
        if "Tc" not in isotopes_measured:
            self.entr_Tc.delete(0, tk.END)
            self.entr_Tc.insert(0, 0.0)
        if "Ru" not in isotopes_measured:
            self.entr_Ru.delete(0, tk.END)
            self.entr_Ru.insert(0, 0.0)
        if "Rh" not in isotopes_measured:
            self.entr_Rh.delete(0, tk.END)
            self.entr_Rh.insert(0, 0.0)
        if "Pd" not in isotopes_measured:
            self.entr_Pd.delete(0, tk.END)
            self.entr_Pd.insert(0, 0.0)
        if "Ag" not in isotopes_measured:
            self.entr_Ag.delete(0, tk.END)
            self.entr_Ag.insert(0, 0.0)
        if "Cd" not in isotopes_measured:
            self.entr_Cd.delete(0, tk.END)
            self.entr_Cd.insert(0, 0.0)
        if "In" not in isotopes_measured:
            self.entr_In.delete(0, tk.END)
            self.entr_In.insert(0, 0.0)
        if "Sn" not in isotopes_measured:
            self.entr_Sn.delete(0, tk.END)
            self.entr_Sn.insert(0, 0.0)
        if "Sb" not in isotopes_measured:
            self.entr_Sb.delete(0, tk.END)
            self.entr_Sb.insert(0, 0.0)
        if "Te" not in isotopes_measured:
            self.entr_Te.delete(0, tk.END)
            self.entr_Te.insert(0, 0.0)
        if "I" not in isotopes_measured:
            self.entr_I.delete(0, tk.END)
            self.entr_I.insert(0, 0.0)
        if "Xe" not in isotopes_measured:
            self.entr_Xe.delete(0, tk.END)
            self.entr_Xe.insert(0, 0.0)
        if "Cs" not in isotopes_measured:
            self.entr_Cs.delete(0, tk.END)
            self.entr_Cs.insert(0, 0.0)
        if "Ba" not in isotopes_measured:
            self.entr_Ba.delete(0, tk.END)
            self.entr_Ba.insert(0, 0.0)
        if "La" not in isotopes_measured:
            self.entr_La.delete(0, tk.END)
            self.entr_La.insert(0, 0.0)
        if "Ce" not in isotopes_measured:
            self.entr_Ce.delete(0, tk.END)
            self.entr_Ce.insert(0, 0.0)
        if "Pr" not in isotopes_measured:
            self.entr_Pr.delete(0, tk.END)
            self.entr_Pr.insert(0, 0.0)
        if "Nd" not in isotopes_measured:
            self.entr_Nd.delete(0, tk.END)
            self.entr_Nd.insert(0, 0.0)
        if "Pm" not in isotopes_measured:
            self.entr_Pm.delete(0, tk.END)
            self.entr_Pm.insert(0, 0.0)
        if "Sm" not in isotopes_measured:
            self.entr_Sm.delete(0, tk.END)
            self.entr_Sm.insert(0, 0.0)
        if "Eu" not in isotopes_measured:
            self.entr_Eu.delete(0, tk.END)
            self.entr_Eu.insert(0, 0.0)
        if "Gd" not in isotopes_measured:
            self.entr_Gd.delete(0, tk.END)
            self.entr_Gd.insert(0, 0.0)
        if "Tb" not in isotopes_measured:
            self.entr_Tb.delete(0, tk.END)
            self.entr_Tb.insert(0, 0.0)
        if "Dy" not in isotopes_measured:
            self.entr_Dy.delete(0, tk.END)
            self.entr_Dy.insert(0, 0.0)
        if "Ho" not in isotopes_measured:
            self.entr_Ho.delete(0, tk.END)
            self.entr_Ho.insert(0, 0.0)
        if "Er" not in isotopes_measured:
            self.entr_Er.delete(0, tk.END)
            self.entr_Er.insert(0, 0.0)
        if "Tm" not in isotopes_measured:
            self.entr_Tm.delete(0, tk.END)
            self.entr_Tm.insert(0, 0.0)
        if "Yb" not in isotopes_measured:
            self.entr_Yb.delete(0, tk.END)
            self.entr_Yb.insert(0, 0.0)
        if "Lu" not in isotopes_measured:
            self.entr_Lu.delete(0, tk.END)
            self.entr_Lu.insert(0, 0.0)
        if "Hf" not in isotopes_measured:
            self.entr_Hf.delete(0, tk.END)
            self.entr_Hf.insert(0, 0.0)
        if "Ta" not in isotopes_measured:
            self.entr_Ta.delete(0, tk.END)
            self.entr_Ta.insert(0, 0.0)
        if "W" not in isotopes_measured:
            self.entr_W.delete(0, tk.END)
            self.entr_W.insert(0, 0.0)
        if "Re" not in isotopes_measured:
            self.entr_Re.delete(0, tk.END)
            self.entr_Re.insert(0, 0.0)
        if "Os" not in isotopes_measured:
            self.entr_Os.delete(0, tk.END)
            self.entr_Os.insert(0, 0.0)
        if "Ir" not in isotopes_measured:
            self.entr_Ir.delete(0, tk.END)
            self.entr_Ir.insert(0, 0.0)
        if "Pt" not in isotopes_measured:
            self.entr_Pt.delete(0, tk.END)
            self.entr_Pt.insert(0, 0.0)
        if "Au" not in isotopes_measured:
            self.entr_Au.delete(0, tk.END)
            self.entr_Au.insert(0, 0.0)
        if "Hg" not in isotopes_measured:
            self.entr_Hg.delete(0, tk.END)
            self.entr_Hg.insert(0, 0.0)
        if "Tl" not in isotopes_measured:
            self.entr_Tl.delete(0, tk.END)
            self.entr_Tl.insert(0, 0.0)
        if "Pb" not in isotopes_measured:
            self.entr_Pb.delete(0, tk.END)
            self.entr_Pb.insert(0, 0.0)
        if "Bi" not in isotopes_measured:
            self.entr_Bi.delete(0, tk.END)
            self.entr_Bi.insert(0, 0.0)
        if "Po" not in isotopes_measured:
            self.entr_Po.delete(0, tk.END)
            self.entr_Po.insert(0, 0.0)
        if "At" not in isotopes_measured:
            self.entr_At.delete(0, tk.END)
            self.entr_At.insert(0, 0.0)
        if "Rn" not in isotopes_measured:
            self.entr_Rn.delete(0, tk.END)
            self.entr_Rn.insert(0, 0.0)
        if "Fr" not in isotopes_measured:
            self.entr_Fr.delete(0, tk.END)
            self.entr_Fr.insert(0, 0.0)
        if "Ra" not in isotopes_measured:
            self.entr_Ra.delete(0, tk.END)
            self.entr_Ra.insert(0, 0.0)
        if "Ac" not in isotopes_measured:
            self.entr_Ac.delete(0, tk.END)
            self.entr_Ac.insert(0, 0.0)
        if "Th" not in isotopes_measured:
            self.entr_Th.delete(0, tk.END)
            self.entr_Th.insert(0, 0.0)
        if "Pa" not in isotopes_measured:
            self.entr_Pa.delete(0, tk.END)
            self.entr_Pa.insert(0, 0.0)
        if "U" not in isotopes_measured:
            self.entr_U.delete(0, tk.END)
            self.entr_U.insert(0, 0.0)
        #
        self.entries = [self.entr_H, self.entr_He, self.entr_Li, self.entr_Be, self.entr_B, self.entr_C, self.entr_N,
                   self.entr_O, self.entr_F, self.entr_Ne, self.entr_Na, self.entr_Mg, self.entr_Al, self.entr_Si,
                   self.entr_P, self.entr_S, self.entr_Cl, self.entr_Ar, self.entr_K, self.entr_Ca, self.entr_Sc,
                   self.entr_Ti, self.entr_V, self.entr_Cr, self.entr_Mn, self.entr_Fe, self.entr_Co, self.entr_Ni,
                   self.entr_Cu, self.entr_Zn, self.entr_Ga, self.entr_Ge, self.entr_As, self.entr_Se, self.entr_Br,
                   self.entr_Kr, self.entr_Rb, self.entr_Sr, self.entr_Y, self.entr_Zr, self.entr_Nb, self.entr_Mo,
                   self.entr_Tc, self.entr_Ru, self.entr_Rh, self.entr_Pd, self.entr_Ag, self.entr_Cd, self.entr_In,
                   self.entr_Sn, self.entr_Sb, self.entr_Te, self.entr_I, self.entr_Xe, self.entr_Cs, self.entr_Ba,
                   self.entr_La, self.entr_Ce, self.entr_Pr, self.entr_Nd, self.entr_Pm, self.entr_Sm, self.entr_Eu,
                   self.entr_Gd, self.entr_Tb, self.entr_Dy, self.entr_Ho, self.entr_Er, self.entr_Tm, self.entr_Yb,
                   self.entr_Lu, self.entr_Hf, self.entr_Ta, self.entr_W, self.entr_Re, self.entr_Os, self.entr_Ir,
                   self.entr_Pt, self.entr_Au, self.entr_Hg, self.entr_Tl, self.entr_Pb, self.entr_Bi, self.entr_Po,
                   self.entr_At, self.entr_Rn, self.entr_Fr, self.entr_Ra, self.entr_Ac, self.entr_Th, self.entr_Pa,
                   self.entr_U]
    #
    def get_values(self, var_srm):
        path = os.getcwd()
        parent = os.path.dirname(path)
        if var_srm == "NIST 606":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_606.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 610":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 610 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 610 (Spandler)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_610_Spandler.csv"))
        elif var_srm == "NIST 611":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_611.csv"))
        elif var_srm == "NIST 611 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_611_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 612":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_612.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 612 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_612_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 613":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_613.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 613 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_613_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 614":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_614.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 614 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_614_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 615":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_615.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 615 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_615_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 616":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_616.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 616 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_616_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 617":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_617.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "NIST 617 (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/NIST_617_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "USGS BCR-2G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_BCR2G_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "USGS GSD-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_GSD1G_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)
        elif var_srm == "USGS GSE-1G (GeoReM)":
            data_srm = data.general().importSRM(filename=parent+str("/lib/USGS_GSE1G_GeoReM.csv"))
            self.place_concentrations(input_srm=data_srm)