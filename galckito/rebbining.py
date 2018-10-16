import numpy as np
import scipy.interpolate


def congrid(a, newdims, centre=False, minusone=False):
    ''' Slimmed down version of congrid as originally obtained from:
		http:Rebinning//wiki.scipy.org/Cookbook/
    '''
    if not a.dtype in [np.float64, np.float32]:
        a = np.cast[float](a)
    m1 = np.cast[int](minusone)
    ofs = np.cast[int](centre) * 0.5
    old = np.array( a.shape )
    ndims = len( a.shape )
    if len( newdims ) != ndims:
        print( "[congrid] dimensions error. " \
              "This routine currently only support " \
              "rebinning to the same number of dimensions.")
        return None
    newdims = np.asarray( newdims, dtype=float )
    dimlist = []



    for i in range( ndims ):
        base = np.arange( newdims[i] )
        dimlist.append( (old[i] - m1) / (newdims[i] - m1) \
                            * (base + ofs) - ofs )
    # specify old dims
    olddims = [np.arange(i, dtype = np.float) for i in list( a.shape )]

    # first interpolation - for ndims = any
    mint = scipy.interpolate.interp1d( olddims[-1], a, kind='linear', bounds_error=False, fill_value=0.0 )
    newa = mint( dimlist[-1] )

    trorder = [ndims - 1] + list(range( ndims - 1 ))
    for i in range( ndims - 2, -1, -1 ):
        newa = newa.transpose( trorder )

        mint = scipy.interpolate.interp1d( olddims[i], newa, kind='linear', bounds_error=False, fill_value=0.0 )
        newa = mint( dimlist[i] )

    if ndims > 1:
        # need one more transpose to return to original dimensions
        newa = newa.transpose( trorder )

    return newa