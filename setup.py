#!/usr/bin/env python
req = ['nose','sympy','scikit-image','astropy','matplotlib','h5py',]
pipreq = ['photutils']

import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception:
    pip.main(['install'] + req)
pip.main(['install'] +pipreq)
# %%
from setuptools import setup

setup(name='starscale',
      packages=['starscale'],
      author='Michael Hirsch, Ph.D.',
      url = 'https://www.github.com/scivision/starscale',
      install_requires=req+pipreq,
	  )

