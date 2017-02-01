#!/usr/bin/env python
"""
Example of the Contrast Stretch options in AstroPy, that you might find handy
in cytometry or other non-astronomical pursuits as well.
"""
from pathlib import Path
from astropy.io import fits
import astropy.visualization as vis
from astropy.visualization.mpl_normalize import ImageNormalize
from matplotlib.pyplot import subplots,show
from matplotlib.colors import LogNorm


def plotcontrast(img):
    """
    http://docs.astropy.org/en/stable/visualization/index.html
    """
    vistypes = (None,
                LogNorm(),
                vis.AsinhStretch(),
                vis.ContrastBiasStretch(1,0.5),
                vis.HistEqStretch(img),
                vis.LinearStretch(),
                vis.LogStretch(),
                vis.PowerDistStretch(a=10.),
                vis.PowerStretch(a=10.),
                vis.SinhStretch(),
                vis.SqrtStretch(),
                vis.SquaredStretch())

    fg,ax = subplots(4,3,figsize=(10,10))
    ax = ax.ravel()

    for i,v in enumerate(vistypes):
        #a = figure().gca()
        a = ax[i]
        if v and not isinstance(v,LogNorm):
            norm = ImageNormalize(stretch=v)
            a.set_title(str(v.__class__).split('.')[-1].split("'")[0])
        else:
            norm = v
            a.set_title(str(v).split('.')[-1].split(" ")[0])

        a.imshow(img,origin='lower',cmap='gray',norm=norm)
        a.axis('off')

    fg.suptitle('Matplotlib/AstroPy normalizations')
    #fg.tight_layout()

def getimage(fn):
    fn = Path(fn).expanduser()
    with fits.open(str(fn),mode='readonly') as h:
        return h[0].data

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn')
    p = p.parse_args()

    img = getimage(p.fn)
    plotcontrast(img)

    show()
