
from .cosmocalc import cosmology
from .realism import z_rescale
from .constants import *
from .utils import get

from astropy.io import fits
from astropy import units as u

from scipy.ndimage import zoom

import numpy as np
import pandas as pd
import json


class IllustrisCube(object):
    '''
        
        Class to handle an Illustris Cube. This parses
        the fits described in 10.1093/mnras/stu2592 and
        adds several utilities functions

    '''

    def __init__(self, path, mfmtk_path=None):

        self.path = path
        self.mfmtk_path = mfmtk_path

        self.parse_path()

        self.url = SUBHALO_URL.format(self.snapshot, self.subfind)

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
        '''
            
            Return redshiftted version of given slice with
            {target_pixelscale}. Target redshift is calculated
            with the snapshot number.

            This fucntion does not apply k-corrections
            and bandpass shifts.
            
            Only for resolution, depth and S/N purposes.
            For a more detailed approach use FERENGI instead http://www.mpia.de/FERENGI/

        '''
        return z_rescale(self.get_slice(filter, cam=cam),
                         self.cosmology.redshift,
                         self.cosmologyf.redshift,
                         self.cosmology.lum_dist,
                         self.cosmologyf.lum_dist,
                         self.px_in_arcsec, target_pixelscale)

    def load_mfmtk(self):
        '''
            Load Morfometryka output with structural measurements
        '''
        data = np.loadtxt(self.mfmtk_path,
                          delimiter=',',
                          usecols=range(0, 56),
                          dtype=str)

        self.mfmtk = pd.DataFrame(data, columns=mfmtk_columns)

        self.mfmtk = self.mfmtk.apply(pd.to_numeric, errors='ignore')

    def color_mock(self, filter_list, cam, normalized=True):
        '''
            If used with 3 filters creates RGB image. It can
            also be used with several filters with other goals, like
            feeding a CNN with multichannel data
        '''
        if(normalized):
            rgb_factor = 1
            type = np.float32
        else:
            type = int
            rgb_factor = 255

        data = np.array([])
        for i, filter in enumerate(filter_list):
            if(i == 0):
                data = self.get_slice(filter, cam=cam)
            
            if(i > 0):
                data = np.dstack((data, self.get_slice(filter, cam=cam)))

        return data.astype(type)

    def parse_path(self):
        '''
            Extracts snapshot and subfind info in the path
            this only works if the mocks are stored as {snap}_{subfind}.fits.
            A more general approach is not yet implemented.
        '''
        split_path = self.path.split('/')
        
        self.filename = split_path[-1]
        self.snapshot = split_path[-1].split('_')[0]
        self.zf = zs_dict[self.snapshot]
        self.subfind = split_path[-1].split('_')[1].split('.fits')[0]

    def in_Jy(self, data):
        '''
            Return the data in Janskys. 
            Illustris data is in muJy / sr
        '''
        return (data * self.px_in_sr / 1e6) * u.Jy

    def abmag(self, data):
        '''
            Measured the ABmag of given slice
        '''
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
        '''
            Gets a slice of the cube.
            This means the {cam}-13 orientation in {filter_name}
        '''
        filter = filter_dict[filter_name]
        return self.fits[cam].data[filter]

    def get_filter(self, filter_name):
        '''
            Gets all orientation from {filter_name}
        '''
        if(filter_name in filter_dict.keys()):
            filter = filter_dict[filter_name]
            slice = [self.fits[cam].data[filter] for cam in range(14, 18)]
            return slice
        else:
            raise KeyError

    def get_SED(self):
        '''
            Downloads the SED json directly from Illustris
        '''
        subhalo = get(self.url)
        SED = get(subhalo['supplementary_data']['stellar_mocks']['sed'])
        lambdas = SED['L_lambda']
        vals = (SED['lambda_vals'] * u.m).to(u.angstrom)
        return (lambdas, vals)
