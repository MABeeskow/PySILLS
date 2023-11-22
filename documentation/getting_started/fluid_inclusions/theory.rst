.. _theory_ref:

Theoretical background
=========================

Blabla

Intensity-related parameters
------------------------------
The ICP-MS machine measures the signal intensity of an isotope that was counted on the detector.
Its unit is cps or "counts per second". In order to be able to calculate the concentration of a
specific element within a fluid inclusion, it is necessary to process these signal intensity values further.
For the analysis of fluid inclusions, the user has to define a background
signal interval, an inclusion signal interval and two matrix signal intervals. Then, it is possible to calculate a
background-corrected and also matrix-corrected signal intensities. The analysis of fluid inclusions requires many
different signal intensities which will be presented in the following subchapters.

Background Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The background intensity :math:`I_{BG,i}` is defined by the background signal interval which was defined by the user.
PySILLS calculates with the arithmetic mean of this interval. The presented equations are always the same for standard
files and sample files.

.. math::
    I_{BG,i} = I_{SIG1,i}

Background-corrected Matrix Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The background-corrected matrix intensity :math:`I_{MAT2,i}` is the difference between the signal intensity of the matrix
interval :math:`I_{SIG2,i}` and the background intensity :math:`I_{BG,i}`. Both parameters are the arithmetic mean of
those intervals.

.. math::
    I_{MAT2,i} = I_{SIG2,i} - I_{BG,i}

Composition of the Total Inclusion Signal Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The total inclusion signal intensity :math:`I_{SIG3,i}` is composed by the contributions of the background, the matrix
and the inclusion itself.

.. math::
    I_{SIG3,i} = I_{BG,i} + I_{MAT,INCL,i} + I_{INCL,i}

Mixed Signal Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The mixed signal intensity :math:`I_{MIX,i}` is composed by the contributions of the matrix and the inclusion itself.

.. math::
    I_{MIX,i} = I_{MAT3,i} + I_{INCL,i}

Therefore, it can be easily calculated by reducing the total inclusion signal intensity :math:`I_{SIG3,i}` by the
background intensity.

.. math::
    I_{MIX,i} = I_{SIG3,i} - I_{BG,i}

Matrix Contribution to the Total Inclusion Signal Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The matrix contribution :math:`I_{MAT3,i}` to the total inclusion signal intensity :math:`I_{SIG3,i}` is already a
little bit tricky to determine, since it requires an element which is only present in the matrix but not in the
inclusion ("matrix-only tracer"). We call this matrix-only tracer element :math:`t`.

.. math::
    I_{MAT3,t} = I_{SIG3,t} - I_{BG,t} = I_{MIX,t}

Now, the calculation of this signal contribution is also possible for all other elements.

.. math::
    I_{MAT3,i} = I_{MAT3,t} \cdot \frac{I_{MAT2,i}}{I_{MAT2,t}}

Background- and Matrix-corrected Inclusion Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The background- and matrix-corrected inclusion intensity :math:`I_{INCL,i}` can be calculated on at least four different
ways that are available in PySILLS.

Method 1 - (after Heinrich et al. 2003)
''''''''''''''''
.. math::
    I_{INCL,i} = I_{MIX,i} - I_{MIX,t} \cdot \frac{I_{MAT2,i}}{I_{MAT2,t}}

Method 2 - (after SILLS Equation Sheet)
''''''''''''''''
.. math::
    I_{INCL,i} = I_{MIX,i} - I_{MAT3,i}

Method 3 - (after SILLS Equation Sheet)
''''''''''''''''
.. math::
    I_{INCL,i} = I_{MIX,i} - r \cdot I_{MAT2,i}

The factor R can be calculated by the following equation.

.. math::
    r = \frac{I_{MIX,t}}{I_{MAT2,t}}

Method 4 - (after the theoretical composition of the total inclusion signal intensity)
''''''''''''''''
.. math::
    I_{INCL,i} = I_{SIG3,i} - I_{BG,i} - I_{MAT3,i}

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
.. rubric:: Matrix Signal
.. math::
    R_{i}^{MAT} = R_{i}^{MAT2} = \xi_{i}^{IS} \cdot \frac{C_{i}^{STD}}{I_{i}^{STD}} \cdot \frac{I_{IS}^{MAT2}}{C_{IS}^{MAT2}}

.. rubric:: Mixed Signal
.. math::
    R_{i}^{MIX} = \xi_{i}^{IS} \cdot \frac{C_{i}^{STD}}{I_{i}^{STD}} \cdot \frac{I_{IS}^{MIX}}{C_{IS}^{MIX}}

.. rubric:: Inclusion Signal
.. math::
    R_{i}^{INCL} = \xi_{i}^{IS} \cdot \frac{C_{i}^{STD}}{I_{i}^{STD}} \cdot \frac{I_{IS}^{INCL}}{C_{IS}^{INCL}}

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
separately, the concentration of isotope :math:`i` can be calculated by different equations that depend from the user's
settings.

.. rubric:: Matrix Concentration
.. math::
    C_{i}^{MAT} = C_{i}^{MAT2} = \frac{I_{i}^{MAT2}}{I_{IS}^{MAT2}} \cdot \frac{C_{IS}^{MAT2}}{\xi_{i}^{IS}}

