#!/usr/bin/env python
"""Setup script for building nret's python bindings"""
import os
import codecs
import re
from os import path
from setuptools import setup, find_packages

# Global variables for this extension:
name = "nret"  # name of the generated python extension (.so)
description = "A Python module that contains all the tools neeeded for retrieving N concentration from satellite bands"
long_description = "Conaining tools to generate biophisical & biochemical input oints and link its distribution to LAI, then run the points through the PROSAIL-PRO radiative transfer model and set every thing for Gaussian Process model training."
author = "Mahmoud H. Ahmed  @ IHE Delft, The Netherlands"
author_email = "mahmoudhatim55@gmail.com"
url = "https://github.com/Mahmoud-H97/NRET"

setup(
    name=name,
    version= 0.9,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=author,
    url=url,
    author_email=author_email,
    include_package_data=True,
    install_requires=[
        "numpy",
        "numba",
        "scipy",
        "pytest",
        "pandas",
    ],
    packages=find_packages(),
    zip_safe=False 
)