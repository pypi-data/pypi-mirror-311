"""
File: setup.py
Creation Date: 2024-11-25
Last Update: 2024-11-25
Creator: eis-x
Github: https://github.com/eis-x/pytreebuilder
"""

from setuptools import setup, find_packages
#name = "pytreebuilder"
#version = "1.0"
from pytreebuilder.utils import name, version
setup(
    name=name,
    version=version,
    packages=find_packages(),
    install_requires=[
        # Liste des dépendances
    ],
    author='eis-x',
    author_email='eis-x@hotmail.com',
    description='A module to create project structures from a tree description text file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eis-x/pytreebuilder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)