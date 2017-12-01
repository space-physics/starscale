#!/usr/bin/env python
install_requires = ['sympy','scikit-image','astropy','matplotlib','h5py',
        'photutils']
tests_require=['nose','coveralls']
from setuptools import setup

setup(name='starscale',
      packages=['starscale'],
      author='Michael Hirsch, Ph.D.',
      url = 'https://www.github.com/scivision/starscale',
      install_requires=install_requires,
      python_requires='>=3.5',
      extras_require={'tests':tests_require},
      tests_require=tests_require,
	  )

