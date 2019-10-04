# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as pl
 
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
 
def fitsphere(pts):
    # CuPy should be faster for large point clouds
    # i.e., pts.shape[0] > 1e5
    #from numpy.linalg import lstsq
    from scipy.linalg import lstsq
 
    A = np.zeros((pts.shape[0], 4))
    x, y, z = pts[:,0], pts[:,1], pts[:,2]
    A[:,0] = x * 2
    A[:,1] = y * 2
    A[:,2] = z * 2
    A[:,3] = 1
    f = np.zeros((len(x), 1))
    f[:,0] = x*x + y*y + z*z
    c, resid, rank, sval = lstsq(A, f)
    r = np.sqrt(c[0]*c[0] + c[1]*c[1] + c[2]*c[2] + c[3])
    return (r, c[0], c[1], c[2])
 
if __name__ == '__main__': 
    from laspy.file import File
    fname = 'C:\\Users\\bodob\\Downloads\\MavicPro2_c2c_ground.las'
 
    print('reading', fname)
    f = File(fname)
    x = f.x
    y = f.y
    z = f.z
    classification = f.classification
    dz = getattr(f,'c2c_absolute_distances_(z)').copy()
    f.close()
 
    print('c2c absolute distances (z):')
    print('pre min, mean, max:', dz.min(), dz.mean(), dz.max())
    #in case, you have not used the CSF classification (or you have used a different way of classifying your PC)
    j = (-2 <= dz) * (dz <= 2)
    xj, yj, dzj = x[j], y[j], dz[j]
    dzj *= 10
    print('post min, mean, max:', dzj.min(), dzj.mean(), dzj.max())
 
    #print('extract ground class ..')
    pts = np.transpose((xj, yj, dzj))
    #pts = pts[classification[j] == 2]
    
    print('fit spherical error model to ground component ..')
    ptsmin = pts.min(axis = 0)
    R, x0, y0, z0 = fitsphere(pts-ptsmin)
    x0 += ptsmin[0]
    y0 += ptsmin[1]
    z0 += ptsmin[2]
 
    # transform (x, y, z) -> (x, y, z-zsphere)
    zsphere = z0 - np.sqrt(R*R - (x-x0)**2-(y-y0)**2)
    zsphere /= 10
    cpts = np.transpose((x, y, z-zsphere))
 
    print('export corrected point cloud to LAZ file ..')
    exportlas('%s_spherical_corrected.laz' % fname[:-4], cpts[:,2], cpts)
 
    print('plane fit on the residuals ..')
    from scipy.linalg import lstsq
    A = np.transpose((x, y, np.ones(len(x))))
    r = dz - zsphere
    c, resid, rank, sval = lstsq(A, r)
    print(c)
    # z of the residual plane
    #zrp = c[0]*x + c[1]*y + c[2]
 
    print('export error model residuals to LAZ file ..')
    exportlas('%s_model_residuals.las' % fname[:-4], r,
              (pts[:,0], pts[:,1], r))