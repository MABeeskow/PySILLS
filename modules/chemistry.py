#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# chemistry.py
# Maximilian Beeskow
# 22.04.2022
# ----------------------
#
## MODULES
import re
import numpy as np
#
## CLASSES
class PeriodicSystemOfElements:
    #
    def __init__(self):
        pass
    #
    def get_element_names(self):
        pse_names = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl",
                         "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As",
                         "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In",
                         "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb",
                         "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl",
                         "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U"]
        #
        return  pse_names
    #
    def get_isotope_masses(self):
        pse_masses = [[1.007825, 2.014102, 3.016049]
        ]
        #
        return pse_masses
    #
    def get_isotopic_mcr(self, isotopes):
        pse_names = self.get_element_names()
        mcr_values = np.zeros(len(isotopes))
        for i in range(len(isotopes)):
            key = re.search("(\D+)(\d+)", isotopes)
            index_isotope = pse_names.index(key.group(1))

class PeriodicSystem:
    """ Class that generates the chemical and physical data of the elements"""
    #
    def __init__(self, name=None, atomicnumber=None):
        """
        :param name: name of the chemical element
        :param atomicnumber: atomic number of the chemical element
        """
        self.name = name
        self.atomicnumber = atomicnumber
    #
    def get_data(self):
        data = []
        # [symbol, atomic number, atomic mass, density, bulk modulus, shear modulus, young's modulus, vP,
        # vS, resistivity]
        if self.name in ["H", "Hydrogen", "hydrogen"] or self.atomicnumber == 1:
            mass_molar = 1.008
            density = 0.0899
            bulk_mod = round(1.4*10**(-4), 5)
            shear_mod = 0.0
            young_mod = (9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = np.sqrt((shear_mod*10**9)/(density))
            resistivity = 0.0
            thermal_cond = 0.1805
            ionization_energy_1st = 13.598
            data = ["H", 1, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["He", "Helium", "helium"] or self.atomicnumber == 2:
            mass_molar = 4.0026
            density = 0.1785
            bulk_mod = round(1.01*10**(-5), 7)
            shear_mod = 0.0
            young_mod = (9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = np.sqrt((shear_mod*10**9)/(density))
            resistivity = 0.0
            thermal_cond = 0.1513
            ionization_energy_1st = 24.587
            ionization_energy_2nd = 54.418
            data = ["He", 2, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Li", "Lithium", "lithium"] or self.atomicnumber == 3:
            mass_molar = 6.938
            density = 530
            bulk_mod = 11
            shear_mod = 4.2
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(9.4*10**(-8), 9)
            thermal_cond = 85
            ionization_energy_1st = 5.392
            ionization_energy_2nd = 75.640
            data = ["Li", 3, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Be", "Beryllium", "beryllium"] or self.atomicnumber == 4:
            mass_molar = 9.0122
            density = 1850
            bulk_mod = 130
            shear_mod = 132
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(4.0*10**(-8), 9)
            thermal_cond = 190
            ionization_energy_1st = 9.323
            ionization_energy_2nd = 18.211
            data = ["Be", 4, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["B", "Boron", "boron"] or self.atomicnumber == 5:
            mass_molar = 10.806
            density = 2460
            bulk_mod = 320
            v_p = 16200
            shear_mod = round((3*(density*v_p**2 - bulk_mod*10**9))/(4)*10**(-9), 1)
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 10000
            thermal_cond = 27
            ionization_energy_1st = 8.298
            ionization_energy_2nd = 25.155
            data = ["B", 5, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["C", "Carbon", "carbon"] or self.atomicnumber == 6:
            mass_molar = 12.009
            density = 3510
            bulk_mod = 33
            v_p = 18350
            shear_mod = round((3*(density*v_p**2 - bulk_mod*10**9))/(4)*10**(-9), 1)
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 1*10**(-5)
            thermal_cond = 140
            ionization_energy_1st = 11.260
            ionization_energy_2nd = 24.383
            data = ["C", 6, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["N", "Nitrogen", "nitrogen"] or self.atomicnumber == 7:
            mass_molar = 14.006
            density = 1.170
            bulk_mod = 2
            v_p = 333.6
            shear_mod = 0.0
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 0.0
            thermal_cond = 0.02583
            ionization_energy_1st = 14.534
            ionization_energy_2nd = 29.601
            data = ["N", 7, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["O", "Oxygen", "oxygen"] or self.atomicnumber == 8:
            mass_molar = 15.999
            density = 1.33
            v_p = 317.5
            shear_mod = 0.0
            bulk_mod = round(v_p**2*density*10**3*10**(-9), 3)
            shear_mod = 0.0
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 0.0
            thermal_cond = 0.02658
            ionization_energy_1st = 13.618
            ionization_energy_2nd = 35.121
            data = ["O", 8, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["F", "Flourine", "flourine"] or self.atomicnumber == 9:
            mass_molar = 18.998
            density = 1650
            bulk_mod = 5
            shear_mod = 2
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 0.0
            thermal_cond = 0.0277
            ionization_energy_1st = 17.423
            ionization_energy_2nd = 34.971
            data = ["F", 9, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ne", "Neon", "neon"] or self.atomicnumber == 10:
            mass_molar = 20.180
            density = 0.84
            v_p = 936
            shear_mod = 0.0
            bulk_mod = round(v_p**2*density*10**3*10**(-9), 3)
            shear_mod = 0.0
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 0.0
            thermal_cond = 0.0491
            ionization_energy_1st = 21.565
            ionization_energy_2nd = 40.963
            data = ["Ne", 10, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Na", "Sodium", "sodium"] or self.atomicnumber == 11:
            mass_molar = 22.990
            density = 970
            bulk_mod = 6.3
            shear_mod = 3.3
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(4.9*10**(-8), 9)
            thermal_cond = 140
            ionization_energy_1st = 5.139
            ionization_energy_2nd = 47.287
            data = ["Na", 11, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Mg", "Magnesium", "magnesium"] or self.atomicnumber == 12:
            mass_molar = 24.304
            density = 1740
            bulk_mod = 45
            shear_mod = 17
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(4.4*10**(-8), 9)
            thermal_cond = 160
            ionization_energy_1st = 7.646
            ionization_energy_2nd = 15.035
            data = ["Mg", 12, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Al", "Aluminium", "aluminium"] or self.atomicnumber == 13:
            mass_molar = 26.982
            density = 2700
            bulk_mod = 76
            shear_mod = 26
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(2.7*10**(-8), 9)
            thermal_cond = 235
            ionization_energy_1st = 5.986
            ionization_energy_2nd = 18.829
            data = ["Al", 13, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Si", "Silicon", "silicon"] or self.atomicnumber == 14:
            mass_molar = 28.084
            density = 2330
            bulk_mod = 100
            young_mod = 47
            shear_mod = round((3*bulk_mod*young_mod)/(9*bulk_mod - young_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 0.001
            thermal_cond = 150
            ionization_energy_1st = 8.152
            ionization_energy_2nd = 16.346
            data = ["Si", 14, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["P", "Phosphorus", "phosphorus"] or self.atomicnumber == 15:
            mass_molar = 30.974
            density = 1940
            bulk_mod = 36.09
            shear_mod = 19.86
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(10*10**(-8), 9)
            thermal_cond = 0.236
            ionization_energy_1st = 10.487
            ionization_energy_2nd = 19.770
            data = ["P", 15, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["S", "Sulfur", "sulfur"] or self.atomicnumber == 16:
            mass_molar = 32.059
            density = 2060
            bulk_mod = 6
            shear_mod = 4
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 1*10**(15)
            thermal_cond = 0.205
            ionization_energy_1st = 10.360
            ionization_energy_2nd = 23.338
            data = ["S", 16, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Cl", "Chlorine", "chlorine"] or self.atomicnumber == 17:
            mass_molar = 35.446
            density = 2.95
            v_p = 206
            shear_mod = 0.0
            bulk_mod = round(v_p**2*density*10**3*10**(-9), 3)
            shear_mod = 0.0
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 100
            thermal_cond = 0.0089
            ionization_energy_1st = 12.968
            ionization_energy_2nd = 23.814
            data = ["Cl", 17, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ar", "Argon", "argon"] or self.atomicnumber == 18:
            mass_molar = 39.948
            density = 1.66
            v_p = 319
            shear_mod = 0.0
            bulk_mod = round(v_p**2*density*10**3*10**(-9), 3)
            shear_mod = 0.0
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 0.0
            thermal_cond = 0.01772
            ionization_energy_1st = 15.760
            ionization_energy_2nd = 27.630
            data = ["Ar", 18, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["K", "Potassium", "potassium"] or self.atomicnumber == 19:
            mass_molar = 39.098
            density = 860
            bulk_mod = 3.1
            shear_mod = 1.3
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(7.5*10**(-8), 9)
            thermal_cond = 100
            ionization_energy_1st = 4.341
            ionization_energy_2nd = 31.630
            data = ["K", 19, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ca", "Calcium", "calcium"] or self.atomicnumber == 20:
            mass_molar = 40.078
            density = 1540
            bulk_mod = 17
            shear_mod = 7.4
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(3.4*10**(-8), 9)
            thermal_cond = 200
            ionization_energy_1st = 6.113
            ionization_energy_2nd = 11.872
            data = ["Ca", 20, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Sc", "Scandium", "scandium"] or self.atomicnumber == 21:
            mass_molar = 44.956
            density = 2990
            bulk_mod = 57
            shear_mod = 29
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(55*10**(-8), 9)
            thermal_cond = 16
            ionization_energy_1st = 6.561
            ionization_energy_2nd = 12.800
            data = ["Sc", 21, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ti", "Titanium", "titanium"] or self.atomicnumber == 22:
            mass_molar = 47.867
            density = 4510
            bulk_mod = 110
            shear_mod = 44
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(40*10**(-8), 9)
            thermal_cond = 21.9
            ionization_energy_1st = 6.828
            ionization_energy_2nd = 13.576
            data = ["Ti", 22, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["V", "Vanadium", "vanadium"] or self.atomicnumber == 23:
            mass_molar = 50.942
            density = 6090
            bulk_mod = 160
            shear_mod = 47
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(20*10**(-8), 9)
            thermal_cond = 30.7
            ionization_energy_1st = 6.746
            ionization_energy_2nd = 14.618
            data = ["V", 23, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Cr", "Chromium", "chromium"] or self.atomicnumber == 24:
            mass_molar = 51.996
            density = 7140
            bulk_mod = 160
            shear_mod = 115
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(12.7*10**(-8), 9)
            thermal_cond = 94
            ionization_energy_1st = 6.767
            ionization_energy_2nd = 16.486
            data = ["Cr", 24, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Mn", "Manganese", "manganese"] or self.atomicnumber == 25:
            mass_molar = 54.938
            density = 7440
            bulk_mod = 160
            young_mod = 198
            shear_mod = round((3*bulk_mod*young_mod)/(9*bulk_mod - young_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(144*10**(-8), 9)
            thermal_cond = 7.8
            ionization_energy_1st = 7.434
            ionization_energy_2nd = 15.640
            data = ["Mn", 25, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Fe", "Iron", "iron"] or self.atomicnumber == 26:
            mass_molar = 55.845
            density = 7870
            bulk_mod = 170
            shear_mod = 82
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(10*10**(-8), 9)
            thermal_cond = 80
            ionization_energy_1st = 7.902
            ionization_energy_2nd = 16.188
            data = ["Fe", 26, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Co", "Cobalt", "cobalt"] or self.atomicnumber == 27:
            mass_molar = 58.933
            density = 8890
            bulk_mod = 180
            shear_mod = 75
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(6*10**(-8), 9)
            thermal_cond = 100
            ionization_energy_1st = 7.881
            ionization_energy_2nd = 17.084
            data = ["Co", 27, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ni", "Nickel", "nickel"] or self.atomicnumber == 28:
            mass_molar = 58.639
            density = 8910
            bulk_mod = 180
            shear_mod = 76
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(7.2*10**(-8), 9)
            thermal_cond = 91
            ionization_energy_1st = 7.640
            ionization_energy_2nd = 18.169
            data = ["Ni", 28, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Cu", "Copper", "copper"] or self.atomicnumber == 29:
            mass_molar = 63.546
            density = 8920
            bulk_mod = 140
            shear_mod = 48
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(1.72*10**(-8), 10)
            thermal_cond = 400
            ionization_energy_1st = 7.726
            ionization_energy_2nd = 20.292
            data = ["Cu", 29, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Zn", "Zinc", "zinc"] or self.atomicnumber == 30:
            mass_molar = 65.38
            density = 7140
            bulk_mod = 70
            shear_mod = 43
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(6.0*10**(-8), 10)
            thermal_cond = 116
            ionization_energy_1st = 9.394
            ionization_energy_2nd = 17.964
            data = ["Zn", 30, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ga", "Gallium", "gallium"] or self.atomicnumber == 31:
            mass_molar = 69.723
            density = 5910
            bulk_mod = 50
            shear_mod = 35
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(14*10**(-8), 10)
            thermal_cond = 29
            ionization_energy_1st = 5.999
            ionization_energy_2nd = 20.515
            data = ["Ga", 31, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ge", "Germanium", "germanium"] or self.atomicnumber == 32:
            mass_molar = 72.630
            density = 5320
            bulk_mod = 59.93
            shear_mod = 30.47
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(50000*10**(-8), 10)
            thermal_cond = 60
            ionization_energy_1st = 7.899
            ionization_energy_2nd = 15.935
            data = ["Ge", 32, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["As", "Arsenic", "arsenic"] or self.atomicnumber == 33:
            mass_molar = 74.922
            density = 5720
            bulk_mod = 22
            young_mod = 8
            shear_mod = round((3*bulk_mod*young_mod)/(9*bulk_mod - young_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(33*10**(-8), 10)
            thermal_cond = 50
            ionization_energy_1st = 9.789
            ionization_energy_2nd = 18.589
            data = ["As", 33, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Se", "Selenium", "selenium"] or self.atomicnumber == 34:
            mass_molar = 78.971
            density = 4820
            bulk_mod = 8.3
            shear_mod = 3.7
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(10*10**(-8), 10)
            thermal_cond = 0.52
            ionization_energy_1st = 9.752
            ionization_energy_2nd = 21.190
            data = ["Se", 34, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Br", "Bromine", "bromine"] or self.atomicnumber == 35:
            mass_molar = 79.901
            density = 3140
            bulk_mod = 1.9
            shear_mod = 1.425 # estimated
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(1*10**18*10**(-8), 10)
            thermal_cond = 0.12
            ionization_energy_1st = 11.814
            ionization_energy_2nd = 21.591
            data = ["Br", 35, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Kr", "Krypton", "krypton"] or self.atomicnumber == 36:
            mass_molar = 83.798
            density = 3.48
            v_p = 1120
            shear_mod = 0.0
            bulk_mod = round(v_p**2*density*10**3*10**(-9), 3)
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 0.0
            thermal_cond = 0.00943
            ionization_energy_1st = 14.000
            ionization_energy_2nd = 24.360
            data = ["Kr", 36, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Rb", "Rubidium", "rubidium"] or self.atomicnumber == 37:
            mass_molar = 85.468
            density = 1530
            bulk_mod = 2.5
            young_mod = 2.4
            shear_mod = round((3*bulk_mod*young_mod)/(9*bulk_mod - young_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(13.3*10**(-8), 10)
            thermal_cond = 58
            ionization_energy_1st = 4.177
            ionization_energy_2nd = 27.290
            data = ["Rb", 37, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Sr", "Strontium", "strontium"] or self.atomicnumber == 38:
            mass_molar = 87.62
            density = 2630
            shear_mod = 6.1
            poisson = 0.28
            bulk_mod = round((2*shear_mod*(1+poisson))/(3*(1-2*poisson)), 1)
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(13.5*10**(-8), 10)
            thermal_cond = 35
            ionization_energy_1st = 5.695
            ionization_energy_2nd = 11.030
            data = ["Sr", 38, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Y", "Yttrium", "yttrium"] or self.atomicnumber == 39:
            mass_molar = 88.906
            density = 4470
            bulk_mod = 41
            shear_mod = 26
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(60*10**(-8), 9)
            thermal_cond = 17.2
            ionization_energy_1st = 6.217
            ionization_energy_2nd = 12.224
            data = ["Y", 39, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Zr", "Zirconium", "zirconium"] or self.atomicnumber == 40:
            mass_molar = 91.224
            density = 6510
            shear_mod = 33
            young_mod = 68
            bulk_mod = round((young_mod*shear_mod)/(3*(3*shear_mod-young_mod)), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(43.3*10**(-8), 9)
            thermal_cond = 22.7
            ionization_energy_1st = 6.634
            ionization_energy_2nd = 13.130
            data = ["Zr", 40, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Nb", "Niobium", "niobium"] or self.atomicnumber == 41:
            mass_molar = 92.906
            density = 8580
            bulk_mod = 170
            shear_mod = 38
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(15.2*10**(-8), 9)
            thermal_cond = 54
            ionization_energy_1st = 6.759
            ionization_energy_2nd = 14.000
            data = ["Nb", 41, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Mo", "Molybdenum", "molybdenum"] or self.atomicnumber == 42:
            mass_molar = 95.95
            density = 10280
            bulk_mod = 230
            shear_mod = 20
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(5.5*10**(-8), 9)
            thermal_cond = 139
            ionization_energy_1st = 7.092
            ionization_energy_2nd = 16.160
            data = ["Mo", 42, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Tc", "Technetium", "technetium"] or self.atomicnumber == 43:
            mass_molar = 97
            density = 11490
            bulk_mod = 281
            shear_mod = 123
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 0.0000185
            thermal_cond = 50.6
            ionization_energy_1st = 7.280
            ionization_energy_2nd = 15.260
            data = ["Tc", 43, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ru", "Ruthenium", "ruthenium"] or self.atomicnumber == 44:
            mass_molar = 101.07
            density = 12450
            bulk_mod = 220
            shear_mod = 173
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(7.1*10**(-8), 9)
            thermal_cond = 120
            ionization_energy_1st = 7.361
            ionization_energy_2nd = 16.760
            data = ["Ru", 44, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Rh", "Rhodium", "rhodium"] or self.atomicnumber == 45:
            mass_molar = 102.91
            density = 12410
            bulk_mod = 380
            shear_mod = 150
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(4.3*10**(-8), 9)
            thermal_cond = 150
            ionization_energy_1st = 7.459
            ionization_energy_2nd = 18.080
            data = ["Rh", 45, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Pd", "Palladium", "palladium"] or self.atomicnumber == 46:
            mass_molar = 106.42
            density = 12020
            bulk_mod = 180
            shear_mod = 44
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(10.8*10**(-8), 9)
            thermal_cond = 72
            ionization_energy_1st = 8.337
            ionization_energy_2nd = 19.430
            data = ["Pd", 46, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ag", "Silver", "silver"] or self.atomicnumber == 47:
            mass_molar = 107.87
            density = 10490
            bulk_mod = 100
            shear_mod = 30
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(1.63*10**(-8), 9)
            thermal_cond = 430
            ionization_energy_1st = 7.576
            ionization_energy_2nd = 21.477
            data = ["Ag", 47, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Cd", "Cadmium", "cadmium"] or self.atomicnumber == 48:
            mass_molar = 112.41
            density = 8640
            bulk_mod = 42
            shear_mod = 19
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(7*10**(-8), 9)
            thermal_cond = 97
            ionization_energy_1st = 8.994
            ionization_energy_2nd = 16.908
            data = ["Cd", 48, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["In", "Indium", "indium"] or self.atomicnumber == 49:
            mass_molar = 114.82
            density = 7310
            shear_mod = 4.4
            poisson = 0.4498
            bulk_mod = round((2*shear_mod*(1+poisson))/(3*(1-2*poisson)), 1)
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(8*10**(-8), 9)
            thermal_cond = 82
            ionization_energy_1st = 5.786
            ionization_energy_2nd = 18.870
            data = ["In", 49, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Sn", "Tin", "tin"] or self.atomicnumber == 50:
            mass_molar = 118.71
            density = 7290
            bulk_mod = 58
            shear_mod = 18
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(11.5*10**(-8), 9)
            thermal_cond = 66.6
            ionization_energy_1st = 7.344
            ionization_energy_2nd = 14.632
            data = ["Sn", 50, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Sb", "Antimony", "antimony"] or self.atomicnumber == 51:
            mass_molar = 121.76
            density = 6690
            bulk_mod = 42
            shear_mod = 20
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(40*10**(-8), 9)
            thermal_cond = 24
            ionization_energy_1st = 8.608
            ionization_energy_2nd = 16.630
            data = ["Sb", 51, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Te", "Tellurium", "tellurium"] or self.atomicnumber == 52:
            mass_molar = 127.60
            density = 6250
            bulk_mod = 65
            shear_mod = 16
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(10000*10**(-8), 9)
            thermal_cond = 3
            ionization_energy_1st = 9.010
            ionization_energy_2nd = 18.600
            data = ["Te", 52, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["I", "Iodine", "iodine"] or self.atomicnumber == 53:
            mass_molar = 126.90
            density = 4940
            bulk_mod = 7.7
            shear_mod = 6.16 # estimated
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(10**15*10**(-8), 9)
            thermal_cond = 0.449
            ionization_energy_1st = 10.451
            ionization_energy_2nd = 19.131
            data = ["I", 53, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Xe", "Xenon", "xenon"] or self.atomicnumber == 54:
            mass_molar = 131.29
            density = 4.49
            v_p = 1090
            shear_mod = 0.0
            bulk_mod = round(v_p**2*density*10**3*10**(-9), 3)
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = 0.0
            thermal_cond = 0.00569
            ionization_energy_1st = 12.130
            data = ["Xe", 54, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Cs", "Caesium", "caesium"] or self.atomicnumber == 55:
            mass_molar = 132.91
            density = 1900
            bulk_mod = 1.6
            young_mod = 1.7
            shear_mod = round((3*bulk_mod*young_mod)/(9*bulk_mod - young_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(21*10**(-8), 10)
            thermal_cond = 36
            ionization_energy_1st = 3.894
            ionization_energy_2nd = 23.157
            data = ["Cs", 55, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ba", "Barium", "barium"] or self.atomicnumber == 56:
            mass_molar = 137.33
            density = 3650
            bulk_mod = 9.6
            shear_mod = 4.9
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(34*10**(-8), 9)
            thermal_cond = 18
            ionization_energy_1st = 5.212
            ionization_energy_2nd = 10.004
            data = ["Ba", 56, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["La", "Lanthanum", "lanthanum"] or self.atomicnumber == 57:
            mass_molar = 138.91
            density = 6160
            bulk_mod = 28
            shear_mod = 14
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(61.5*10**(-8), 9)
            thermal_cond = 13
            ionization_energy_1st = 5.577
            ionization_energy_2nd = 11.059
            data = ["La", 57, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ce", "Cerium", "cerium"] or self.atomicnumber == 58:
            mass_molar = 140.12
            density = 6770
            bulk_mod = 22
            shear_mod = 14
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(74*10**(-8), 9)
            thermal_cond = 11
            ionization_energy_1st = 5.539
            ionization_energy_2nd = 10.850
            data = ["Ce", 58, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Pr", "Prasaeodymium", "prasaeodymium"] or self.atomicnumber == 59:
            mass_molar = 140.91
            density = 6480
            bulk_mod = 29
            shear_mod = 15
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(70*10**(-8), 9)
            thermal_cond = 13
            ionization_energy_1st = 5.473
            ionization_energy_2nd = 10.550
            data = ["Pr", 59, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Nd", "Neodymium", "neodymium"] or self.atomicnumber == 60:
            mass_molar = 144.24
            density = 7000
            bulk_mod = 32
            shear_mod = 16
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(64.3*10**(-8), 9)
            thermal_cond = 17
            ionization_energy_1st = 5.525
            ionization_energy_2nd = 10.720
            data = ["Nd", 60, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Pm", "Promethium", "promethium"] or self.atomicnumber == 61:
            mass_molar = 145
            density = 7220
            bulk_mod = 33
            shear_mod = 18
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(75*10**(-8), 9)
            thermal_cond = 15
            ionization_energy_1st = 5.582
            ionization_energy_2nd = 10.900
            data = ["Pm", 61, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Sm", "Samarium", "samarium"] or self.atomicnumber == 62:
            mass_molar = 150.36
            density = 7540
            bulk_mod = 38
            shear_mod = 20
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(94*10**(-8), 9)
            thermal_cond = 13
            ionization_energy_1st = 5.644
            ionization_energy_2nd = 11.070
            data = ["Sm", 62, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Eu", "Europium", "europium"] or self.atomicnumber == 63:
            mass_molar = 151.96
            density = 5250
            bulk_mod = 8.3
            shear_mod = 7.9
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(90*10**(-8), 9)
            thermal_cond = 14
            ionization_energy_1st = 5.670
            ionization_energy_2nd = 11.250
            data = ["Eu", 63, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Gd", "Gadolinium", "gadolinium"] or self.atomicnumber == 64:
            mass_molar = 157.25
            density = 7890
            bulk_mod = 38
            shear_mod = 22
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(131*10**(-8), 9)
            thermal_cond = 11
            ionization_energy_1st = 6.150
            ionization_energy_2nd = 12.090
            data = ["Gd", 64, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Tb", "Terbium", "terbium"] or self.atomicnumber == 65:
            mass_molar = 158.93
            density = 8250
            bulk_mod = 38.7
            shear_mod = 22
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(115*10**(-8), 9)
            thermal_cond = 11
            ionization_energy_1st = 5.864
            ionization_energy_2nd = 11.520
            data = ["Tb", 65, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Dy", "Dysprosium", "dysprosium"] or self.atomicnumber == 66:
            mass_molar = 162.50
            density = 8560
            bulk_mod = 41
            shear_mod = 25
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(92.6*10**(-8), 9)
            thermal_cond = 11
            ionization_energy_1st = 5.939
            ionization_energy_2nd = 11.670
            data = ["Dy", 66, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ho", "Holmium", "holmium"] or self.atomicnumber == 67:
            mass_molar = 164.93
            density = 8780
            bulk_mod = 40
            shear_mod = 26
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(81.4*10**(-8), 9)
            thermal_cond = 16
            ionization_energy_1st = 6.022
            ionization_energy_2nd = 11.800
            data = ["Ho", 67, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Er", "Erbium", "erbium"] or self.atomicnumber == 68:
            mass_molar = 167.26
            density = 9050
            bulk_mod = 44
            shear_mod = 28
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(86*10**(-8), 9)
            thermal_cond = 15
            ionization_energy_1st = 6.108
            ionization_energy_2nd = 11.930
            data = ["Er", 68, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Tm", "Thulium", "thulium"] or self.atomicnumber == 69:
            mass_molar = 168.93
            density = 9320
            bulk_mod = 45
            shear_mod = 31
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(67.6*10**(-8), 9)
            thermal_cond = 17
            ionization_energy_1st = 6.184
            ionization_energy_2nd = 12.050
            data = ["Tm", 69, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Yb", "Ytterbium", "ytterbium"] or self.atomicnumber == 70:
            mass_molar = 173.05
            density = 6970
            bulk_mod = 31
            shear_mod = 9.9
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(25*10**(-8), 9)
            thermal_cond = 34.9
            ionization_energy_1st = 6.254
            ionization_energy_2nd = 12.176
            data = ["Yb", 70, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Lu", "Lutetium", "lutetium"] or self.atomicnumber == 71:
            mass_molar = 174.97
            density = 9840
            bulk_mod = 48
            shear_mod = 27
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(58*10**(-8), 9)
            thermal_cond = 16
            ionization_energy_1st = 5.426
            ionization_energy_2nd = 13.900
            data = ["Lu", 71, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Hf", "Hafnium", "hafnium"] or self.atomicnumber == 72:
            mass_molar = 178.48
            density = 13310
            bulk_mod = 110
            shear_mod = 30
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(34*10**(-8), 9)
            thermal_cond = 23
            ionization_energy_1st = 6.825
            ionization_energy_2nd = 15.000
            data = ["Hf", 72, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ta", "Tantalum", "tantalum"] or self.atomicnumber == 73:
            mass_molar = 180.95
            density = 16680
            bulk_mod = 200
            shear_mod = 69
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(13.5*10**(-8), 9)
            thermal_cond = 57
            ionization_energy_1st = 7.550
            data = ["Ta", 73, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["W", "Tungsten", "tungsten"] or self.atomicnumber == 74:
            mass_molar = 183.84
            density = 19260
            bulk_mod = 310
            shear_mod = 161
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(5.4*10**(-8), 9)
            thermal_cond = 174
            ionization_energy_1st = 7.980
            data = ["W", 74, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Re", "Rhenium", "rhenium"] or self.atomicnumber == 75:
            mass_molar = 186.21
            density = 21030
            bulk_mod = 370
            shear_mod = 178
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(18*10**(-8), 9)
            thermal_cond = 48
            ionization_energy_1st = 7.834
            data = ["Re", 75, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Os", "Osmium", "osmium"] or self.atomicnumber == 76:
            mass_molar = 190.23
            density = 22590
            shear_mod = 222
            poisson = 0.25
            bulk_mod = round((2*shear_mod*(1+poisson))/(3*(1-2*poisson)), 1)
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(8.1*10**(-8), 9)
            thermal_cond = 88
            ionization_energy_1st = 8.438
            data = ["Os", 76, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Ir", "Iridium", "iridium"] or self.atomicnumber == 77:
            mass_molar = 192.22
            density = 22560
            bulk_mod = 320
            shear_mod = 210
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(4.7*10**(-8), 9)
            thermal_cond = 150
            ionization_energy_1st = 8.967
            data = ["Ir", 77, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Pt", "Platinum", "platinum"] or self.atomicnumber == 78:
            mass_molar = 195.08
            density = 21450
            bulk_mod = 230
            shear_mod = 61
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(10.6*10**(-8), 9)
            thermal_cond = 72
            ionization_energy_1st = 8.959
            ionization_energy_2nd = 18.563
            data = ["Pt", 78, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Au", "Gold", "gold"] or self.atomicnumber == 79:
            mass_molar = 196.97
            density = 19320
            bulk_mod = 220
            shear_mod = 27
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(2.2*10**(-8), 9)
            thermal_cond = 320
            ionization_energy_1st = 9.226
            ionization_energy_2nd = 20.200
            data = ["Au", 79, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Hg", "Mercury", "mercury"] or self.atomicnumber == 80:
            mass_molar = 200.59
            density = 13550
            bulk_mod = 25
            v_p = 1407
            shear_mod = round(0.75*(density*v_p**2 - bulk_mod*10**9)*10**(-9), 1)
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(96*10**(-8), 9)
            thermal_cond = 8.3
            ionization_energy_1st = 10.438
            ionization_energy_2nd = 18.757
            data = ["Hg", 80, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Tl", "Thallium", "thallium"] or self.atomicnumber == 81:
            mass_molar = 204.38
            density = 11850
            bulk_mod = 43
            shear_mod = 2.8
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(15*10**(-8), 9)
            thermal_cond = 46
            ionization_energy_1st = 6.108
            ionization_energy_2nd = 20.428
            data = ["Tl", 81, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Pb", "Lead", "lead"] or self.atomicnumber == 82:
            mass_molar = 207.2
            density = 11340
            bulk_mod = 46
            shear_mod = 5.6
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(21*10**(-8), 9)
            thermal_cond = 35
            ionization_energy_1st = 7.417
            ionization_energy_2nd = 15.032
            data = ["Pb", 82, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Bi", "Bismuth", "bismuth"] or self.atomicnumber == 83:
            mass_molar = 208.98
            density = 9800
            bulk_mod = 31
            shear_mod = 12
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(130*10**(-8), 9)
            thermal_cond = 8
            ionization_energy_1st = 7.286
            ionization_energy_2nd = 16.703
            data = ["Bi", 83, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Po", "Polonium", "polonium"] or self.atomicnumber == 84:
            mass_molar = 209
            density = 9200
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = round(40*10**(-8), 9)
            thermal_cond = 20
            ionization_energy_1st = 8.414
            data = ["Po", 84, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["At", "Astatine", "astatine"] or self.atomicnumber == 85:
            mass_molar = 210
            density = 6400
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = None
            thermal_cond = 1.7
            ionization_energy_1st = 9.318
            ionization_energy_2nd = 20.000
            data = ["At", 85, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Rn", "Radon", "radon"] or self.atomicnumber == 86:
            mass_molar = 222
            density = 9.23
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = None
            thermal_cond = 0.00361
            ionization_energy_1st = 10.749
            data = ["Rn", 86, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Fr", "Francium", "francium"] or self.atomicnumber == 87:
            mass_molar = 223
            density = 348
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = None
            thermal_cond = 15
            ionization_energy_1st = 4.073
            data = ["Fr", 87, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Ra", "Radium", "radium"] or self.atomicnumber == 88:
            mass_molar = 226
            density = 5500
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = round(100*10**(-8), 9)
            thermal_cond = 19
            ionization_energy_1st = 9.318
            ionization_energy_2nd = 10.147
            data = ["Ra", 88, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Ac", "Actinium", "actinium"] or self.atomicnumber == 89:
            mass_molar = 227
            density = 10070
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = None
            thermal_cond = 12
            ionization_energy_1st = 5.170
            ionization_energy_2nd = 11.750
            data = ["Ac", 89, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Th", "Thorium", "thorium"] or self.atomicnumber == 90:
            mass_molar = 232.04
            density = 11720
            bulk_mod = 54
            shear_mod = 31
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(15*10**(-8), 9)
            thermal_cond = 54
            ionization_energy_1st = 6.307
            ionization_energy_2nd = 11.900
            data = ["Th", 90, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Pa", "Protactinium", "protactinium"] or self.atomicnumber == 91:
            mass_molar = 231.04
            density = 15370
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = round(18*10**(-8), 9)
            thermal_cond = 47
            ionization_energy_1st = 5.890
            data = ["Pa", 91, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["U", "Uranium", "uranium"] or self.atomicnumber == 92:
            mass_molar = 238.03
            density = 18970
            bulk_mod = 100
            shear_mod = 111
            young_mod = round((9*bulk_mod*shear_mod)/(3*bulk_mod + shear_mod), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(28*10**(-8), 9)
            thermal_cond = 27.6
            ionization_energy_1st = 6.194
            ionization_energy_2nd = 10.600
            data = ["U", 92, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Np", "Neptunium", "neptunium"] or self.atomicnumber == 93:
            mass_molar = 237
            density = 20480
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = round(120*10**(-8), 9)
            thermal_cond = 6
            ionization_energy_1st = 6.266
            data = ["Np", 93, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Pu", "Plutonium", "plutonium"] or self.atomicnumber == 94:
            mass_molar = 244
            density = 19740
            shear_mod = 43
            young_mod = 96
            bulk_mod = round((young_mod*shear_mod)/(3*(3*shear_mod-young_mod)), 1)
            v_p = round(np.sqrt((bulk_mod*10**9 + 4/3*shear_mod*10**9)/(density)), 2)
            v_s = round(np.sqrt((shear_mod*10**9)/(density)), 2)
            resistivity = round(150*10**(-8), 9)
            thermal_cond = 6
            ionization_energy_1st = 6.026
            ionization_energy_2nd = 11.200
            data = ["Pu", 94, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        elif self.name in ["Am", "Americium", "americium"] or self.atomicnumber == 95:
            mass_molar = 243
            density = 13670
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = None
            thermal_cond = 10
            ionization_energy_1st = 5.974
            data = ["Am", 95, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Cm", "Curium", "curium"] or self.atomicnumber == 96:
            mass_molar = 247
            density = 13510
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = None
            thermal_cond = 10
            ionization_energy_1st = 5.991
            data = ["Cm", 96, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Bk", "Berkelium", "berkelium"] or self.atomicnumber == 97:
            mass_molar = 247
            density = 13250
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = None
            thermal_cond = 10
            ionization_energy_1st = 6.198
            data = ["Bk", 97, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st]
        elif self.name in ["Cf", "Californium", "californium"] or self.atomicnumber == 98:
            mass_molar = 251
            density = 15100
            bulk_mod = None
            shear_mod = None
            young_mod = None
            v_p = None
            v_s = None
            resistivity = None
            thermal_cond = 10
            ionization_energy_1st = 6.282
            ionization_energy_2nd = 11.800
            data = ["Cf", 98, mass_molar, density, bulk_mod, shear_mod, young_mod, v_p, v_s, resistivity,
                    thermal_cond, ionization_energy_1st, ionization_energy_2nd]
        #
        return data