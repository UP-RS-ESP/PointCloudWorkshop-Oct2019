import numpy as np
from matplotlib import pyplot as pl
from scipy.interpolate import UnivariateSpline
from scipy.signal import find_peaks

from fwflib import loadfwf, get_vlr_from_las, exportlas

fname = 'Haus29_ID04_FWF_V14_xyzinrtWV.asc'
UTM_XYZ, intensity, return_index, gps_time, wpd, byte_offset_wf_data, ref_location_offset, dxdydz, _, _, wf = loadfwf(fname)

lasfname = 'Haus29_ID04_FWF.las'
_, _, vlr_bits_per_sample, vlr_compression, vlr_samples, vlr_temporal, vlr_gain, vlr_wpd = get_vlr_from_las(lasfname)

i = 198
i = 199
#i = 200
print(return_index[198:201,:])

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

pl.plot(t, ampl, 'ro', fillstyle = 'none')
pl.plot(s[peaks], usp(s)[peaks], 'ko', ms = 13, fillstyle = 'none')
pl.plot(s[peaks], usp(s)[peaks], 'kx', ms = 10)
pl.plot(s, usp(s))
pl.axvline(x = ref_location_offset[i], c = 'r')
pl.grid()
pl.xlabel('Time [ps]')
pl.ylabel('Amplitude')
pl.title('Full Waveform of index %d' % i)
pl.show()

V = dxdydz[i,:]
S_x = UTM_XYZ[i,0] + ref_location_offset[i] * V[0]
S_y = UTM_XYZ[i,1] + ref_location_offset[i] * V[1]
S_z = UTM_XYZ[i,2] + ref_location_offset[i] * V[2]

pulse_x = S_x - np.arange(len(ampl)) * step * V[0]
pulse_y = S_y - np.arange(len(ampl)) * step * V[1]
pulse_z = S_z - np.arange(len(ampl)) * step * V[2]
pts = np.transpose((pulse_x, pulse_y, pulse_z))
rgb = ampl

exportlas('%s_id%i.las' % (lasfname[:-4], i), rgb, pts)

pts_x = S_x - s[peaks] * V[0]
pts_y = S_y - s[peaks] * V[1]
pts_z = S_z - s[peaks] * V[2]
pts = np.transpose((pts_x, pts_y, pts_z))
rgb = usp(s)[peaks]

pts = pts[rgb > 20]
rgb = rgb[rgb > 20]

exportlas('%s_id%i_pts.las' % (lasfname[:-4], i), rgb, pts)

