import numpy as np
from matplotlib import pyplot as pl
from scipy.interpolate import UnivariateSpline
from scipy.signal import find_peaks

from fwflib import loadfwf, get_vlr_from_las, exportlas

fname = 'Haus29_ID04_FWF_V14_xyzinrtWV.asc'
UTM_XYZ, intensity, return_index, gps_time, wpd, byte_offset_wf_data, ref_location_offset, dxdydz, _, _, wf = loadfwf(fname)

lasfname = 'Haus29_ID04_FWF.las'
_, _, vlr_bits_per_sample, vlr_compression, vlr_samples, vlr_temporal, vlr_gain, vlr_wpd = get_vlr_from_las(lasfname)

from laspy.file import File
f = File(lasfname)
x = f.x
y = f.y
z = f.z
r = f.intensity
exportlas('%s_intensity.las' % lasfname[:-4], r.astype('float64'), np.transpose((x, y, z, r)))

n = return_index.shape[0]
pts = np.zeros((n * 3, 3))
rgb = np.zeros(n * 3)
j = 0
for i in range(n):
    if return_index[i,1] > 1:
        continue

    print(i/n)
    b = vlr_wpd == wpd[i]
    step = vlr_temporal[b]
    ampl = wf[i] * vlr_gain[b]
    
    # remove background noise
    ampl -= ampl[0:3].mean()
    ampl[ampl < 0] = 0
    
    # wave form times [ps]
    t = np.arange(0, len(ampl) * step, step)
    s = np.arange(0, len(ampl) * step, step/4)
    
    usp = UnivariateSpline(t, ampl)
    peaks, properties = find_peaks(usp(s), prominence = 5)

    V = dxdydz[i,:]
    S_x = UTM_XYZ[i,0] + ref_location_offset[i] * V[0]
    S_y = UTM_XYZ[i,1] + ref_location_offset[i] * V[1]
    S_z = UTM_XYZ[i,2] + ref_location_offset[i] * V[2]

    #pulse_x = S_x - np.arange(len(ampl)) * step * V[0]
    #pulse_y = S_y - np.arange(len(ampl)) * step * V[1]
    #pulse_z = S_z - np.arange(len(ampl)) * step * V[2]
    #pts = np.transpose((pulse_x, pulse_y, pulse_z))
    
    pts_x = S_x - s[peaks] * V[0]
    pts_y = S_y - s[peaks] * V[1]
    pts_z = S_z - s[peaks] * V[2]
    ptsi = np.transpose((pts_x, pts_y, pts_z))
    ampi = usp(s)[peaks]
    
    #ptsi = ptsi[ampi > 20]
    #ampi = ampi[ampi > 20]
    m = len(ampi)
    pts[j:j+m,:] = ptsi[:]
    rgb[j:j+m] = ampi[:]
    j += m

pts = pts[:j]
rgb = rgb[:j]
exportlas('%s_densify.las' % lasfname[:-4], rgb, pts)

