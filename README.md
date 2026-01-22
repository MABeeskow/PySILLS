[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-370/) &nbsp;
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0) &nbsp;

<a href="https://github.com/MABeeskow/PySILLS">
  <img src="https://raw.githubusercontent.com/MABeeskow/PySILLS/master/src/pysills/legacy/lib/images/PySILLS_Logo_Header.png" width="75%">
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

### Top Features
The following list shows some of the main features that differentiate PySILLS from alternative data reduction tools.
* works on all common computer systems that can run Python
* use of multiple standard reference materials in one project file
* use of multiple internal standards in one project file
* consideration of isotope-specific standard reference materials
* assemblage definition
* file-specific quick analysis
* intuitive, fast and flexible workflow
* multiple check-up possibilities
* export of processed LA-ICP-MS data (e.g. intensity ratios, analytical sensitivities, etc.) for external calculations
* many quality-of-life features

### Planned Features
The following features extend PySILLS and do not replace already existing features.
* more outlier detection algorithms
* replacement of scattered intensity values by regression curves
* extended language support
* in-built geothermometry analysis
* Jupyter notebooks for a browser-based data reduction of LA-ICP-MS experiments
* production of a video course on YouTube

If you like this project, please consider to follow (click on the star icon above) it.

## 💭 Citing PySILLS

If you have used PySILLS for your work, please use the following citation:

- Maximilian Beeskow, Fusswinkel, T., & Wagner, T. (2026). PySILLS, Python-based and open source data reduction tool for 
the major, minor, and trace element analysis of minerals, fluid and melt inclusions, Zenodo, 
https://doi.org/10.5281/zenodo.8206534

---

## ⚠️ Disclaimer

I am aware of the fact that there are still some bugs and some of them can also cause a crash of the program. But, those
bugs are the reason why I have decided to publish this pre-release version, because, as a developer, I see everywhere 
construction sites in the code, but I would like to know which ones are the most important. So, it is possible that 
different users have different ideas how a mineral or fluid inclusion analysis project should be done. I have developed 
PySILLS with my workflow in my mind. Now, the goal is to make it also applicable for your workflow.

Let's catch the bugs and smash them! 👊

#### Attention
It was necessary to apply some changes concerning the saving/loading algorithm of a project. It is possible that an 
imported project does not contain any information about the acquisition time of the single measurement files. It is 
necessary to add them manually, to save the project again and to restart it finally again. If the user does not restart 
the project, it is possible that further bugs occur.

## 🚀 Installation

A detailed manual about the installation of PySILLS can be found [here](https://docs.google.com/document/d/18nw22PvVRpJvcUNXSThIvXpVhTG6ePhRhZph0nDWVaY/edit?usp=sharing).

PySILLS can be easily installed via the following command:

<code>pip install PySILLS</code>

Alternatively, it is possible to run PySILLS by a manual installation of Python and - if not already installed - the 
following packages:

* numpy
* scipy
* pandas
* matplotlib
* sympy
* (tkinter)

In some cases, it will be necessary to install tkinter manually although it should be actually already part of your 
python version.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) &nbsp;
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) &nbsp;
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white) &nbsp;
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) &nbsp;
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Sympy](https://img.shields.io/badge/SymPy-3B5526.svg?style=for-the-badge&logo=SymPy&logoColor=white) &nbsp;

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) &nbsp;
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0) &nbsp;
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

#### Running PySILLS

PySILLS can be started by running the command <code> python pysills_app.py </code>. If possible, use the newest version 
of PySILLS.

#### Attention (only for Mac OS users)
There is unfortunately a bug concerning the GUI library tkinter and default Python version that is installed on a Mac. 
You will notice this bug for example when you click on a button and for some cases, it will work directly, and for other
cases, you have to click several times on the button or after moving the window a little bit.
In order to avoid this bug, there is the following workaround until Apple will fix this one day:
1) Install the newest version of PySILLS (it will work with Python 3.12). There are several ways to do this but I would
recommend to install it via Homebrew which is a package manager for Mac OS.
2) Install all needed packages explicitly for this newly installed Python version, for example via pip. Example command 
for the installation of numpy for Python 3.12: <code> python3.12 -m pip install numpy </code>.
3) If you run PySILLS now by the command <code> python3.12 pysills_app.py </code>, the previously described bug should 
not appear anymore!

