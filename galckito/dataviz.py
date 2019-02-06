'''
    Utilities with the goal of data visualization
'''


from astropy.visualization import simple_norm
from astropy.visualization.mpl_normalize import ImageNormalize

from matplotlib import pyplot as plt

from .constants import filter_dict
from .image import IllustrisCube

import numpy as np


def filter_mosaic(cube):
    '''
        Displays all the filters of the
        Illustris cube in a mosaic
    '''
    f, axs = plt.subplots(6, 6, figsize=(12, 12))

    for ax, filter in zip(axs.flat, filter_dict.keys()):
        ax.set_xticks([])
        ax.set_yticks([])
        filter_data = cube.in_Jy(cube.get_slice(filter))
        ref = cube.in_Jy(cube.get_slice('SDSS-r'))
        noise = np.sqrt(ref.sum()/10) * np.random.randn(cube.npix, cube.npix)
        gshow(filter_data+noise, ax=ax)
        per5 = np.percentile(np.linspace(0, cube.npix, 100), 8.5)
        ax.text(per5, per5, filter)
    plt.subplots_adjust(hspace=0, wspace=-0.2)


def gshow(data, ax=None, Rp=None, mode=None, title='', colorbar_label='', cmap='viridis'):
    '''
        Adaptation of pyplot.imshow with
        normalization and without ticks
    '''
    f = None
    if(ax is None):
        f, ax = plt.subplots(1, 1)
        
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    if(isinstance(data, IllustrisCube)):
        data = data.get_slice('ACS-F606', cam=14, Rp=Rp)

    if(mode == 'SB'):
        cmap = 'viridis_r'
        colorbar_label = '$mag \ / \ arcsec^2$'

    cs = ax.imshow(data, cmap=cmap, interpolation=None)

    

    if(f is not None):
        cb = f.colorbar(cs)
        cb.set_label(colorbar_label, fontsize=17)

    return ax
