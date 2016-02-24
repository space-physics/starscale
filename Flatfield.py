#!/usr/bin/env python3
"""
Takes FITS image stack of a uniformly illuminated field (e.g. tungsten light box)
and discards the first "bad" image in the stack, then takes the mean of the other images
and saves the result to an HDF5 file.

To do tomographic analysis, you must take into account the vignetting of the optical
system via flat-fielding, plus the background subtraction
"""
from pathlib import Path
from numpy import float32,uint8,string_
import h5py
from matplotlib.pyplot import figure,show
#
from astrometry_azel.imgAvgStack import meanstack

#fn = '~/HST/calibration/flatfield/hist0/TungstenUltra53HzG2EM20_A.fits'
fn = '~/HST/calibration/flatfield/hist1/tungstenExternal30fps_preamp1EM200.fits'
method='median'

def writeh5img(h,dat,path):
    fimg = h.create_dataset(path,data=dat,
                            compression='gzip', compression_opts=5,
                            fletcher32=True,shuffle=True,track_times=True)

    fimg.attrs["CLASS"] = string_("IMAGE")
    fimg.attrs["IMAGE_VERSION"] = string_("1.2")
    fimg.attrs["IMAGE_SUBCLASS"] = string_("IMAGE_GRAYSCALE")
    fimg.attrs["DISPLAY_ORIGIN"] = string_("LL")
    fimg.attrs['IMAGE_WHITE_IS_ZERO'] = uint8(0)

def writeflatfield(fn,img):
    assert fn.suffix=='.h5'
    maximg = img.max()
    flatnorm = (img/maximg).astype(float32)


    print('writing {}'.format(fn))
    with h5py.File(str(fn),'w',libver='latest') as h:
        writeh5img(h,img,     '/flatimg')
        writeh5img(h,flatnorm,'/flatnorm')


def plotflatfield(img):
    fg=figure()
    ax = fg.gca()
    hi=ax.imshow(mimg,interpolation='none',origin='bottom',cmap='gray')
    fg.colorbar(hi)
    ax.set_title('{} {}'.format(fn,method))

    ax = figure().gca()
    ax.hist(img.ravel(),bins=100)
    ax.set_yscale('log')
    ax.set_title('{} {}'.format(fn,method))

if __name__ == "__main__":
    mimg = meanstack(fn,slice(1,None),method=method)[0]

    ofn = Path(fn).expanduser().with_suffix('.h5')
    writeflatfield(ofn,mimg)

    plotflatfield(mimg)

    show()