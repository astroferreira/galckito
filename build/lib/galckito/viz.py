from astropy.visualization import simple_norm
from astropy.visualization.mpl_normalize import ImageNormalize

from matplotlib import pyplot as plt

def gshow(data, ax=None):

    if(ax==None):
        f, ax = plt.subtplos(1, 1)

    norm = simple_norm(data, 'sqrt', percent=99.9)
    cs = ax.imshow(data, norm=norm, cmap='gist_gray_r')
    
    if(ax==None):
        f.colorbar(cs)

    return ax
