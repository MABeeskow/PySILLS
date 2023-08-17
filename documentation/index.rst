.. pysills documentation master file.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation of PySILLS |version|!
===========================================================

PySILLS is a newly developed Python-based, open source tool for a modern data reduction of LA-ICP-MS experiments. It is
focused on the major, minor and trace element analysis of mineral compositions as well as of fluid and melt inclusion
compositions. PySILLS, which was initially part of a M.Sc. thesis project, is developed by Maximilian Alexander Beeskow
in the work group of Prof. Dr. Thomas Wagner and Dr. Tobias Fusswinkel at RWTH Aachen University. PySILLS was inspired
conceptionally by the widely-used data reduction tool SILLS.

Top Features
~~~~~~~~~~~~~~~
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

Planned Features
~~~~~~~~~~~~~~~~~~
* more outlier detection algorithms
* replacement of scattered intensity values by regression curves
* extended language support
* in-built geothermometry analysis
* Jupyter notebooks for a browser-based data reduction of LA-ICP-MS experiments
* production of a video course on YouTube

.. container:: button

   :doc:`About PySILLS <getting_started/about>` | :doc:`Authors <getting_started/authors>` |
   :doc:`Installation <getting_started/installation>` | :doc:`Contributing <getting_started/contributing>` |
   :doc:`What is what <getting_started/whatiswhat>` | :doc:`Tutorials <getting_started/tutorial/index>` |
   :doc:`Examples <getting_started/example/index>`

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Getting Started
   :glob:

   getting_started/about
   getting_started/authors
   getting_started/installation
   getting_started/contributing


   getting_started/whatiswhat/index
   getting_started/tutorial/index
   getting_started/example/index

   :caption: API Reference
   :glob:

   api_reference/vector

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`