import numpy as np

def gaussian_psf(pixelscale, angularFWHM, shape):

    FWHM = angularFWHM/pixelscale
    gaussian   = np.zeros(shape)
  
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

    FWHM = angularFWHM/pixelscale
    beta = 4.765
    a = FWHM/(2*(2**(1./beta) - 1))
    moffat   = np.zeros(shape)
  
    Xc = np.floor(shape[0]/2)
    Yc = np.floor(shape[1]/2)
    
    sigma = FWHM/2.354
    for i in range(0, shape[0], 1):
        for j in range(0, shape[1], 1):
            r = np.sqrt((i-Xc)**2 + (j-Yc)**2)
            moffat[i][j] = ((beta-1)/(np.pi*a**2))*(1+(r/a)**2.)**(-beta)
            
    moffat = moffat/moffat.sum()
    return moffat 

