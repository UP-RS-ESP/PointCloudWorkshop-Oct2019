import numpy as np

def exportlas(fn, var, pnts, cmap = None):
    import laspy
    if cmap is None:
        from matplotlib.cm import magma_r
        cmap = magma_r

    v = var - np.min(var)
    v /= v.max()
    rgb = cmap(v)
    rgb = rgb[:, :3]
    rgb *= 65535
    rgb = rgb.astype('uint')
    header = laspy.header.Header()
    header.data_format_id = 2
    f = laspy.file.File(fn, mode = 'w', header = header)
    f.header.scale = [0.001, 0.001, 0.001]
    f.header.offset = [pnts[:,0].min(), pnts[:,1].min(), pnts[:,2].min()]
    f.x = pnts[:, 0]
    f.y = pnts[:, 1]
    f.z = pnts[:, 2]
    if pnts.shape[1] == 4:
        f.intensity = pnts[:, 3]
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
    with open(fn, 'r') as f:
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
    return (np.array(UTM_XYZ), np.array(intensity), np.array(return_index), 
            np.array(gps_time), np.array(wavepacket_descriptor), np.array(byte_offset_wf_data), 
            np.array(ref_location_offset_ps), np.array(dxdydz), np.array(nrbits), np.array(nrofwfsamples), np.array(wf))

