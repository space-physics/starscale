#!/usr/bin/env python

from setuptools import setup
import subprocess

try:
    subprocess.call(['conda','install','--quiet','--file','requirements.txt'])
except Exception as e:
    pass

setup(name='starscale',
	description='Examples of source extraction and photometry with AstroPy',
	author='Michael Hirsch',
	url='https://github.com/scienceopen/starscale',
	install_requires=['photutils','pathlib2'],
   	dependency_links = [],
      packages=['starscale'],
	  )

