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
The background-corrected matrix intensity :math:`I_{MAT,i}` is the difference between the signal intensity of the matrix
interval :math:`I_{SIG2,i}` and the background intensity :math:`I_{BG,i}`. Both parameters are the arithmetic mean of
those intervals.

.. math::
    I_{MAT,i} = I_{SIG2,i} - I_{BG,i}

Composition of the Total Inclusion Signal Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The total inclusion signal intensity :math:`I_{SIG3,i}` is composed by the contributions of the background, the matrix
and the inclusion itself.

.. math::
    I_{SIG3,i} = I_{BG,i} + I_{MAT,i} + I_{INCL,i}

Mixed Signal Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The mixed signal intensity :math:`I_{MIX,i}` is composed by the contributions of the matrix and the inclusion itself.

.. math::
    I_{MIX,i} = I_{MAT,i} + I_{INCL,i}

Therefore, it can be easily calculated by reducing the total inclusion signal intensity :math:`I_{SIG3,i}` by the
background intensity.

.. math::
    I_{MIX,i} = I_{SIG3,i} - I_{BG,i}

Matrix Contribution to the Total Inclusion Signal Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The matrix contribution :math:`I_{MAT-INCL,i}` to the total inclusion signal intensity :math:`I_{SIG3,i}` is already a
little bit tricky to determine, since it requires an element which is only present in the matrix but not in the
inclusion ("matrix-only tracer"). We call this matrix-only tracer element :math:`t`.

.. math::
    I_{MAT-INCL,t} = I_{SIG3,t} - I_{BG,t} = I_{MIX,t}

Now, the calculation of this signal contribution is also possible for all other elements.

.. math::
    I_{MAT-INCL,i} = I_{MAT-INCL,t} \cdot \frac{I_{MAT,i}}{I_{MAT,t}}

Background- and Matrix-corrected Inclusion Intensity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The background- and matrix-corrected inclusion intensity :math:`I_{INCL,i}` can be calculated on at least four different
ways that are available in PySILLS.
Method 1 - (after Heinrich et al. 2003)
''''''''''''''''
.. math::
    I_{INCL,i} = I_{MIX,i} - I_{MIX,t} \cdot \frac{I_{MAT,i}}{I_{MAT,t}}
Method 2 - (after SILLS Equation Sheet)
''''''''''''''''
.. math::
    I_{INCL,i} = I_{MIX,i} - I_{MAT-INCL,i}
Method 3 - (after SILLS Equation Sheet)
''''''''''''''''
.. math::
    I_{INCL,i} = I_{MIX,i} - R \cdot I_{MAT,i}
The factor R can be calculated by the following equation.
.. math::
    R = \frac{I_{MIX,t}}{I_{MAT,t}}
Method 4 - (after the theoretical composition of the total inclusion signal intensity)
''''''''''''''''
.. math::
    I_{INCL,i} = I_{SIG3,i} - I_{BG,i} - I_{MAT-INCL,i}

Sensitivity-related parameters
--------------------------------
More blabla

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