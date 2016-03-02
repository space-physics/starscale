#!/usr/bin/env python3
"""
Compute Intensity Ratio between cameras.
This is useful as cameras with the same optics and after de-vignetting will
have distinct optical gain.
One has to back out atmospheric attenuation for higher fidelity with known stellar spectra,
but if you have cameras closely spaced (few km standoff), with same optics and filters,
looking in the same direction,
as a first pass one may just identify stars and take their intensity ratios.

First you need some video without any aurora or clouds at all, not even faint wisps.

BE SURE there isn't even faint aurora in your videos for this cross-calibration with stars!

We chose to use data from 2013-04-14T11:30 UT, as by the DMSP keogram, this was a time of minimal auroral activity
We extract about 100 frames of data to HDF5 from this time by:

cd histutils
./ConvertDMC2h5.py ~/U/irs_archive3/HSTdata/2013-04-14-HST0/2013-04-14T07-00-CamSer7196.DMCdata \
  -s 2013-04-14T06:59:55Z -k 0.018867924528301886 -t 2013-04-14T11:30:00Z 2013-04-14T11:30:02Z -l 65.1186367 -147.432975 500 \
  --rotccw -1 -o ~/Dropbox/aurora_data/StudyEvents/2013-04-14/HST/hst0star.h5

./ConvertDMC2h5.py ~/U/irs_archive4/HSTdata/2013-04-14/2013-04-14T07-00-CamSer1387.DMCdata \
  -s 2013-04-14T07:00:07Z -k 0.03333333333333333 -t 2013-04-14T11:30:00Z 2013-04-14T11:30:03Z -l 65.12657 -147.496908333 210 \
  --rotccw 2 -o ~/Dropbox/aurora_data/StudyEvents/2013-04-14/HST/hst1star.h5

based on http://photutils.readthedocs.org/en/latest/photutils/detection.html
"""
from pathlib import Path
import h5py
from numpy import column_stack,empty,rot90
from photutils import daofind
from astropy.stats import sigma_clipped_stats
from photutils.background import Background
from photutils import CircularAperture
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from matplotlib.pyplot import subplots,show
#
from astrometry_azel.imgAvgStack import meanstack #reads the typical formats our group stores images in
#
def starbright(fnstar,fnflat,istar,axs,fg):
    #%% load data
    data = meanstack(fnstar,100)[0]
    #%% flat field
    flatnorm = readflat(fnflat,fnstar)
    data = (data/flatnorm).round().astype(data.dtype)
    #%% background
    mean, median, std = sigma_clipped_stats(data, sigma=3.0)

    rfact=data.shape[0]//32
    cfact=data.shape[1]//32
    bg = Background(data,(rfact,cfact),interp_order=5)

    dataphot = data - bg.background
    #%% source extraction
    sources = daofind(data - median, fwhm=3.0, threshold=5*std)
    #%% star identification and quantification
    XY = column_stack((sources['xcentroid'], sources['ycentroid']))
    apertures = CircularAperture(XY, r=4.)
    norm = ImageNormalize(stretch=SqrtStretch())
#%% plots
    fg.suptitle('{}'.format(fnflat.parent),fontsize='x-large')

    hi = axs[-3].imshow(flatnorm,interpolation='none',origin='lower')
    fg.colorbar(hi,ax=axs[-3])
    axs[-3].set_title('flatfield {}'.format(fnflat.name))

    hi = axs[-2].imshow(bg.background,interpolation='none',origin='lower')
    fg.colorbar(hi,ax=axs[-2])
    axs[-2].set_title('background {}'.format(fnstar.name))

    hi = axs[-1].imshow(data, cmap='Greys', origin='lower', norm=norm,interpolation='none')
    fg.colorbar(hi,ax=axs[-1])
    for i,xy in enumerate(XY):
        axs[-1].text(xy[0],xy[1], str(i),ha='center',va='center',fontsize=16,color='w')
    apertures.plot(ax=axs[-1], color='blue', lw=1.5, alpha=0.5)
    axs[-1].set_title('star {}'.format(fnstar.name))

    return dataphot[XY[istar,1].round().astype(int),
                    XY[istar,0].round().astype(int)]

def readflat(fnflat,fnstar):
    """
    star is used to get orientation info, the flat field has to be rotated to match
    the star field.
    """
    with h5py.File(str(fnflat),'r',libver='latest') as f, h5py.File(str(fnstar),'r',libver='latest') as g:
        return rot90(f['flatnorm'], g['params']['rotccw'])


if __name__ == '__main__':
    #fn = '../astrometry_azel/test/apod4.fits'
    path = '~/Dropbox/aurora_data/StudyEvents/2013-04-14/HST/'
    fstar = ('hst0star.h5', 'hst1star.h5')
    fflat = ('hst0flat.h5', 'hst1flat.h5')
    # a manually identified pairing of stars (could be automatic but this is a one-off)
    slist = column_stack((range(1,8), range(1,8)))
#%%
    path = Path(path).expanduser()
    bstar = empty(slist.shape)

    fg,axs= subplots(2,3)
    for i,(fs,ff,ax) in enumerate(zip(fstar,fflat,axs)):
        bstar[:,i] = starbright(path/fs, path/ff, slist[:,i], ax, fg)

    show()