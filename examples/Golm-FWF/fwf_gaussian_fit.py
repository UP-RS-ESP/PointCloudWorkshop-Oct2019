#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 21:17:20 2019

@author: bodo
"""
import numpy as np
from matplotlib import pyplot as pl
from subprocess import call, check_output
from lmfit import Model
import progressbar, sys
from multiprocessing import Pool
import psutil

def savelas(fn, var, intensity, pnts, cmap = pl.cm.magma_r):
   import laspy

   v_0298p = np.percentile(var, [2, 98])
   #var[var<v_0298p[0]] = v_0298p[0]
   #var[var>v_0298p[1]] = v_0298p[1]
   v = var - v_0298p[0]
   v /= v_0298p[1]
   rgb = cmap(v)
   rgb = rgb[:, :3]
   rgb *= 65535
   rgb = rgb.astype('uint32')
   header = laspy.header.Header()
   header.data_format_id = 2
   f = laspy.file.File(fn, mode = 'w', header = header)
   f.header.scale = [0.001, 0.001, 0.001]
   f.header.offset = [pnts[:,0].min(), pnts[:,1].min(), pnts[:,2].min()]
   f.x = pnts[:, 0]
   f.y = pnts[:, 1]
   f.z = pnts[:, 2]
   f.intensity = intensity
   f.set_red(rgb[:, 0])
   f.set_green(rgb[:, 1])
   f.set_blue(rgb[:, 2])
   f.close()

def get_vlr_from_las(lasfname):
    import laspy
    
    lasfile = laspy.file.File(lasfname, mode='r')
    byteoffsettowaveformdata = lasfile.byte_offset_to_waveform_data
    return_point_waveform_loc = lasfile.get_return_point_waveform_loc()
    
    wf_vlrs = lasfile.header.vlrs
    vlr_bits_per_sample = []
    vlr_compression = []
    vlr_samples = []
    vlr_temporal = []
    vlr_gain = []
    vlr_wdp = []
    for vlr in wf_vlrs:
        if vlr.reserved == 43707 and vlr.user_id == 'LASF_Spec\x00\x00\x00\x00\x00\x00\x00':
            #index 1 bits/sample 16 compression 0 samples 32 temporal 1005 gain 1, offset 0
            vlr_bits_per_sample.append(vlr.parsed_body[0])
            vlr_compression.append(vlr.parsed_body[1])
            vlr_samples.append(vlr.parsed_body[2])
            vlr_temporal.append(vlr.parsed_body[3])
            vlr_gain.append(vlr.parsed_body[4])
            description = vlr.description
            vlr_wdp.append(int(description.split('#')[1].split('\x00')[0]))
            #print('WDP#%d: temporal: %d'%(description_wdp, temporal))
    #lasfile.close()
    return(byteoffsettowaveformdata, return_point_waveform_loc, np.array(vlr_bits_per_sample), 
           np.array(vlr_compression), np.array(vlr_samples), np.array(vlr_temporal), np.array(vlr_gain), np.array(vlr_wdp) )

def loadfwf(fn):
    UTM_XYZ = []
    intensity = []
    return_index = []
    gps_time = []
    wavepacket_descriptor = []
    byte_offset_wf_data = []
    ref_location_offset_ps = []
    dxdydz = []
    nrbits = []
    nrofwfsamples = []
    wf = []
    with open(fn, 'r', encoding="ISO-8859-1", errors='ignore') as f:
        for l in f:
            i = l.split(' ')
            UTM_XYZ.append(np.array(i[0:3], dtype = 'float'))
            intensity.append(np.array(i[3], dtype = 'int16'))
            return_index.append(np.array(i[4:6], dtype = 'int8'))
            gps_time.append(np.array(i[6], dtype = 'float'))
            wavepacket_descriptor.append(np.array(i[7], dtype = 'int'))
            byte_offset_wf_data.append(np.array(i[8:10], dtype = 'int'))
            ref_location_offset_ps.append(np.array(i[10], dtype = 'int'))
            dxdydz.append(np.array(i[11:14], dtype = 'float'))
            nrbits.append(np.array(i[14], dtype = 'int'))
            nrofwfsamples.append(np.array(i[15], dtype = 'int'))
            wf.append(np.array(i[16:], dtype = 'int'))
    #m = np.loadtxt(fn, usecols = (0, 1, 2, 3))
    return (np.array(UTM_XYZ), np.array(intensity), np.array(return_index), 
            np.array(gps_time), np.array(wavepacket_descriptor), np.array(byte_offset_wf_data), 
            np.array(ref_location_offset_ps), np.array(dxdydz), np.array(nrbits), np.array(nrofwfsamples), np.array(wf))

def show_fwf(crd, pts, fwf):
    b = (crd == pts).all(axis = 1)
    if len(b[b]) > 0:
        i = np.arange(len(fwf))
        w = fwf[i[b][0]]
        pl.clf()
        pl.title('full wave form at (%.3f, %.3f, %.3f)' % (crd[0], crd[1], crd[2]))
        pl.plot(w, 'k-', lw = 1)
        pl.xlabel('time')
        pl.ylabel('amplitude')

# load ASCII and store as numpy arrays
fname = sys.argv[1]
#fname = 'Haus29_ID04_FWF_V13_xyzinrtWV.asc'
print('Loading %s...'%fname, end='', flush=True)
UTM_XYZ, intensity, return_index, gps_time, wavepacket_descriptor, byte_offset_wf_data, ref_location_offset_ps, dxdydz, nrbits, nrofwfsamples, wf = loadfwf(fname)
print(' done', flush=True)

lasfname = sys.argv[2]
#lasfname = 'Haus29_ID04_FWF_V13.laz'
print('Loading %s...'%lasfname, end='', flush=True)
byteoffsettowaveformdata, return_point_waveform_loc, vlr_bits_per_sample, vlr_compression, vlr_samples, vlr_temporal, vlr_gain, vlr_wdp = get_vlr_from_las(lasfname)
print(' done', flush=True)

#iterate through all points and fit gaussians
def gaussian(x, amp, cen, wid):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (np.sqrt(2*np.pi) * wid)) * np.exp(-(x-cen)**2 / (2*wid**2))

def fit_gaussian(y,x_ns,pt_intensity,identified_point_ns,wid=1):
    gmodel = Model(gaussian)
    result = gmodel.fit(y, x=x_ns, amp=pt_intensity, cen=identified_point_ns, wid=wid)
    peak_width = result.best_values['wid']
    peak_amp = result.best_values['amp']
    peak_center = result.best_values['cen']
    return peak_width, peak_amp, peak_center

peak_width = np.empty_like(gps_time)
peak_amp = np.empty_like(gps_time)
peak_center = np.empty_like(gps_time)
bar = progressbar.ProgressBar(maxval=intensity.shape[0])
bar.start()
for i in range(0,intensity.shape[0]):
    wdp_id = wavepacket_descriptor[i]
    pt_intensity = intensity[i]
    vlr_wdp_index = np.where(wdp_id == vlr_wdp)[0][0]
    identified_point_ps = ref_location_offset_ps[i]
    nr_of_samples = nrofwfsamples[i]
    x_ns =  np.linspace(0,nr_of_samples*vlr_temporal[vlr_wdp_index], nr_of_samples) * 1e-3
    y = wf[i] * vlr_gain[vlr_wdp_index]
    y_background = np.mean(y[0:3])
    y = y - y_background
    y[y<0] = 0
    peak_width[i], peak_amp[i], peak_center[i] = fit_gaussian(y, x_ns, pt_intensity, identified_point_ps/1000, 1)
    bar.update(i)
bar.finish()
np.save('Haus29_ID04_FWF_V13_width', peak_width)
np.save('Haus29_ID04_FWF_V13_amp', peak_amp)
np.save('Haus29_ID04_FWF_V13_center', peak_center)

print('Mean, Median, Stddev peak_width: %3.2f, %3.2f, %3.2f'%(np.mean(peak_width), np.median(peak_width), np.std(peak_width)))
wid_lasfname = lasfname[:-4] + '_width.las'
print('Saving %s...'%wid_lasfname, end='', flush=True)
savelas(wid_lasfname, peak_width, intensity, UTM_XYZ)
print('done', flush=True)

#amp_lasfname = 'Haus29_ID04_FWF_V13_amp.laz'
amp_lasfname = lasfname[:-4] + '_amp.las'
print('Saving %s...'%amp_lasfname, end='', flush=True)
savelas(amp_lasfname, peak_amp, intensity, UTM_XYZ)
print('done', flush=True)