.. rubric:: Mixed Concentration
.. math::
    C_{i}^{MIX} = (1 - x) \cdot C_{i}^{MAT} + x \cdot C_{i}^{INCL}
.. math::
    C_{t}^{MIX} = (1 - x) \cdot C_{t}^{MAT}
.. math::
    C_{IS}^{MIX} = (1 - x) \cdot C_{IS}^{MAT} + x \cdot C_{IS}^{INCL}

In order to be able to calculate the mixed concentration but also the inclusion concentration with respect to the
equations of SILLS, it is necessary to calculate :math:`x` which cannot determined directly, so that another factor
called :math:`a` has to be calculated before.

.. math::
    a = \frac{C_{t}^{MIX}}{C_{IS}^{MIX}} = \frac{I_{t}^{MIX}}{I_{IS}^{MIX}} \cdot \frac{1}{\xi_{t}^{IS}}

.. math::
    x = \frac{C_{t}^{MAT} -  a \cdot C_{IS}^{MAT}}{C_{t}^{MAT} - a \cdot C_{IS}^{MAT} + a \cdot C_{IS}^{INCL}}

.. rubric:: Inclusion Concentration
The inclusion concentration can be calculated by at least three different equations that are available in PySILLS.

.. rubric:: Method 1 - Simple Signals (after SILLS Equation Sheet)
.. math::
    C_{i}^{INCL} = \frac{I_{i}^{INCL}}{I_{IS}^{INCL}} \cdot \frac{C_{IS}^{INCL}}{\xi_{i}^{IS}}

.. rubric:: Method 2 - Matrix-Only-Tracer and Second Internal Standard (after SILLS Equation Sheet)
.. math::
    C_{i}^{INCL} = \frac{1}{x} \cdot \left( \frac{C_{IS}^{MIX}}{I_{IS}^{MIX}} \cdot \frac{I_{i}^{MIX}}{\xi_{i}^{IS}} + (x - 1) \cdot \frac{C_{IS}^{MAT}}{I_{IS}^{MAT}} \cdot \frac{I_{i}^{MAT}}{\xi_{i}^{IS}} \right)

The difference between these two methods is the determination of :math:`x`.

Mixed Concentration Ratio a and Mixing Ratio x
''''''''''''''
The mixed concentration ratio :math:`a` is necessary for the determination of the mixing ratio :math:`x`.

.. rubric:: Method 1 - Matrix-Only-Tracer (after SILLS Equation Sheet)
.. math::
    a = \frac{C_{t}^{MIX}}{C_{IS}^{MIX}} = \frac{I_{t}^{MIX}}{I_{IS}^{MIX}} \cdot \frac{1}{\xi_{t}^{IS}}

.. math::
    x = \frac{C_{t}^{MAT} -  a \cdot C_{IS}^{MAT}}{C_{t}^{MAT} - a \cdot C_{IS}^{MAT} + a \cdot C_{IS}^{INCL}}

.. rubric:: Method 2 - Second Internal Standard (after SILLS Equation Sheet)
.. math::
    a = \frac{C_{IS2}^{MIX}}{C_{IS1}^{MIX}} = \frac{I_{IS2}^{MIX}}{I_{IS1}^{MIX}} \cdot \frac{1}{\xi_{IS2}^{IS1}}

.. math::
    x = \frac{C_{IS2}^{MAT} -  a \cdot C_{IS1}^{MAT}}{C_{IS2}^{MAT} - C_{IS2}^{INCL} - a \cdot C_{IS1}^{MAT} + a \cdot C_{IS1}^{INCL}}

Limit of Detection
^^^^^^^^^^^^^^^^^^^^
Standard Files
''''''''''''''''
.. rubric:: Longerich et al. (1996)

.. math::
    L_{i}^{STD} = 3 \sigma_{i}^{BG} \cdot \frac{C_{i}^{STD}}{I_{i}^{STD}} \cdot \sqrt{\frac{1}{N_{BG}} + \frac{1}{N_{SMPL}}}

.. rubric:: Pettke et al. (2012)

.. math::
    L_{i}^{STD} = \frac{3.29 \cdot \sqrt{\hat{I}_{i}^{BG} \cdot \tau_i \cdot N_{SMPL} \cdot (1 + N_{SMPL}/N_{BG})} + 2.71}{N_{SMPL} \cdot \tau_i} \cdot \frac{C_{i}^{STD}}{I_{i}^{STD}}

Sample Files
''''''''''''''
.. rubric:: Longerich et al. (1996)

.. math::
    L_{i}^{SMPL} = \frac{3 \sigma_{i}^{BG}}{\xi_{i}^{IS}} \cdot \frac{C_{IS}^{SMPL}}{I_{IS}^{SMPL}} \cdot \sqrt{\frac{1}{N_{BG}} + \frac{1}{N_{SMPL}}}

.. rubric:: Pettke et al. (2012)

.. math::
    L_{i}^{SMPL} = \frac{3.29 \cdot \sqrt{\hat{I}_{i}^{BG} \cdot \tau_i \cdot N_{SMPL} \cdot (1 + N_{SMPL}/N_{BG})} + 2.71}{N_{SMPL} \cdot \tau_i \cdot \xi_{i}^{IS}} \cdot \frac{C_{IS}^{SMPL}}{I_{IS}^{SMPL}}