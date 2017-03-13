#!/usr/bin/env python
from setuptools import setup

req = ['nose','sympy','scikit-image','astropy','matplotlib',
       'photutils']

setup(name='starscale',
      packages=['starscale'],
      author='Michael Hirsch, Ph.D.',
      url = 'https://www.github.com/scivision/starscale',
      install_requires=req,
	  )

