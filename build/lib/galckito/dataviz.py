from astropy.visualization import simple_norm
from astropy.visualization.mpl_normalize import ImageNormalize

from matplotlib import pyplot as plt

from .constants import filter_dict

def filter_mosaic(illustris_cube):

    f, axs = plt.subtplots(6, 6)

    for ax, filter in zip(axs.flat, filter_dict.keys()):
        filter_data = illustris_cube.get_slice(filter)
        gshow(filter_data, ax=ax)

def gshow(data, ax=None):

    if(ax==None):
        f, ax = plt.subtplos(1, 1)

    norm = simple_norm(data, 'sqrt', percent=99.9)
    cs = ax.imshow(data, norm=norm, cmap='gist_gray_r')
    
    if(ax==None):
        f.colorbar(cs)

    return ax
