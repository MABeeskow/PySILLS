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
PySILLS calculates with the arithmetic mean of this interval.

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
:math:`S_i`, the analytical sensitivity :math:`\xi_i^{IS}` and the relative sensitivity factor :math:`R_i`.

Normalized Sensitivity
^^^^^^^^^^^^^^^^^^^^^^^^
Blabla

Analytical Sensitivity
^^^^^^^^^^^^^^^^^^^^^^^^
Blabla

Relative Sensitivity Factor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Blabla

Concentration-related parameters
---------------------------------
More blabla

Concentration
^^^^^^^^^^^^^^^^^
Blabla

Concentration Ratio
^^^^^^^^^^^^^^^^^^^^
Blabla

Limit of Detection
^^^^^^^^^^^^^^^^^^^^
Blabla