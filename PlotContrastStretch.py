#!/usr/bin/env python3
"""
Example of the Contrast Stretch options in AstroPy, that you might find handy
in cytometry or other non-astronomical pursuits as well.
"""
from astropy.io import fits
import astropy.visualization as vis
from astropy.visualization.mpl_normalize import ImageNormalize
from matplotlib.pyplot import figure,draw,pause,show
from matplotlib.colors import LogNorm

fn = 'test/hst0cal.fits'

def plotcontrast(img):
    """
    refer to http://astrofrog-debug.readthedocs.org/en/latest/visualization/
    for parameters
    """
    vistypes = (vis.AsinhStretch(),
                #vis.ContrastBiasStretch(),
                vis.LinearStretch(),
                vis.LogStretch(),
                vis.PowerDistStretch(),
                #vis.PowerStretch(),
                vis.SinhStretch(),
                vis.SqrtStretch(),
                vis.SquaredStretch())

    for v in vistypes:
        norm = ImageNormalize(stretch=v)
        ax = figure().gca()
        ax.imshow(img,origin='lower',cmap='gray',norm=norm)
        ax.set_title(str(v.__class__))
        draw(); pause(0.001) #let's throw an error now if there's a problem


    ax = figure().gca()
    ax.imshow(img,origin='lower',cmap='gray',norm=LogNorm())
    ax.set_title('matplotlib LogNorm()')

def getimage(fn):
    with fits.open(str(fn),mode='readonly') as h:
        return h[0].data

if __name__ == '__main__':
    img = getimage(fn)
    plotcontrast(img)

    show()