#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from setuptools import setup, find_packages
import sys, os

requires = [
    'ConfigParser',
    'requests',
    'cassandra-driver',
    'elasticsearch',
    'blist'
]

version = '0.1'

setup(name='csindex',
      version=version,
      description="Cassandra Index on Elastic Search",
      long_description="""\
Keep Elastic Search document index in sync with Cassandra database""",
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Environment :: Console",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
      ],
      keywords='',
      author='Eduardo F. Santos',
      author_email='eduardo@eduardosan.com',
      url='http://www.eduardosan.com',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
