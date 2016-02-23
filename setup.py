#!/usr/bin/env python3

from setuptools import setup
import subprocess

with open('README.rst','r') as f:
	long_description = f.read()

setup(name='starscale',
      version='0.1',
	description='Examples of source extraction and photometry with AstroPy',
	long_description=long_description,
	author='Michael Hirsch',
	url='https://github.com/scienceopen/starscale',
	install_requires=['photutils'],
   	dependency_links = [''],
      packages=['starscale'],
	  )

#%%
try:
    subprocess.run(['conda','install','--yes','--quiet','--file','requirements.txt'])
except Exception as e:
    print('you will need to install packages in requirements.txt  {}'.format(e))
    with open('requirements.txt','r') as f:
        print(f.read())
