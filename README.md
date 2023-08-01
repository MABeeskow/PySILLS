[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) &nbsp;
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0) &nbsp;
[![DOI](https://zenodo.org/badge/663565362.svg)](https://zenodo.org/badge/latestdoi/663565362)

<a href="https://github.com/MABeeskow/PySILLS">
  <img src="https://raw.githubusercontent.com/MABeeskow/PySILLS/master/documentation/images/PySILLS_Logo_Header.png" width="75%">
</a>

developed by Maximilian Alexander Beeskow

PySILLS is a newly developed, Python-based open source tool for a modern data 
reduction of LA-ICP-MS experiments. It is focused on the compositional analysis 
of major, minor and trace elements of minerals (and glasses) as well as of fluid
and melt inclusions.
PySILLS which was initially part of a M.Sc. thesis project, is developed by 
Maximilian Alexander Beeskow in the work group of Prof. Dr. Thomas Wagner and
Dr. Tobias Fusswinkel at RWTH Aachen University.
PySILLS was inspired conceptionally by the widely-used data reduction tool SILLS.

---

## ⚠️ Pre-release comment / disclaimer

I am aware of the fact that there are still some bugs and some of them can also cause a crash of the program. But, those
bugs are the reason why I have decided to publish this pre-release version, because, as a developer, I see everywhere 
construction sites in the code, but I would like to know which ones are the most important. So, it is possible that 
different users have different ideas how a mineral or fluid inclusion analysis project should be done. I have developed 
PySILLS with my workflow in my mind. Now, the goal is to make it also applicable for your workflow.

Let's catch the bugs and smash them! 👊

## 🚀 Installation

It is planned that PySILLS will be able to install via PyPi and conda, since all required dependencies will then be 
installed automatically.

Alternatively, it is possible to run PySILLS by a manual installation of Python and - if not already installed - the 
following packages:

* numpy
* scipy
* pandas
* matplotlib

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) &nbsp;
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) &nbsp;
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white) &nbsp;
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) &nbsp;
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) &nbsp;
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0) &nbsp;
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

## 💻 Resources

Coming soon ...

[PySILLS on ReadTheDocs](https://pysills.readthedocs.io/en/latest/) |
[PySILLS on Blogger](https://pysills.blogspot.com/) | 
[PySILLS on YouTube](https://www.youtube.com/@PySILLS)

![Blogger](https://img.shields.io/badge/Blogger-FF5722?style=for-the-badge&logo=blogger&logoColor=white) &nbsp;
![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)

## 💭 Citing PySILLS

Coming soon ...

[![DOI](https://zenodo.org/badge/663565362.svg)](https://zenodo.org/badge/latestdoi/663565362)

---

## 💎 Mineral Analysis

PySILLS allows the major, minor and trace element analysis of minerals and glasses. The calculations are based on the 
measured intensity signals and sensitivities of the ICP-MS instrument.

### Top Features

* use of multiple standard reference materials in one project file
* use of multiple internal standards in one project file
* consideration of isotope-specific standard reference materials
* assemblage definition
* file-specific quick analysis
* intuitive, fast and flexible workflow
* multiple check-up possibilities

### Short Step-by-Step Manual

In addition to a more detailed manual, I would like to describe briefly here which steps are necessary for 
a complete data reduction of a mineral analysis project.

#### Data import
1. Select the correct analysis mode. In this case, select "Mineral Analysis" below "Select Mode".
2. Import the measurement files by clicking on "Add" below "Standard Files" and "Sample Files".

#### Project setup
1. Click on "Settings". A new window will be opened.

On the left side of the settings window, you can define some default parameters and features that influence the whole 
dataset, for example a spike elimination.

2. Select a default standard reference material (SRM) for the standard files and isotopes below the header "Standard 
Reference Material (SRM)".
3. Define the concentration of the internal standard. For this purpose, it is possible to calculate the concentration 
value based on the amount of a specific oxide, for example 100 % of SiO2, on the amount of an element, by importing 
a csv-file containing the needed information or by defining the internal standard and its concentration manually.
4. Click on "Run" behind "Auto-Detection" below "Default Time Window (Background)" and "Default Time Window (Matrix)" in
order to get automatically detected calculation intervals for the background and matrix signal. If you are very sure 
when the laser started and ended, you can also define manually the time limits of the calculation windows.
5. Click on "Apply to all" for the standard and sample files in order to apply a spike elimination on all files.

In theory, all mandatory settings were defined now, but it is of course possible to change some parameters if this is 
necessary. We also recommend to check if the automatically set calculation intervals for the background and matrix 
signal were set correctly.

#### Project results
After all settings were defined, it is now finally possible to calculate the results of this mineral analysis project.

1. Click on "Results" below "Mineral Analysis" in the main window of PySILLS. A new window will be opened.

The user can now specify which results should be displayed in the table, for example the concentration values for the 
smoothed (spike eliminated) sample files. Of course, the final step is to create a report file that contains all 
results.

2. Click on "Export Results" in order to collect and export all data in a created report file. This file contains all 
possible values that can be displayed in the table. 

### Screenshots

Coming soon ...

---

## 💎 Fluid Inclusion Analysis

Coming soon ...

### Top Features

Coming soon ...

### Short Step-by-Step Manual

Coming soon ...

### Screenshots

Coming soon ...

## 📦 PyPitzer

PyPitzer allows thermodynamic modeling of fluid inclusion systems based on the Pitzer model. The quantification of those
systems requires microthermometric data as well as element/Na ratios from LA-ICP-MS experiments. PyPitzer is able to 
calculate precise concentrations of fluid inclusion compositions for also complex multi-element systems.
The calculated results of PyPitzer can be imported in PySILLS. It is planned to integrate PyPitzer in PySILLS in the 
future.

[PyPitzer](https://github.com/pypitzer/pypitzer)

---

## 💎 Melt Inclusion Analysis

Coming soon ...

---

## 📚 References

* Heinrich, C.A., et al., 2003, "Quantitative multi-element analysis of minerals, fluid and melt inclusions by 
laser-ablation inductively-coupled-plasma mass-spectrometry", Geochimica et Cosmochimica Acta, 67, pp. 3473-3496, 
[Link](https://www.sciencedirect.com/science/article/pii/S001670370300084X)
* Guillong, M., et al., 2008, "SILLS: A MATLAB-based program for the reduction of Laser ablation ICP-MS data of 
homogenous materials and inclusions", Mineralogical Association of Canada Short Course, 40, pp. 323-333, [Link](
https://ethz.ch/content/dam/ethz/special-interest/erdw/geopetro/mineralsystems-dam/documents/MAC_SC_40_Sills_description.pdf)
* Longerich, H.P., et al., 1996, "Laser Ablation Inductively Coupled Plasma Mass Spectrometric Transient Signal Data 
Acquisition and Analyte Concentration Calculation", Journal of Analytical Atomic Spectrometry, 11, pp. 899-904, [Link](
https://www.scopus.com/record/display.uri?eid=2-s2.0-0030245362&origin=inward&txGid=a8ec37914d0f3f4ed5d97cd7db187e41)
* Pettke, T., et al., 2012, "Recent developments in element concentration and isotope ratio analysis of individual fluid 
inclusions by laser ablation single and multiple collector ICP-MS", Ore Geology Reviews, 44, pp. 10-38, [Link](
https://www.sciencedirect.com/science/article/abs/pii/S016913681100134X)