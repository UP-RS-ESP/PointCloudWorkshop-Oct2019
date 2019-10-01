import sys
import numpy as np
from pclib import exportlas, voxelstats
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
    l = f.classification
    f.close()
    r = call(['rm', fn])
    if r:
        sys.exit('rm '+fn+' failed')

    return np.transpose((x, y, z, l))


pfix = sys.argv[1][:-4]
pixw = float(sys.argv[2])

print('read las file ..')
pts = readlas('%s.laz' % pfix)

print('voxel stats ..')
ix = ((pts[:, 0] - pts[:, 0].min()) / pixw).astype('uint32')
iy = ((pts[:, 1] - pts[:, 1].min()) / pixw).astype('uint32')
iz = ((pts[:, 2] - pts[:, 2].min()) / pixw).astype('uint32')
shape = (iz.max()+1, iy.max()+1, ix.max()+1)
iv = iz * shape[1] * shape[2] + iy * shape[2] + ix
mean, stdr, count = voxelstats(pts[:, 2], iv, np.prod(shape))
mean.shape = shape
stdr.shape = shape
count.shape = shape

from matplotlib import pyplot as pl
pl.figure(1, (19.2, 10.8))
stdthr = np.nanpercentile(stdr, 50)
pl.hist(stdr[~np.isnan(stdr)], bins = 'auto', log = True)
pl.axvline(x = stdthr, color = 'r')
pl.ylabel('counts')
pl.xlabel('voxel elevation standard deviation')
pl.savefig('%s-stdr-%0.2f.png' % (pfix, pixw))

#print('export as LAZ files ..')
#exportlas('%s-mean-%.2f.laz' % (pfix, pixw), mean[iz,iy,ix], pts[:, :3])
#exportlas('%s-stdr-%.2f.laz' % (pfix, pixw), stdr[iz,iy,ix], pts[:, :3])
#exportlas('%s-count-%.2f.laz' % (pfix, pixw), count[iz,iy,ix].astype('float'), pts[:, :3])

stdr[np.isnan(stdr)] = np.nanmax(stdr)

print('voxel events ..')
ev = ((stdr < stdthr) * (count > 0)).astype('uint32')

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
rc = np.zeros(pts.shape[0])
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
#
#print('sum of false positives and negatives:', len(ix[fgpos])+len(ix[fgneg]))

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
