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
from photutils import daofind
from astropy.stats import sigma_clipped_stats
from photutils.background import Background
from photutils import CircularAperture
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from matplotlib.pyplot import figure,show
#
from astrometry_azel.imgAvgStack import meanstack #reads the typical formats our group stores images in
#
#infn = '../astrometry_azel/test/apod4.fits'
infn = '~/Dropbox/aurora_data/StudyEvents/2013-04-14/HST/hst0star.h5'
#%% load data
data = meanstack(infn,100)[0]
#%% flat field

#%% background
mean, median, std = sigma_clipped_stats(data, sigma=3.0, iters=5)

rfact=data.shape[0]//10
cfact=data.shape[1]//10
bg = Background(data,(rfact,cfact))

dataphot = data - bg.background
#%% source extraction
sources = daofind(data - median, fwhm=3.0, threshold=5.*std)
#%% plots
positions = (sources['xcentroid'], sources['ycentroid'])
apertures = CircularAperture(positions, r=4.)
norm = ImageNormalize(stretch=SqrtStretch())

ax = figure().gca()
ax.imshow(data, cmap='Greys', origin='lower', norm=norm)
apertures.plot(color='blue', lw=1.5, alpha=0.5)
show()