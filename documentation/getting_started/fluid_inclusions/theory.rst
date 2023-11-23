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
The background intensity :math:`I_{i}^{BG}` is defined by the background signal interval which was defined by the user.
PySILLS calculates with the arithmetic mean of this interval. The presented equations are always the same for standard
files and sample files.

.. math::
    I_{i}^{BG} = I_{i}^{SIG1}

Background-corrected Matrix Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The background-corrected matrix intensity :math:`I_{i}^{MAT2}` is the difference between the signal intensity of the matrix
interval :math:`I_{i}^{SIG2}` and the background intensity :math:`I_{i}^{BG}`. Both parameters are the arithmetic mean of
those intervals.

.. math::
    I_{i}^{MAT} = I_{i}^{MAT2} = I_{i}^{SIG2} - I_{i}^{BG}

Composition of the Total Inclusion Signal Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The total inclusion signal intensity :math:`I_{i}^{SIG3}` is composed by the contributions of the background, the matrix
and the inclusion itself.

.. math::
    I_{i}^{SIG3} = I_{i}^{BG} + I_{i}^{MAT3} + I_{i}^{INCL}

Mixed Signal Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The mixed signal intensity :math:`I_{i}^{MIX}` is composed by the contributions of the matrix and the inclusion itself.

.. math::
    I_{i}^{MIX} = I_{i}^{MAT3} + I_{i}^{INCL}

Therefore, it can be easily calculated by reducing the total inclusion signal intensity :math:`I_{i}^{SIG3}` by the
background intensity.

.. math::
    I_{i}^{MIX} = I_{i}^{SIG3} - I_{i}^{BG}

Matrix Contribution to the Total Inclusion Signal Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The matrix contribution :math:`I_{i}^{MAT3}` to the total inclusion signal intensity :math:`I_{i}^{SIG3}` is already a
little bit tricky to determine, since it requires an element which is only present in the matrix but not in the
inclusion ("matrix-only tracer"). We call this matrix-only tracer element :math:`t`.

.. math::
    I_{t}^{MAT3} = I_{t}^{SIG3} - I_{t}^{BG} = I_{t}^{MIX}

Now, the calculation of this signal contribution is also possible for all other elements.

.. math::
    I_{i}^{MAT3} = I_{t}^{MAT3} \cdot \frac{I_{i}^{MAT}}{I_{t}^{MAT}}

Background- and Matrix-corrected Inclusion Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The background- and matrix-corrected inclusion intensity :math:`I_{i}^{INCL}` can be calculated on at least four different
ways that are available in PySILLS.

Method 1 - (after Heinrich et al. 2003)
''''''''''''''''
.. math::
    I_{i}^{INCL} = I_{i}^{MIX} - I_{t}^{MIX} \cdot \frac{I_{i}^{MAT}}{I_{t}^{MAT}}

Method 2 - (after SILLS Equation Sheet)
''''''''''''''''
.. math::
    I_{i}^{INCL} = I_{i}^{MIX} - I_{i}^{MAT3}

Method 3 - (after SILLS Equation Sheet)
''''''''''''''''
.. math::
    I_{i}^{INCL} = I_{i}^{MIX} - r \cdot I_{i}^{MAT}

The factor R can be calculated by the following equation.

.. math::
    r = \frac{I_{t}^{MIX}}{I_{t}^{MAT}}

Method 4 - (after the theoretical composition of the total inclusion signal intensity)
''''''''''''''''
.. math::
    I_{i}^{INCL} = I_{i}^{SIG3} - I_{i}^{BG} - I_{i}^{MAT3}

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
    \xi_{i}^{IS} = \frac{S_{i}^{STD}}{S_{IS}^{STD}} = \frac{I_{i}^{STD}}{I_{IS}^{STD}} \cdot \frac{C_{IS}^{STD}}{C_{i}^{STD}}

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
    R_{i}^{MAT} = R_{i}^{MAT2} = \xi_{i}^{IS} \cdot \frac{C_{i}^{STD}}{I_{i}^{STD}} \cdot \frac{I_{IS}^{MAT}}{C_{IS}^{MAT}}

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
    C_{i}^{MIX} = (1 - x) \cdot C_{i}^{MAT} + x \cdot C_{i}^{INCL} = \frac{I_{i}^{MIX}}{I_{IS}^{MIX}} \cdot \frac{C_{IS}^{MIX}}{\xi_{i}^{IS}}
.. math::
    C_{t}^{MIX} = (1 - x) \cdot C_{t}^{MAT}
.. math::
    C_{IS}^{MIX} = (1 - x) \cdot C_{IS}^{MAT} + x \cdot C_{IS}^{INCL}

In order to be able to calculate the mixed concentration but also the inclusion concentration with respect to the
equations of SILLS, it is necessary to calculate :math:`x` which cannot determined directly, so that another factor
called :math:`a` has to be calculated before.

.. rubric:: Inclusion Concentration
The inclusion concentration can be calculated by at least three different equations that are available in PySILLS.

.. rubric:: Method 1 - Simple Signals (after SILLS Equation Sheet)
.. math::
    C_{i}^{INCL} = \frac{I_{i}^{INCL}}{I_{IS}^{INCL}} \cdot \frac{C_{IS}^{INCL}}{\xi_{i}^{IS}}

.. rubric:: Method 2 & 3 - Matrix-Only-Tracer and Second Internal Standard (after SILLS Equation Sheet)
.. math::
    C_{i}^{INCL} = \frac{1}{x} \cdot \left( C_{i}^{MIX} + (x - 1) \cdot C_{i}^{MAT} \right)

.. math::
    C_{i}^{INCL} = \frac{1}{x \cdot \xi_{i}^{IS}} \cdot \left( \frac{C_{IS}^{MIX}}{I_{IS}^{MIX}} \cdot I_{i}^{MIX} + (x - 1) \cdot \frac{C_{IS}^{MAT}}{I_{IS}^{MAT}} \cdot I_{i}^{MAT} \right)

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