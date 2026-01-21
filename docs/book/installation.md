# Installation

*PySILLS* can be installed in two supported ways:

1. via the *Python* package manager pip, or
2. by downloading the *GitHub* repository.

The installation via *pip* is the recommended and preferred method.

### Installation via pip (recommended)
The most straightforward and stable way to install *PySILLS* is using *pip*. This installs the latest released 
version together with all required dependencies.

```bash
pip install pysills
```

**Requirements:**
- *Python* ≥ 3.9
- A functional Python environment (e.g. venv, conda)

After installation, *PySILLS* can be started directly in the terminal by using the command

```bash 
pysills
```

This installation method is recommended because it: 
- is reproducible, 
- resolves dependencies automatically, 
- allows easy updates:

```bash 
pip install --upgrade pysills
```

### Installation from GitHub (alternative)
Alternatively, *PySILLS* can be installed directly from the *GitHub* repository. This approach is useful if:
- development versions need to be tested, 
- modifications to the source code are planned, 
- a released package version is not desired.

First, clone the repository or download it as a ZIP archive:

```bash
git clone https://github.com/MABeeskow/PySILLS.git
cd PySILLS
```

Then install *PySILLS* from the local source directory:

```bash
pip install .
```

#### Note ⚠️

When installing from *GitHub*, the installed code corresponds to the current state of the repository. Depending on the 
development status, stability cannot be guaranteed.

### Developer's recommendation
For regular users and productive workflows, installation via *pip* is strongly recommended. Installation from *GitHub* 
is primarily intended for developers and advanced users.