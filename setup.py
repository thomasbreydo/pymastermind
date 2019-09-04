#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
   name='pymastermind',
   version='1.0',
   author='Thomas Breydo',
   author_email='tbreydo@gmail.com',
   url='https://github.com/thomasbreydo/pymastermind',
   description='A Python package for simulation of the MasterMind game.',
   long_description=long_description,
   license='MIT',
   packages=find_packages(),
   install_requires=['pandas', 'tqdm'],
   include_package_data=True,
)