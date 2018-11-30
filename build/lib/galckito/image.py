
from .cosmocalc import cosmology
from .constants import *

from astropy.io import fits
from scipy.ndimage import zoom


import numpy as np
import pandas as pd


class IllustrisCube(object):

    def __init__(self, path, mfmtk_path=None):

        self.path = path
        self.mfmtk_path = mfmtk_path

        self.parse_path()

        if(self.mfmtk_path is not None):
            self.load_mfmtk()

        if(path is not None):
            try:
                self.fits = fits.open(path)                
                self.npix = self.fits[14].data[0].shape[0]
                self.fov = self.fits[2].header['linear_fov']
                self.px_in_kpc = self.fov / self.npix
                self.z = 0.05
                self.cosmology = cosmology(self.z)
                self.cosmologyf = cosmology(self.zf)
                
                self.cam_px_in_arcsec = (self.px_in_kpc /
                                         self.fits[2].header['cameradist'] *
                                         2.06e5)

                self.px_in_sr = (1e3 * self.px_in_kpc / 10.0)**2
                
                self.px_in_arcsec = (self.px_in_kpc / 
                                     self.cosmology.kpc_per_arcsec)

            except (Exception, TypeError):
                print('Error opening FITS')

    def redshiftted(self, filter, target_pixelscale, cam):
        return artificial_redshift(self.get_slice(filter, cam=cam), self.cosmology.redshift, self.cosmologyf.redshift, self.cosmology.lum_dist, self.cosmologyf.lum_dist, self.px_in_arcsec, target_pixelscale)

    def load_mfmtk(self):
        data = np.loadtxt(self.mfmtk_path,
                          delimiter=',',
                          usecols=range(0, 56),
                          dtype=str)

        self.mfmtk = pd.DataFrame(data, columns=mfmtk_columns)

        self.mfmtk = self.mfmtk.apply(pd.to_numeric, errors='ignore')

    def color_mock(self, filter_list):

        if(len(filter_list) > 3):
            filter_list = filter_list[0:3]

        R = self.get_slice(filter_list[0])
        R = (R-R.min())/(R.max() - R.min()) * 255
        G = self.get_slice(filter_list[1])
        G = (G-G.min())/(G.max() - G.min()) * 255
        B = self.get_slice(filter_list[2])
        B = (B-B.min())/(B.max() - B.min()) * 255

        return np.dstack((R, G, B))

    def parse_path(self):
        split_path = self.path.split('/')
        
        self.filename = split_path[-1]
        self.snapshot = split_path[-1].split('_')[0]
        self.zf = zs_dict[self.snapshot]
        self.subfind = split_path[-1].split('_')[0].split('.fits')

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
        return color_color('ACS-F435', 'ACS_F606', 'ACS_F606', 'f125w')

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


def artificial_redshift(data, z1, z2, d1, d2, ps1, ps2):
    scale_factor = (d1 * (1+z2) * ps1) / (d2 * (1+z1) * ps2)
    return zoom(data, scale_factor)

