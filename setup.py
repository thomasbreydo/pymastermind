#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

with open(os.path.join('docs', 'README.md')) as f:
    long_description = f.read()

setup(
   name='pymastermind',
   version='1.2',
   author='Thomas Breydo',
   author_email='tbreydo@gmail.com',
   url='https://github.com/thomasbreydo/pymastermind',
   download_url='https://github.com/thomasbreydo/pymastermind/archive/' \
                'v1.2.tar.gz',
   description='A Python package designed to play, develop strategies/' \
               'algorithms, and implement the classic MasterMind board game.',
   long_description=long_description,
   long_description_content_type='text/markdown',
   keywords=['GAME', 'MASTER', 'MIND', 'STRATEGY', 'BOARD', 'CODE'],
   classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3.7',
      'Topic :: Games/Entertainment :: Board Games',
      'Topic :: Games/Entertainment :: Turn Based Strategy',
   ],
   license='MIT',
   packages=find_packages(),
   install_requires=['pandas', 'tqdm'],
   include_package_data=True,
)