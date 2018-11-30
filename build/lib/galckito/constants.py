filter_dict = {'GALAX FUV': 0, 'GALAX NUV':1, 'SDSS-u':2, 'SDSS-g':3,
               'SDSS-r':4, 'SDSS-i':5, 'SDSS-z':6, 'IRAC1':7, 
               'IRAC2':8, 'IRAC3':9, 'IRAC4':10, 'Johnson-U':11,
               'Johnson-B':12, 'Cousins-R':13, 'Cousins-I':14,
               'Johnson-V':15, 'Johnson-J':16, 'Johnson-H':17, 
               'Johnson-K':18, '2MASS-H':19, '2MASS-Ks':20, 
               'ACS-F435':21, 'ACS-F606':22, 'ACS-F775':23,
               'ACS-F850':24, 'f105w':25, 'f125w':26, 'f160w':27, 
               'NIRCAM-F070W': 28, 'NIRCAM-F090W':29, 'NIRCAM-F115W':30,
               'NIRCAM-F150W':31, 'NIRCAM-F200W': 32, 'NIRCAM-F277W': 33,
               'NIRCAM-F356W':34, 'NIRCAM-F444W':35}

mfmtk_columns = ['rootname','Mo','No','psffwhm','asecpix','skybg',
                 'skybgstd','x0peak ','y0peak','x0col','y0col',
                 'x0A1fit','y0A1fit','x0A3fit','y0A3fit','a','b',
                 'PAdeg','InFit1D','RnFit1D','nFit1D','xsin',
                 'x0Fit2D','y0Fit2D','InFit2D','RnFit2D','nFit2D',
                 'qFit2D','PAFit2D','LT','R10','R20','R30','R40',
                 'R50','R60','R70','R80','R90','Rp', 'C1','C2','A1',
                 'A2','A3','A4','S1','S3','G','M20','psi','sigma_psi',
                 'H','IRkurvmedian', 'IRkurvmad','QF']

zs_dict = {'135': 0.05, '103': 0.5, '85': 1, '75': 1.5, '68': 2,
           '64': 2.5, '60': 3, '54': 4, '49': 5, '45': 6, 
           '41': 7, '38': 8, '35': 9}