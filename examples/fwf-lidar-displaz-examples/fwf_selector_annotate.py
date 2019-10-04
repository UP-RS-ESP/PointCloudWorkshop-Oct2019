import sys
import numpy as np
from matplotlib import pyplot as pl

from subprocess import call, check_output
from fwflib import loadfwf, get_vlr_from_las, exportlas

fname = 'Haus29_ID04_FWF_V14_xyzinrtWV.asc'
UTM_XYZ, intensity, return_index, gps_time, wpd, byte_offset_wf_data, ref_location_offset, dxdydz, _, _, wf = loadfwf(fname)

lasfname = 'Haus29_ID04_FWF.las'
_, _, vlr_bits_per_sample, vlr_compression, vlr_samples, vlr_temporal, vlr_gain, vlr_wpd = get_vlr_from_las(lasfname)

def show_fwf(coord, pts):
    global m
    b = (coord == pts).all(axis = 1)
    if len(b[b]) > 0:
        m += 1

        # get first match
        i = np.where(b)[0][0]

        b = vlr_wpd == wpd[i]
        step = vlr_temporal[b]
        ampl = wf[i] * vlr_gain[b]
    
        # remove background noise
        ampl -= ampl[0:3].mean()
        ampl[ampl < 0] = 0
 
        V = dxdydz[i,:]
        S_x = UTM_XYZ[i,0] + ref_location_offset[i] * V[0]
        S_y = UTM_XYZ[i,1] + ref_location_offset[i] * V[1]
        S_z = UTM_XYZ[i,2] + ref_location_offset[i] * V[2]

        pulse_x = S_x - np.arange(len(ampl)) * step * V[0]
        pulse_y = S_y - np.arange(len(ampl)) * step * V[1]
        pulse_z = S_z - np.arange(len(ampl)) * step * V[2]

        exportlas('tmp_sel%i.las' % m, ampl,
                  np.transpose((pulse_x, pulse_y, pulse_z)))
        call(['displaz', '-script', 'tmp_sel%i.las' % m])

        pl.title('full wave form at (%.3f, %.3f, %.3f)' % (coord[0], coord[1], coord[2]))
        pl.plot(pulse_z, ampl, lw = 1, alpha = 0.7, label = 'p %i' % m)
        pl.xlabel('Elevation [m]')
        pl.ylabel('Amplitude')
        call(['displaz', '-annotation', 'p %i' % m, '%.3f' % coord[0], '%.3f' % coord[1], '%.3f' % coord[2]])
        pl.legend(loc = 'upper right')

# load LAS file into displaz and start interaction
exportlas('tmp.las', intensity.astype('float64'), UTM_XYZ)
call(['displaz', '-script', 'tmp.las'])
pl.ion()
xo, yo, zo = 0, 0, 0
m = 0

pts = np.round(UTM_XYZ, decimals = 3)

while True:
    xs, ys, zs = map(float, str(check_output('displaz -script -querycursor', shell = True), 'utf-8').split())
    d = np.sqrt((xs-xo)**2+(ys-yo)**2+(zs-zo)**2)
    if d:
        show_fwf(np.round([xs, ys, zs], decimals = 3), pts)
        xo, yo, zo = xs, ys, zs
    else:
        pl.pause(1)
