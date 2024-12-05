# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:27:18 2024

@author: Chunlei Liu
"""

import setuptools

with open("README.md","r",encoding="utf-8") as fh:
    long_description=fh.read()
    
setuptools.setup(
    name='Matilda',
    version='1.0',
    description='A nulti-modal single cell sequencing analysis tool',
    author='Chunlei Liu',
    author_email='',
    packages=setuptools.find_packages(),
   )