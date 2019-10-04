import sys
import numpy as np

def voxelmax(double[::] v, unsigned int[::] iv, unsigned int m):
    cdef unsigned int k, n
    cdef unsigned int[::] c
    cdef double[::] a

    n = len(iv)
    a = np.zeros(m, dtype = 'float64')
    c = np.zeros(m, dtype = 'uint32')
    for k in range(n):
        c[iv[k]] += 1
        if v[k] > a[iv[k]]:
            a[iv[k]] = v[k]
    return (np.asarray(a), np.asarray(c))

def exportlas(fname, var, pnts, cmap = None, classification = None):
    import laspy
    import os
    from subprocess import call

    if cmap is None:
        from matplotlib.cm import magma_r
        cmap = magma_r

    fn, fe = os.path.splitext(fname)
    v = var - np.min(var)
    v /= v.max()
    rgb = cmap(v)
    rgb = rgb[:, :3]
    rgb *= 65535
    rgb = rgb.astype('uint')
    header = laspy.header.Header()
    header.data_format_id = 2
    f = laspy.file.File('%s.las' % fn, mode = 'w', header = header)
    f.header.scale = [0.001, 0.001, 0.001]
    f.header.offset = [pnts[:,0].min(), pnts[:,1].min(), pnts[:,2].min()]
    f.x = pnts[:, 0]
    f.y = pnts[:, 1]
    f.z = pnts[:, 2]
    if classification is not None:
        f.classification = classification
    f.set_red(rgb[:, 0])
    f.set_green(rgb[:, 1])
    f.set_blue(rgb[:, 2])
    f.close()
    try:
        r = call(['laszip', '%s.las' % fn])
        if not r:
            r = call(['rm', '%s.las' % fn])
    except:
        pass

def hillshade(array, azimuth = 315, angle_altitude = 45):
    '''
    Roger Veciana i Rovira (2014)
    https://raw.githubusercontent.com/rveciana/introduccion-python-geoespacial/master/hillshade.py
    '''
    azimuth = 360.0 - azimuth 
    x, y = np.gradient(array)
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)
    azimuthrad = azimuth * np.pi / 180.
    altituderad = angle_altitude * np.pi / 180.
    shaded = np.sin(altituderad) * np.sin(slope)\
           + np.cos(altituderad) * np.cos(slope)\
           * np.cos((azimuthrad - np.pi/2.) - aspect)
    return 255 * (shaded + 1) / 2

cdef extern from 'main.c':
    #void cvoxelize(unsigned int *r, const unsigned int *x,
    #    const unsigned int n, const unsigned int m)
    void cvoxelstats(double *mean, double *stdr, unsigned int *count,
        const double *v, const unsigned int *x,
        const unsigned int n, const unsigned int m)

def voxelstats(const double[::] var, const unsigned int[::] x, const unsigned int m):
    cdef unsigned int n
    cdef unsigned int[::] count
    cdef double[::] mean, stdr

    n = len(x)
    count = np.zeros(m, dtype = 'uint32')
    mean = np.zeros(m, dtype = 'float64')
    stdr = np.zeros(m, dtype = 'float64')
    cvoxelstats(&mean[0], &stdr[0], &count[0], &var[0], &x[0], n, m)
    return (np.asarray(mean), np.asarray(stdr), np.asarray(count))

