
from .cosmocalc import cosmology

from astropy.io import fits

import numpy as np

filter_dict = {'GALAX FUV': 0, 'GALAX NUV':1, 'SDDS-u':2, 'SDDS-g':3, 'SDDS-r':4, 'SDDS-i':5, 'SDDS-z':6, 'IRAC1':7, 'IRAC2':8, 'IRAC3':9, 'IRAC4':10, 'Johnson-U':11, 'Johnson-B':12,'Cousins-R':13, 'Cousins-I':14, 'Johnson-V':15, 'Johnson-J':16, 'Johnson-H':17, 'Johnson-K':18, '2MASS-H':19, '2MASS-Ks':20, 'ACS-F435':21, 'ACS-F606':22, 'ACS-F775':23, 'ACS-F850':24, 'f105w':25, 'f125w':26, 'f160w':27, 'NIRCAM-F070W': 28, 'NIRCAM-F090W':29, 'NIRCAM-F115W':30, 'NIRCAM-F150W':31, 'NIRCAM-F200W': 32, 'NIRCAM-F277W': 33, 'NIRCAM-F356W':34, 'NIRCAM-F444W':35}

class IllustrisCube(object):

    def __init__(self, path):

        if(path is not None):
            try:
                self.fits = fits.open(path)
                self.npix = self.fits[14].data[0].shape[0]
                self.fov = self.fits[2].header['linear_fov']
                self.px_in_kpc = self.fov / self.npix
                self.z = 0.05
                self.cosmology = cosmology(self.z)
                self.cam_px_in_arcsec = (self.px_in_kpc / self.fits[2].header['cameradist'] * 2.06e5)
                self.px_in_sr = (1e3 * self.px_in_kpc / 10.0)**2
            except (Exception, TypeError):
                print('Error opening FITS')

    def in_Jy(self, data):
        return data * self.px_in_sr / 1e6

    def abmag(self, data):
        return - 2.5 * np.log10(np.sum(self.in_Jy(data)) / 3631)

    def color_color(self, filter1, filter2, filter3, filter4, cam=14):
        '''
            Return the color color value as
            (filter1-filter2, filter3, filter4)
        '''
        f_mag = self.abmag(self.get_slice(filter1, cam=cam))
        s_mag = self.abmag(self.get_slice(filter2, cam=cam))
        t_mag = self.abmag(self.get_slice(filter3, cam=cam))
        th_mag = self.abmag(self.get_slice(filter4, cam=cam))

        return (f_mag - s_mag, t_mag - th_mag)

    def UVJ(self, cam=14):
        umag = self.abmag(self.get_slice('ACS-F435', cam=cam))
        vmag = self.abmag(self.get_slice('ACS-F606', cam=cam))
        jmag = self.abmag(self.get_slice('f125w', cam=cam))

        return (umag-vmag, vmag-jmag)

    def get_slice(self, filter_name, cam=14):
        filter = filter_dict[filter_name]
        return self.fits[cam].data[filter]

    def get_filter(self, filter_name):
        if(filter_name in filter_dict.keys()):
            filter = filter_dict[filter_name]
            slice = [self.fits[cam].data[filter] for cam in range(14, 18)]
            return slice
        else:
            raise NotImplementedError