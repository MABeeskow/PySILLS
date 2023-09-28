.. _theory_ref:

Theoretical background
=========================

Blabla

Intensity-related parameters
------------------------------
The ICP-MS machine measures the signal intensity of an isotope that was counted on the detector.
Its unit is cps or "counts per second". In order to be able to calculate the concentration of a
specific element within a mineral, it is necessary to process these signal intensity values further.
For the analysis of minerals, glasses and other homogenous solid phases, the user has to define a background
signal interval and a sample signal interval. Then, it is possible to calculate a background-corrected signal intensity
for the sample interval which is free from a background-based offset.

Background Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The background intensity :math:`I_{BG,i}` is defined by the background signal interval which was defined by the user.
PySILLS calculates with the arithmetic mean of this interval. The presented equations are always the same for standard
files and sample files.

Background-corrected Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The background-corrected intensity :math:`I_i` is the difference between the signal intensity of the sample interval
:math:`I_{SMPL,i}` and the background intensity :math:`I_{BG,i}`. Both parameters are the arithmetic mean of those
intervals.

.. math::
    I_i = I_{SMPL,i} - I_{BG,i}

Intensity Ratio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The intensity ratio is the ratio between the background-corrected intensities of isotope :math:`i` and the internal
standard :math:`IS`.

.. math::
    \tilde{I}_i = \frac{I_i}{I_{IS}}

Sensitivity-related parameters
--------------------------------
In order to be able to calculate the concentration of isotope :math:`i` within a sample, it is necessary to build a
connection between the measured signal intensities and the desired concentrations. This link is the sensitivity of an
ICP-MS instrument. There are three different sensitivities that can be calculated in PySILLS: the normalized sensitivity
:math:`S_i`, the analytical sensitivity :math:`\xi_i^{IS}` and the relative sensitivity factor :math:`R_i`. The
presented equations are different for standard files and sample files.

Normalized Sensitivity
^^^^^^^^^^^^^^^^^^^^^^^^
Standard Files
''''''''''''''''
.. math::
    S_{i}^{STD} = \frac{I_{i}^{STD}}{C_{i}^{STD}}

Sample Files
''''''''''''''
.. math::
    S_{i}^{SMPL} = \xi_i^{IS} \cdot \frac{I_{i}^{SMPL}}{C_{i}^{SMPL}}

Analytical Sensitivity
^^^^^^^^^^^^^^^^^^^^^^^^
Standard Files
''''''''''''''''
.. math::
    \xi_{i}^{IS} = \frac{I_{i}^{STD}}{I_{IS}^{STD}} \cdot \frac{C_{IS}^{STD}}{C_{i}^{STD}}

Sample Files
''''''''''''''
Since an ICP-MS machine has a sensitivity drift over time, it is necessary to calculate a linear regression through all
measured standard files, in order to get an analytical sensitivity value at the time of a measured sample file.

Relative Sensitivity Factor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Standard Files
''''''''''''''''
The relative sensitivity factor is one for all isotopes that were measured in a standard reference material.

.. math::
    R_{i}^{STD} = 1

Sample Files
''''''''''''''
.. math::
    R_{i}^{SMPL} = \xi_{i}^{IS} \cdot \frac{C_{i}^{STD}}{I_{i}^{STD}} \cdot \frac{I_{IS}^{SMPL}}{C_{IS}^{SMPL}}

Concentration-related parameters
---------------------------------
More blabla

Concentration
^^^^^^^^^^^^^^^^^
Standard Files
''''''''''''''''
The concentration value of isotope :math:`i` within a measured standard reference material is constant and defined by
its database. The measured signal intensities have no influence on the concentration values of standard measurements.

Sample Files
''''''''''''''
With the exception of the concentration value of the internal standard :math:`IS` which has to be measured or estimated
separately, the concentration of isotope :math:`i` within a sample can be calculated by a quite simple equation
connecting signal intensities, analytical sensitivity and internal standard concentration.

.. math::
    C_{i}^{SMPL} = \frac{I_{i}^{SMPL}}{I_{IS}^{SMPL}} \cdot \frac{C_{IS}^{SMPL}}{\xi_{i}^{IS}}

Concentration Ratio
^^^^^^^^^^^^^^^^^^^^
The intensity ratio is the ratio between the concentrations of isotope :math:`i` and the internal standard :math:`IS`.

.. math::
    \tilde{C}_i = \frac{C_i}{C_{IS}}

Limit of Detection
^^^^^^^^^^^^^^^^^^^^
Standard Files
''''''''''''''''
.. rubric:: Longerich et al. (1996)

Blabla

.. rubric:: Pettke et al. (2012)

Blabla

Sample Files
''''''''''''''
.. rubric:: Longerich et al. (1996)

Blabla

.. rubric:: Pettke et al. (2012)

Blabla
