from pathlib import Path

import numpy as np
import h5py
from matplotlib.pyplot import figure


def writeh5img(h, dat, path):
    fimg = h.create_dataset(
        path,
        data=dat,
        compression="gzip",
        compression_opts=5,
        fletcher32=True,
        shuffle=True,
        track_times=True,
    )

    fimg.attrs["CLASS"] = np.string_("IMAGE")
    fimg.attrs["IMAGE_VERSION"] = np.string_("1.2")
    fimg.attrs["IMAGE_SUBCLASS"] = np.string_("IMAGE_GRAYSCALE")
    fimg.attrs["DISPLAY_ORIGIN"] = np.string_("LL")
    fimg.attrs["IMAGE_WHITE_IS_ZERO"] = np.uint8(0)


def writeflatfield(fn, img):
    assert fn.suffix == ".h5"
    maximg = img.max()
    flatnorm = (img / maximg).astype(np.float32)

    print("writing {}".format(fn))
    with h5py.File(str(fn), "w", libver="latest") as h:
        writeh5img(h, img, "/flatimg")
        writeh5img(h, flatnorm, "/flatnorm")


def plotflatfield(img: np.ndarray, fn: Path, method: str):
    fg = figure()
    ax = fg.gca()
    hi = ax.imshow(img, interpolation="none", origin="bottom", cmap="gray")
    fg.colorbar(hi)
    ax.set_title(f"{fn} {method}")

    ax = figure().gca()
    ax.hist(img.ravel(), bins=100)
    ax.set_yscale("log")
    ax.set_title(f"{fn} {method}")
