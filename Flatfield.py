#!/usr/bin/env python
"""
Takes FITS image stack of a uniformly illuminated field (e.g. tungsten light box)
and discards the first "bad" image in the stack, then takes the mean of the other images
and saves the result to an HDF5 file.

To do tomographic analysis, you must take into account the vignetting of the optical
system via flat-fielding, plus the background subtraction
"""
from pathlib import Path
from matplotlib.pyplot import show
#
from astrometry_azel.io import meanstack
from starscale.flatfield import writeflatfield,plotflatfield

# these files in Dropbox as hst0flat.h5, hst1flat.h5
#fn = '~/HST/calibration/flatfield/hist0/TungstenUltra53HzG2EM20_A.fits'
#fn = '~/HST/calibration/flatfield/hist1/tungstenExternal30fps_preamp1EM200.fits'
method='median'

if __name__ == "__main__":
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn')
    p = p.parse_args()

    mimg = meanstack(p.fn,slice(1,None),method=method)[0]

    ofn = Path(p.fn).expanduser().with_suffix('.h5')
    writeflatfield(ofn,mimg)

    plotflatfield(mimg)

    show()
