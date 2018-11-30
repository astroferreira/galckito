import numpy as np
from scipy import zoom


def z_rescale(data, z1, z2, d1, d2, ps1, ps2):
    '''
        Rescale data from z1 to z2, and from pixel scale ps1
        to pixel scale ps2. This simulates the change of resolution
        if a galaxy at z1 would be observed at z2.

        http://esoads.eso.org/abs/2008ApJS..175..105B
    '''
    scale_factor = (d1 * (1+z2) * ps1) / (d2 * (1+z1) * ps2)
    return zoom(data, scale_factor, prefilter=True)


def gaussian_psf(pixelscale, angularFWHM, shape):
    '''
        Generates a simulated PSF from a Gaussian distribution
        pixelscale: instrument pixel scale
        angularFWHM: FWHM of the instrument
        shape: shape of the output
    '''
    FWHM = angularFWHM/pixelscale
    gaussian = np.zeros(shape)
  
    Xc = np.floor(shape[0]/2)
    Yc = np.floor(shape[1]/2)
    
    sigma = FWHM/2.354

    for i in range(0, shape[0], 1):
        for j in range(0, shape[1], 1):
            r = np.sqrt((i-Xc)**2 + (j-Yc)**2)
            gaussian[i][j] = np.exp(-(r)**2./(2*sigma**2))
            
    gaussian = gaussian/gaussian.sum()
    return gaussian


def moffat_psf(pixelscale, angularFWHM, shape):
    '''
        Generates a simulated PSF from a Moffat distribution
        pixelscale: instrument pixel scale
        angularFWHM: FWHM of the instrument
        shape: shape of the output
    '''
    FWHM = angularFWHM/pixelscale
    beta = 4.765
    a = FWHM/(2*(2**(1./beta) - 1))
    moffat = np.zeros(shape)
  
    Xc = np.floor(shape[0]/2)
    Yc = np.floor(shape[1]/2)
    
    sigma = FWHM/2.354
    for i in range(0, shape[0], 1):
        for j in range(0, shape[1], 1):
            r = np.sqrt((i-Xc)**2 + (j-Yc)**2)
            moffat[i][j] = ((beta-1)/(np.pi*a**2))*(1+(r/a)**2.)**(-beta)
            
    moffat = moffat/moffat.sum()
    return moffat

