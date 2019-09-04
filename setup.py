#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
   name='mastermind',
   version='1',
   author='Thomas Breydo',
   author_email='tbreydo@gmail.com',
   url='https://github.com/thomasbreydo/mastermind',
   description='A Python package for simulation of the MasterMind game.',
   long_description=long_description,
   license='MIT',
   packages=find_packages(),
   install_requires=['pandas', 'tqdm'],
   include_package_data=True,
)