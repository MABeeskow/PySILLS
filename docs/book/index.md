# PySILLS

*PySILLS* is a new, *Python*-based open source tool for a modern data reduction of LA-ICP-MS experiments. It
is focused on the compositional analysis of major, minor, and trace elements of minerals (and glasses) as well as of 
fluid and melt inclusions. *PySILLS*, started as a M.Sc. thesis project, is developed by Maximilian Alexander Beeskow, 
who is part of the work group of Prof. Dr. Thomas Wagner and Dr. Tobias Fusswinkel at RWTH Aachen University. *PySILLS* 
was conceptionally inspired by the widely-used data reduction tool *SILLS*, developed and maintained by Prof. Dr. 
Christoph A. Heinrich and Dr. Marcel Guillong at ETH Zürich.

### Top features
The following list shows some of the main features that differentiate *PySILLS* from alternative data reduction tools:

- works on all common computer systems that can run *Python* code,
- use of multiple standard reference materials in one project file,
- use of multiple internal standards in one project file,
- consideration of isotope-specific standard reference materials,
- assemblage definition,
- file-specific quick analysis,
- intuitive, fast and flexible workflow,
- use of *PyPitzer*, which enables thermodynamic modeling of fluid inclusion systems based on the Pitzer model,
- multiple check-up possibilities,
- export of processed LA-ICP-MS data (e.g., signal intensity ratios, analytical sensitivities, etc.) for external 
calculations,
- many quality-of-life features that support and accelerate a fast and reliable workflow.

### Planned features
The following list shows some ideas, that we have in mind, for the future development of *PySILLS*.

- replacement of scattered signal intensity values by regression curves,
- *Jupyter notebooks* for a browser-based data reduction of LA-ICP-MS experiments,
- production of a *YouTube* video course.

### Disclaimer
Although PySILLS has been tested extensively and many issues encountered during development have been resolved, 
undiscovered bugs may still exist.
Please report any suspected bugs using a structured and detailed bug report, including clear instructions on how the 
issue can be reproduced.

Based on our experience, a considerable number of reported issues were not caused by software errors but by workflows 
that deviated from the documented tutorials. PySILLS is a powerful but complex data reduction tool, and careful 
adherence to the provided tutorials is essential for correct usage.
An intuitive workflow does not imply the absence of methodological constraints. Users are therefore strongly encouraged 
to read and follow the tutorials thoroughly before reporting potential issues.