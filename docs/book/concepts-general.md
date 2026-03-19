# General

The data reduction in *PySILLS* is strongly influenced by the workflow from its precursor *SILLS*. The user has to 
measure external standards, also called standard reference materials, before and after taking sample measurements via 
LA-ICP-MS. 

In *PySILLS*, the user will define different calculation intervals, that correspond to the nature of the 
acquired signal: background, matrix and inclusion signal. The background signal occurs before, after and in between 
shooting the sample. However, it may happen that the average of the background signal does not stay at the same level, 
e.g., 100 cps. The user could either wait, until the background signal has been stabilized itself, or the user should 
consider only the background signal before shooting the sample. Since the background signal can be interpreted as a 
systematic error, it contributes to all other types of signal. Therefore, it is necessary to correct the matrix and 
inclusion signal by the background. These background-corrected signal intensities of the matrix can be used for the 
quantification of the matrix composition. The further analysis of the inclusion composition does require more 
sophisticated algorithms. 

This chapter would like to highlight the theoretical concepts behind the data reduction of complex datasets 
from LA-ICP-MS experiments.

* [Intensity analysis](https://mabeeskow.github.io/PySILLS/concepts-intensity/)
* [Sensitivity analysis](https://mabeeskow.github.io/PySILLS/concepts-sensitivity/)
* [Compositional analysis](https://mabeeskow.github.io/PySILLS/concepts-concentration/)