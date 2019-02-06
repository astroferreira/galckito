'''
    Data handling and other tools
'''

from .constants import ILL_HEADERS

import requests


def get(path, params=None):
    '''
        Function adapted from Illustris scripts
        (https://bitbucket.org/illustris/illustris_python)
    '''
    r = requests.get(path, params=params, headers=ILL_HEADERS)

    r.raise_for_status()

    if r.headers['content-type'] == 'application/json':
        return r.json()

    if 'content-disposition' in r.headers:
        filename = r.headers['content-disposition'].split("filename=")[1]
        with open(filename, 'wb') as f:
            f.write(r.content)
        return filename

    return r


def norm(data):
    '''
        Normalize the image to range [0, 1].
    '''
    return (data-data.min())/(data.max() - data.min())


def ab_to_flux(mag):
    Fo = 3631
    return Fo * 10**(-0.4*mag)

def abmag(flux, area=1):
    return -2.5*np.log10(flux / 3631) + 2.5*np.log10(area)

def abmag2(flux, area=1):
    return -2.5*np.log10(flux / area / 3631 /area)

def SNR(flux, bg_flux, area, t):
    return flux*area*t/np.sqrt(flux*area*t + area*bg_flux*t)

def muJysr_to_Jy(data):

    sr_to_arcsec = 2.35 / 1e11

    # sr to arcsec²
    muJy_arc2 = data * sr_to_arcsec
    
    # myJy to Jy
    Jy_arc2 = muJy_arc2 / 1e6
    
    area = (1. / px_in_arcsec**2) * (data.shape[0]**2)
    
    # Jy / arcsec² to Jy
    in_Jy = Jy_arc2 * area 

    return in_Jy

        