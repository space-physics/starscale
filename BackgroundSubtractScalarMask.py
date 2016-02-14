#!/usr/bin/env python3
"""
Astronomical Image Scalar Background Subtraction with Source Masking
- Estimates background noise level as a scalar, after masking out stars
Michael Hirsch

https://photutils.readthedocs.org/en/latest/photutils/background.html
"""
from numpy import ones,iinfo
from numpy.ma import masked_where
from sympy.ntheory import factorint
from astropy.stats import sigma_clipped_stats
#from astropy.convolution import Gaussian2DKernel
from photutils.detection import detect_sources
from photutils.background import Background
from skimage.morphology import binary_dilation
from matplotlib.pyplot import figure,subplots,show
import seaborn as sns
sns.set_context('talk')
#
from astrometry_azel.imgAvgStack import meanstack #reads the typical formats our group stores images in
#
infn = '../astrometry_azel/test/apod4.fits'

data = meanstack(infn,1)[0]


#%% now photutils way
#rfact = max(list(factorint(data.shape[0]).keys()))
#cfact = max(list(factorint(data.shape[1]).keys()))
rfact=data.shape[0]//10
cfact=data.shape[1]//10
bg = Background(data,(rfact,cfact))
dataphot = data - bg.background
#%%

fg,axs = subplots(1,2)

ax = axs[0]
hi=ax.imshow(dataphot,interpolation='none',cmap='gray')
ax.grid(False)
ax.set_title('background subtracted image')

ax = axs[1]
hi = ax.imshow(bg.background,interpolation='none',cmap='jet')
fg.colorbar(hi,ax=ax)
ax.grid(False)

show()

def manual_bg(data):
    #directly from photutils example
    mean, median, std = sigma_clipped_stats(data, sigma=3.0, iters=5)
    threshold = median + (std * 2.)
    segm_img = detect_sources(data, threshold, npixels=5)
    #%% morphological
    mask = segm_img.data.astype(bool)
    strel = ones((3,3))
    dilated = binary_dilation(mask,strel)
    mean, median, std = sigma_clipped_stats(data, sigma=3.0, mask=dilated)
    #%% use mean or median for background? Let's do what sextractor does
    if (mean - median) / std > 0.3:
        bgval = median
    else:
        bgval = mean
    #%% background subtract
    dinf = iinfo(data.dtype)

    imgmask = masked_where(~dilated,100+data).clip(0,dinf.max).astype(data.dtype)
    datashift=(data-bgval).clip(0,dinf.max).astype(data.dtype)
#%%
    fg,axs = subplots(2,2)
    ax = axs[0,0]
    hi=ax.imshow(data,interpolation='none',cmap='gray')
    ax.imshow(imgmask,interpolation='none',cmap='gray')
    ax.set_title('original image with stars highlighted')
    fg.colorbar(hi,ax=ax)
    ax.grid(False)

    ax=axs[0,1]
    ax.imshow(dilated,interpolation='none')
    ax.set_title('dilated')
    ax.grid(False)

    ax = axs[1,0]
    hi=ax.imshow(datashift,interpolation='none',cmap='gray')
    ax.set_title('background subtracted image {:.3f}'.format(bgval))
    fg.colorbar(hi,ax=ax)
    ax.grid(False)

    fg.tight_layout()

    return datashift