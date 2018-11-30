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


def norm(data):
    '''
        Normalize the image to range [0, 1].
    '''
    return (data-data.min())/(data.max() - data.min())
