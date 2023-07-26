[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

<a href="https://github.com/MABeeskow/PySILLS">
  <img src="https://raw.githubusercontent.com/MABeeskow/PySILLS/master/documentation/images/PySILLS_Logo_Header.png" width="75%">
</a>

PySILLS is a newly developed, Python-based open source tool for a modern data 
reduction of LA-ICP-MS experiments. It is focused on the compositional analysis 
of major, minor and trace elements of minerals (and glasses) as well as of fluid
and melt inclusions.
PySILLS which was initially part of a M.Sc. thesis project, is developed by 
Maximilian Alexander Beeskow in the work group of Prof. Dr. Thomas Wagner and
Dr. Tobias Fusswinkel at RWTH Aachen University.
PySILLS was inspired conceptionally by the widely-used data reduction tool SILLS.

---

## 🚀 Installation

Coming soon ...

## 💻 Resources

Coming soon ...

[PySILLS on ReadTheDocs](https://pysills.readthedocs.io/en/latest/) |
[PySILLS on Blogger](https://pysills.blogspot.com/) | 
[PySILLS on YouTube](https://www.youtube.com/@PySILLS)

## 💭 Citing PySILLS

Coming soon ...

---

## 💎 Mineral Analysis

PySILLS allows a major, minor and trace element analysis of minerals and glasses. The calculations are based on the 
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
Reference Material (SRM)". It is also necessary to define an internal standard for the standard files.
3. Define the concentration of the internal standard within the mineral. For this purpose, it is possible to calculate
the concentration value based on the amount of a specific oxide, for example 100 % of SiO2, on the amount of an element 
or by importing a csv-file that contains those information.
4. Click on "Run" behind "Auto-Detection" below "Default Time Window (Background)" and "Default Time Window (Matrix)" in
order to get automatically detected calculation intervals for the background and matrix signal.
5. Click on "Apply to all" for the standard and sample files in order to apply a spike elimination on all files.

In theory, all mandatory settings were defined now but it is of course possible to change some parameters now if this is 
needed. We also recommend to check if the automatically set calculation intervals for the background and matrix signal 
were set correctly.

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

## 💎 Fluid Inclusion Analysis

Coming soon ...

### Top Features

Coming soon ...

### Short Step-by-Step Manual

Coming soon ...

### Screenshots

Coming soon ...

## 💎 Melt Inclusion Analysis

Coming soon ...

---

## 📦 PyPitzer

Coming soon ...

[PyPitzer](https://github.com/pypitzer/pypitzer)

---

## 📚 References

Coming soon ...