#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='EntroPy_Toolbox',
    version='1.0.2',
    description='A Python toolbox for calculating various kinds of entropy of sequences',
    long_description='A Python toolbox for calculating various kinds of entropy of sequences',
    author='Nicolas McNair',
    author_email='nicolas.mcnair@sydney.edu.au',
    url='https://github.com/nicolasmcnair/EntroPy',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3'],
    keywords='entropy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.3',
    install_requires=['numpy','scipy']
)
