from astropy.visualization import simple_norm
from astropy.visualization.mpl_normalize import ImageNormalize

from matplotlib import pyplot as plt

from .constants import filter_dict

import numpy as np

def filter_mosaic(cube):

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

def gshow(data, ax=None):

    if(ax==None):
        f, ax = plt.subplots(1, 1)
        ax.set_xticks([])
        ax.set_yticks([])

    norm = simple_norm(data, 'sqrt', percent=99.9)
    cs = ax.imshow(data, norm=norm, cmap='gist_gray_r', interpolation=None)
    
    if(ax==None):
        f.colorbar(cs)

    return ax
