#!/usr/bin/env python3

from setuptools import setup

with open('README.md') as f:
    description = f.read()

setup(
   name='mastermind',
   version='1.0',
   description=description,
   url='https://github.com/thomasbreydo/mastermind',
   author='Thomas Breydo',
   author_email='tbreydo@gmail.com',
   packages=['mastermind'],
   install_requires=['pandas', 'tqdm.auto'],
   include_package_data=True,
)