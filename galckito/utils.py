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
