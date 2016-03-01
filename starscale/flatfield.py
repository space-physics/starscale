from numpy import float32,uint8,string_
import h5py
from matplotlib.pyplot import figure

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
