#!/usr/bin/env python

from __future__ import unicode_literals
from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))
README = io.open(os.path.join(here, 'README.rst'), encoding="utf8").read()

version = '0.0.1'
author = 'Ratson'
description = "Dj-environ allows you to utilize 12factor inspired environment " \
              "variables to configure your Django application."
install_requires = ['django', 'six']

setup(name='dj-environ',
      version=version,
      description=description,
      long_description=README,
      classifiers=[
          # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Information Technology',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
          'License :: OSI Approved :: MIT License',
          'Framework :: Django'
      ],
      keywords='django environment variables 12factor',
      author=author,
      author_email='contact@ratson.name',
      url='https://github.com/ratson/dj-environ',
      license='MIT License',
      packages=find_packages(),
      platforms=["any"],
      include_package_data=True,
      test_suite='environ.test.load_suite',
      zip_safe=False,
      install_requires=install_requires,
      )