## 💻 Resources

[PySILLS manual (installation)](https://docs.google.com/document/d/18nw22PvVRpJvcUNXSThIvXpVhTG6ePhRhZph0nDWVaY/)\
[PySILLS manual (mineral analysis)](https://docs.google.com/document/d/1u5CkBJiXBnhqsdh7ooiEncuexeBWgP6WDg5X2Am6bOA/)\
[PySILLS manual (fluid inclusion analysis)](https://docs.google.com/document/d/1GeK4aQaiP3D1Na_-7ZUZiBLfzr0wK2mq2888VtTlZIY/)\
[PySILLS manual (melt inclusion analysis)](https://docs.google.com/document/d/15PcfBwTK-dGnMUEiuOhYsKcNpWurOAWnUiKUSeNjtN8/)

[PySILLS on ReadTheDocs](https://pysills.readthedocs.io/en/latest/)\
[PySILLS on Blogger](https://pysills.blogspot.com/)\
[PySILLS on YouTube](https://www.youtube.com/@PySILLS)\
[PySILLS on PyPi](https://pypi.org/project/PySILLS/)

![Blogger](https://img.shields.io/badge/Blogger-FF5722?style=for-the-badge&logo=blogger&logoColor=white) &nbsp;
![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)

---

## 💎 Mineral Analysis

PySILLS allows the major, minor and trace element analysis of minerals and glasses. The calculations are based on the 
measured intensity signals and sensitivities of the ICP-MS instrument.

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

PySILLS does not only allow the major, minor and trace element analysis of (homogenous) solid phases like minerals and 
glasses but also from fluid inclusions.

### Short Step-by-Step Manual

In addition to a more detailed manual, I would like to describe briefly here which steps are necessary for 
a complete data reduction of a fluid inclusion analysis project.

#### Data import
1. Select the correct analysis mode. In this case, select "Fluid Inclusion Analysis" below "Select Mode".
2. Import the measurement files by clicking on "Add" below "Standard Files" and "Sample Files".

#### Project setup
1. Click on "Settings". A new window will be opened.

On the left side of the settings window, you can define some default parameters and features that influence the whole 
dataset, for example a spike elimination.

2. Select a default standard reference material (SRM) for the standard files and isotopes below the header "Standard 
Reference Material (SRM)".
3. Define the matrix by setting a concentration value for the internal standard of the matrix which will be used for 
example if the "Matrix-only Tracer" quantification method was selected.
4. Define the settings for the quantification method, for example the "Matrix-only Tracer" algorithm.
5. Click on "Run" behind "Auto-Detection" below "Default Time Window (Background)" in order to get automatically 
detected calculation intervals for the background signal. If you are very sure when the laser started and ended, you can 
also define manually the time limits of the calculation windows.
6. Click on "Apply to all" for the standard and sample files in order to apply a spike elimination on all files.
7. Open every standard and sample file and define the calculation intervals for the matrix and inclusion signal.
8. Define the concentration values of the internal standard that was selected for the sample files (this will be used 
for the fluid inclusion analysis). There are several options available, for example a mass balance calculation or a 
calculation based on PyPitzer.

Now, all mandatory settings were defined, but it is of course possible to change some parameters if this is 
necessary.

#### Project results
After all settings were defined, it is now finally possible to calculate the results of this fluid inclusion analysis 
project.

1. Click on "Results" below "Fluid Inclusion Analysis" in the main window of PySILLS. A new window will be opened.

The user can now specify which results should be displayed in the table, for example the concentration values for the 
smoothed (spike eliminated) sample files. Of course, the final step is to create a report file that contains all 
results.

2. Click on "Export Results" in order to collect and export all data in a created report file. This file contains all 
possible values that can be displayed in the table. 

### Screenshots

Coming soon ...

## 📦 PyPitzer

PyPitzer allows thermodynamic modeling of fluid inclusion systems based on the Pitzer model. The quantification of those
systems requires microthermometric data as well as element/Na ratios from LA-ICP-MS experiments. PyPitzer is able to 
calculate precise concentrations of fluid inclusion compositions for also complex multi-element systems.
It is possible to use an already fully implemented version of PyPitzer in PySILLS or to use it externally which means 
that the user can export the necessary LA-ICP-MS data and import then the calculated Na concentrations.

[PyPitzer](https://github.com/pypitzer/pypitzer)

---

## 💎 Melt Inclusion Analysis

PySILLS does not only allow the major, minor and trace element analysis of (homogenous) solid phases and fluid 
inclusions but also from melt inclusions.

### Short Step-by-Step Manual

In addition to a more detailed manual, I would like to describe briefly here which steps are necessary for 
a complete data reduction of a melt inclusion analysis project.

#### Data import
1. Select the correct analysis mode. In this case, select "Melt Inclusion Analysis" below "Select Mode".
2. Import the measurement files by clicking on "Add" below "Standard Files" and "Sample Files".

#### Project setup
1. Click on "Settings". A new window will be opened.

On the left side of the settings window, you can define some default parameters and features that influence the whole 
dataset, for example a spike elimination.

2. Select a default standard reference material (SRM) for the standard files and isotopes below the header "Standard 
Reference Material (SRM)".
3. Define the matrix by setting a concentration value for the internal standard of the matrix which will be used for 
example if the "Matrix-only Tracer" quantification method was selected.
4. Define the settings for the quantification method, for example the "Matrix-only Tracer" algorithm.
5. Click on "Run" behind "Auto-Detection" below "Default Time Window (Background)" and "Default Time Window (Matrix)" 
in order to get automatically detected calculation intervals for the background/matrix signal. If you are very sure 
when the laser started and ended, you can also define manually the time limits of the calculation windows.
6. Click on "Apply to all" for the standard and sample files in order to apply a spike elimination on all files.
7. Open every standard and sample file and define the calculation intervals for the missing matrix and inclusion signal.
8. Define the concentration values of the internal standard that was selected for the sample files (this will be used 
for the melt inclusion analysis). There are several options available, for example the quantification based on a 100 
wt.% oxides normalization.

Now, all mandatory settings were defined, but it is of course possible to change some parameters if this is 
necessary.

#### Project results
After all settings were defined, it is now finally possible to calculate the results of this fluid inclusion analysis 
project.

1. Click on "Results" below "Melt Inclusion Analysis" in the main window of PySILLS. A new window will be opened.

The user can now specify which results should be displayed in the table, for example the concentration values for the 
smoothed (spike eliminated) sample files. Of course, the final step is to create a report file that contains all 
results.

2. Click on "Export Results" in order to collect and export all data in a created report file. This file contains all 
possible values that can be displayed in the table. 

---

## 📚 References

* Heinrich, C.A., et al., 2003, "Quantitative multi-element analysis of minerals, fluid and melt inclusions by 
laser-ablation inductively-coupled-plasma mass-spectrometry", Geochimica et Cosmochimica Acta, 67, pp. 3473-3496, 
[Link](https://www.sciencedirect.com/science/article/pii/S001670370300084X)
* Guillong, M., et al., 2008, "SILLS: A MATLAB-based program for the reduction of Laser ablation ICP-MS data of 
homogenous materials and inclusions", Mineralogical Association of Canada Short Course, 40, pp. 323-333, [Link](
https://ethz.ch/content/dam/ethz/special-interest/erdw/geopetro/mineralsystems-dam/documents/MAC_SC_40_Sills_description.pdf)
* Liu, Y., et al., 2024, "An integrated approach for quantifiying fluid inclusion data combining microthermometry, 
LA-ICP-MS, and thermodynamic modeling", Chemical Geology, 644, pp. 1-18, [Link](
https://www.sciencedirect.com/science/article/pii/S0009254123005648?via%3Dihub)
* Longerich, H.P., et al., 1996, "Laser Ablation Inductively Coupled Plasma Mass Spectrometric Transient Signal Data 
Acquisition and Analyte Concentration Calculation", Journal of Analytical Atomic Spectrometry, 11, pp. 899-904, [Link](
https://www.scopus.com/record/display.uri?eid=2-s2.0-0030245362&origin=inward&txGid=a8ec37914d0f3f4ed5d97cd7db187e41)
* Pettke, T., et al., 2012, "Recent developments in element concentration and isotope ratio analysis of individual fluid 
inclusions by laser ablation single and multiple collector ICP-MS", Ore Geology Reviews, 44, pp. 10-38, [Link](
https://www.sciencedirect.com/science/article/abs/pii/S016913681100134X)

---

Last updated: 22.01.2026