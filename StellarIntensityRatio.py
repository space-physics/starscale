#!/usr/bin/env python3
"""
Compute Intensity Ratio between cameras.
This is useful as cameras with the same optics and after de-vignetting will
have distinct optical gain.
One has to back out atmospheric attenuation for higher fidelity with known stellar spectra,
but if you have cameras closely spaced (few km standoff), with same optics and filters,
looking in the same direction,
as a first pass one may just identify stars and take their intensity ratios.
"""
