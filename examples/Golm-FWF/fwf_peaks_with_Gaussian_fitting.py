import numpy as np
from matplotlib import pyplot as pl
from scipy.interpolate import UnivariateSpline
from scipy.signal import find_peaks

from fwflib import loadfwf, get_vlr_from_las, exportlas

fname = 'Haus29_ID04_FWF_V14_xyzinrtWV.asc'
UTM_XYZ, intensity, return_index, gps_time, wpd, byte_offset_wf_data, ref_location_offset, dxdydz, _, _, wf = loadfwf(fname)

lasfname = 'Haus29_ID04_FWF.las'
_, _, vlr_bits_per_sample, vlr_compression, vlr_samples, vlr_temporal, vlr_gain, vlr_wpd = get_vlr_from_las(lasfname)

#i = 31731
#i = 199
#i = 200
i=31731
print(return_index[31731:31735,:])

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
peaks, properties = find_peaks(usp(s), prominence = 2)

pl.plot(t, ampl, 'ro', fillstyle = 'none')
pl.plot(s[peaks], usp(s)[peaks], 'ko', ms = 13, fillstyle = 'none')
pl.plot(s[peaks], usp(s)[peaks], 'kx', ms = 10)
pl.plot(s, usp(s))
pl.axvline(x = ref_location_offset[i], c = 'r')
pl.axvline(x = ref_location_offset[i+1], c = 'r')
pl.axvline(x = ref_location_offset[i+2], c = 'r')
pl.axvline(x = ref_location_offset[i+3], c = 'r')
pl.grid()
pl.xlabel('Time [ps]')
pl.ylabel('Amplitude')
pl.title('Full Waveform of index %d' % i)
pl.show()

#Perform Gaussian Fitting
from lmfit import Model

def gaussian(x, amp, cen, wid):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (np.sqrt(2*np.pi) * wid)) * np.exp(-(x-cen)**2 / (2*wid**2))

def fit_gaussian(y, x_ns, pt_intensity, identified_point_ns, wid=1):
    gmodel = Model(gaussian)
    result = gmodel.fit(y, x=x_ns, amp=pt_intensity, cen=identified_point_ns, wid=wid)
    peak_width = result.best_values['wid']
    peak_amp = result.best_values['amp']
    peak_center = result.best_values['cen']
    return peak_width, peak_amp, peak_center

y = ampl
peak_width = np.empty( (len(peaks),1) )
peak_amp = np.empty( (len(peaks),1) )
peak_center = np.empty( (len(peaks),1) )
for j in range(len(peaks)):
    initial_peak_x = s[peaks[j]]
    initial_peak_y = usp(s)[peaks[j]]
    peak_width[j], peak_amp[j], peak_center[j] = \
        fit_gaussian(y, t/1000, initial_peak_y, initial_peak_x/1000, 1)

fitted_gaussian_y1 = gaussian(t/1000, peak_amp[0], peak_center[0], peak_width[0])
fitted_gaussian_y2 = gaussian(t/1000, peak_amp[1], peak_center[1], peak_width[1])
fitted_gaussian_y3 = gaussian(t/1000, peak_amp[2], peak_center[2], peak_width[2])
fitted_gaussian_y4 = gaussian(t/1000, peak_amp[3], peak_center[3], peak_width[3])
pl.plot(t, fitted_gaussian_y1, 'k-', linewidth=2)
pl.plot(t, fitted_gaussian_y2, 'k-', linewidth=2)
pl.plot(t, fitted_gaussian_y3, 'k-', linewidth=2)
pl.plot(t, fitted_gaussian_y4, 'k-', linewidth=2)



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
