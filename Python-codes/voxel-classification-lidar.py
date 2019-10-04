import sys
import numpy as np
from pclib import exportlas, voxelmax
from scipy.ndimage.measurements import label

def readlas(fname):
    from laspy.file import File
    from subprocess import call

    r = call(['laszip', fname])
    if r:
        sys.exit('laszip '+fname+' failed')

    fn = '%s.las' % fname[:-4]
    f = File(fn)
    x = f.x
    y = f.y
    z = f.z
    i = f.return_num
    n = f.num_returns
    l = f.classification
    f.close()
    r = call(['rm', fn])
    if r:
        sys.exit('rm '+fn+' failed')

    return np.transpose((x, y, z, n-i, l))

pfix = sys.argv[1][:-4]
pixw = float(sys.argv[2])

print('read las file ..')
pts = readlas('%s.laz' % pfix)

print('voxel maxima ..')
ix = ((pts[:, 0] - pts[:, 0].min()) / pixw).astype('uint32')
iy = ((pts[:, 1] - pts[:, 1].min()) / pixw).astype('uint32')
iz = ((pts[:, 2] - pts[:, 2].min()) / pixw).astype('uint32')
shape = (iz.max()+1, iy.max()+1, ix.max()+1)
iv = iz * shape[1] * shape[2] + iy * shape[2] + ix
vmax, count = voxelmax(pts[:, 3], iv, np.prod(shape))
vmax.shape = shape
count.shape = shape

print('voxel events ..')
ev = ((vmax == 0) * (count > 0)).astype('uint32')

print('voxel component labeling ..')
cl, nc = label(ev)
print('number of components:', nc)

print('component sizes ..')
cs = np.bincount(cl.ravel())
cmax = cs[1:].max()
print('max component size:', cmax)
print('mean component size:', cs[1:].mean())
print('median component size:', np.median(cs[1:]))

print('classify giant component as ground class 2 ..')
# color var (0,1)
rc = np.zeros(pts.shape[0])

# las class int
rl = np.zeros(pts.shape[0], dtype = 'uint8')

b = cs[cl[iz, iy, ix]] == cmax
rc[b] = 1
rl[b] = 2

b = cs[cl[iz, iy, ix]] < cmax
rc[b] = 0
rl[b] = 4

b = cs[cl[iz, iy, ix]] == cs[0]
rc[b] = 0.5
rl[b] = 3

#print('false ground negatives ..')
#ll = pts[:, 4].astype('int')
#b = ll == 2
#fgneg = np.zeros(pts.shape[0], dtype = 'bool')
#fgneg[b] = rl[b] != 2
#
#print('false ground positives ..')
#b = rl == 2
#fgpos = np.zeros(pts.shape[0], dtype = 'bool')
#fgpos[b] = ll[b] != 2

cs[0] = 1
pcs = np.log10(cs[cl[iz, iy, ix]])

print('export as LAZ files ..')
from matplotlib.cm import viridis_r as cmap
exportlas('%s-class-%.2f.laz' % (pfix, pixw), rc, pts[:, :3], cmap = cmap,
                                              classification = rl)
exportlas('%s-comps-%.2f.laz' % (pfix, pixw), cl[iz, iy, ix].astype('float'),
                                              pts[:, :3], cmap = cmap)
exportlas('%s-csize-%.2f.laz' % (pfix, pixw), pcs, pts[:, :3])

#exportlas('%s-fgpos-%.2f.laz' % (pfix, pixw), pts[fgpos, 2], pts[fgpos, :3],
#                                              classification = ll[fgpos])
#exportlas('%s-fgneg-%.2f.laz' % (pfix, pixw), pts[fgneg, 2], pts[fgneg, :3],
#                                              classification = ll[fgneg])
