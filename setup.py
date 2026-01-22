from setuptools import setup, find_packages

with open("README.md", "r", encoding="latin-1") as f:
    description = f.read()

setup(
    name="pysills",
    version="1.0.93",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    url="https://github.com/MABeeskow/PySILLS",
    license="LGPL-3.0",
    author="Maximilian Alexander Beeskow",
    author_email="pysills.analysis@gmail.com",
    description="PySILLS is a Python-based, open source data reduction tool for the major, minor and trace element "
                "analysis of minerals as well as of fluid and melt inclusions.",
    keywords=["LA-ICP-MS", "data reduction", "minerals", "fluid inclusions", "melt inclusions", "sills", "pysills",
              "chemical composition", "compositional analysis", "major elements", "minor elements", "trace elements"],
    install_requires=["numpy", "scipy", "pandas", "matplotlib", "sympy"],
    entry_points={"console_scripts": ["pysills = pysills.pysills_app:pysills"]},
    include_package_data=True,
    package_data={"": ["lib/srm/*.csv", "lib/icpms/*.csv", "lib/translations/*.csv", "lib/translations/*.txt",
                       "lib/demo_files/*.csv", "lib/images/*.png", "lib/images/*.ico"]},
    long_description=description,
    long_description_content_type="text/markdown",
)