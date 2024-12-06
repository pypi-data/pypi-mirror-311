"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/stable/plugins/guides.html?#sample-data

Replace code below according to your needs.
"""

from __future__ import annotations

import numpy
from skimage import io


def make_sample_data():
    """Download a sample image"""

    scale = (1, 1000, 76.0005, 76.0005)
    units = ('pixel', 'nm', 'nm', 'nm')
    nucleiData = io.imread('https://dev.mri.cnrs.fr/attachments/download/3597/C1-240628_DAPI_MEMBRITE-546_EPHA-488_TBXT-594_OTX-647_SLOWFADE_2.tif')
    nuclei = numpy.array([numpy.array(nucleiData)])
    spotsData = io.imread('https://dev.mri.cnrs.fr/attachments/download/3595/C4-240628_DAPI_MEMBRITE-546_EPHA-488_TBXT-594_OTX-647_SLOWFADE_2.tif')
    spots = numpy.array([numpy.array(spotsData)])
    membranesData = io.imread('https://dev.mri.cnrs.fr/attachments/download/3596/C5-240628_DAPI_MEMBRITE-546_EPHA-488_TBXT-594_OTX-647_SLOWFADE_2.tif')
    membranes = numpy.array([numpy.array(membranesData)])

    return [(nuclei,
             {'scale': scale,
              'units':  units,
              'colormap': 'bop blue',
              'blending': "additive",
              'name': 'nuclei (segment-embryo example image)'}),
            (spots,
             {'scale': scale,
              'units': units,
              'colormap': 'red',
              'blending': "additive",
              'name': 'spots (segment-embryo example image)'},
             ),
            (membranes,
             {'scale': scale,
              'units': units,
              'colormap': 'bop orange',
              'blending': "additive",
              'name': 'membranes (segment-embryo example image)'},
             )
            ]
