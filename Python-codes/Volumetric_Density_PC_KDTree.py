#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 11:36:08 2019

@author: bodo
"""

import argparse, numpy as np, pandas as pd, timeit, os, subprocess
import matplotlib.cm as cm
import laspy

def write_LAS(pc_xyz, v, output_las_fn, input_las_fn, cmap=cm.terrain, rescale='none'):
    import datetime
    from laspy.file import File
    from skimage import exposure
    import copy
    
    inFile = File(input_las_fn, mode='r')

    #normalize input and generate colors for height using colormap
    #stretch to 10-90th percentile
    #v_1090p = np.percentile(v, [10, 90])
    #stretch to 2-98th percentile
    v_0298p = np.percentile(v, [2, 98])
    if rescale == 'none':
        v_rescale = exposure.rescale_intensity(v, in_range=(v_0298p[0], v_0298p[1]))
    elif rescale == 'median':
        bounds = np.round(np.median(np.abs(v_0298p)), decimals=2)
        v_rescale = exposure.rescale_intensity(v, in_range=(-bounds, bounds))

    colormap_terrain = cmap
    rgb = colormap_terrain(v_rescale)
    #remove last column - alpha value
    rgb = (rgb[:, :3] * (np.power(2,16)-1)).astype('uint16')    
    outFile = File(output_las_fn, mode='w', header=inFile.header)
    new_header = copy.copy(outFile.header)
    #setting some variables
    new_header.created_year = datetime.datetime.now().year
    new_header.created_day = datetime.datetime.now().timetuple().tm_yday
    new_header.x_max = pc_xyz[:,0].max()
    new_header.x_min = pc_xyz[:,0].min()
    new_header.y_max = pc_xyz[:,1].max()
    new_header.y_min = pc_xyz[:,1].min()
    new_header.z_max = pc_xyz[:,2].max()
    new_header.z_min = pc_xyz[:,2].min()
    new_header.point_records_count = pc_xyz.shape[0]
    new_header.point_return_count = 0
    outFile.header.count = v.shape[0]
    new_header.scale=inFile.header.scale
    new_header.offset=inFile.header.offset
    outFile.X = (pc_xyz[:,0]-inFile.header.offset[0])/inFile.header.scale[0]
    outFile.Y = (pc_xyz[:,1]-inFile.header.offset[1])/inFile.header.scale[1]
    outFile.Z = (pc_xyz[:,2]-inFile.header.offset[2])/inFile.header.scale[2]
    outFile.Red = rgb[:,0]
    outFile.Green = rgb[:,1]
    outFile.Blue = rgb[:,2]    
    outFile.close()    

def write_LAS_intensity(pc_xyz, v, output_las_fn, input_las_fn, rescale='none'):
    import datetime
    from laspy.file import File
    from skimage import exposure
    import copy
    
    inFile = File(input_las_fn, mode='r')

    #normalize input and generate colors for height using colormap
    #stretch to 10-90th percentile
    #v_1090p = np.percentile(v, [10, 90])
    #stretch to 2-98th percentile
    v_0298p = np.percentile(v, [2, 98])
    if rescale == 'none':
        v_rescale = exposure.rescale_intensity(v, in_range=(v_0298p[0], v_0298p[1]))
    elif rescale == 'median':
        bounds = np.round(np.median(np.abs(v_0298p)), decimals=2)
        v_rescale = exposure.rescale_intensity(v, in_range=(-bounds, bounds))

    v_rescale = v_rescale * (np.power(2,16)-1).astype('uint16')
    outFile = File(output_las_fn, mode='w', header=inFile.header)
    new_header = copy.copy(outFile.header)
    #setting some variables
    new_header.created_year = datetime.datetime.now().year
    new_header.created_day = datetime.datetime.now().timetuple().tm_yday
    new_header.x_max = pc_xyz[:,0].max()
    new_header.x_min = pc_xyz[:,0].min()
    new_header.y_max = pc_xyz[:,1].max()
    new_header.y_min = pc_xyz[:,1].min()
    new_header.z_max = pc_xyz[:,2].max()
    new_header.z_min = pc_xyz[:,2].min()
    new_header.point_records_count = pc_xyz.shape[0]
    new_header.point_return_count = 0
    outFile.header.count = v.shape[0]
    new_header.scale=inFile.header.scale
    new_header.offset=inFile.header.offset
    outFile.X = (pc_xyz[:,0]-inFile.header.offset[0])/inFile.header.scale[0]
    outFile.Y = (pc_xyz[:,1]-inFile.header.offset[1])/inFile.header.scale[1]
    outFile.Z = (pc_xyz[:,2]-inFile.header.offset[2])/inFile.header.scale[2]
    outFile.intensity = v_rescale
    outFile.close()

def pc_generate_pyKDTree(pc_xyz):
    try:
        from pykdtree.kdtree import KDTree as pyKDTree
    except ImportError:
        raise pc_generate_pyKDTree("pykdtree not installed.")
    pc_xyz_pyKDTree_tree = pyKDTree(pc_xyz)
    return pc_xyz_pyKDTree_tree
    
def pc_query_pyKDTree(pc_xyz_pyKDTree_tree, pc_xyz, k=10):
    pc_pyKDTree_distance, pc_pyKDTree_id = pc_xyz_pyKDTree_tree.query(pc_xyz, k=k)
    return pc_pyKDTree_distance, pc_pyKDTree_id

def pc_density_sphere(d, k=10):
    dens =  k / np.pi / d[:, -1]**2
    return dens

if __name__ == '__main__':     
    fname = 'UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm_c2cdist.las'
    print('Loading input file: %s... '%fname, end='', flush=True)
    print('reading', fname)
    f = laspy.file.File(fname)
    x = f.x
    y = f.y
    z = f.z
    f.close()
    pc_xyz = np.transpose((x, y, z))
    print('loaded %s points'%"{:,}".format(pc_xyz.shape[0]))
    #you can verify memory usage of a variable with:
    #from sys import getsizeof    
    #getsizeof(x)    

    pc_xyz_pyKDTree_tree = pc_generate_pyKDTree(pc_xyz)
    pc_pyKDTree_distance, pc_pyKDTree_id = pc_query_pyKDTree(pc_xyz_pyKDTree_tree, pc_xyz, k=10)
    pc_dens_sphere_k10 = pc_density_sphere(pc_pyKDTree_distance, k=10)
    pc_pyKDTree_distance = None
    pc_pyKDTree_id = None    
    DensityData = {'UTM-X': pc_xyz[:,0], 'UTM-Y': pc_xyz[:,1], 'UTM-Z': pc_xyz[:,2], 
                   'Dens_sphere_k10': pc_dens_sphere_k10}
    df_DensityData = pd.DataFrame(DensityData, columns= ['UTM-X', 'UTM-Y', 'UTM-Z', 'Dens_sphere_k10'])
    output_hdf_fn = 'UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm_c2cdist.hdf'
    df_DensityData.to_hdf(output_hdf_fn, 
                          key='df_DensityData', mode='w', complevel=7)
    DensityData = None
    # Write to LAS/LAZ file (writing to LAZ file not yet supported by laspy, using work around with laszip)
    output_las_fn = 'UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm_c2cdist_pykdtree_density_k10.las'
    if os.path.exists(output_las_fn) == False:
        print('\tWriting density_sphere_k10 to LAZ file: %s... '%os.path.basename(output_las_fn), end='', flush=True)    
        pts2write = pc_xyz
        mask = np.all(np.isnan(pts2write) | np.equal(pts2write, 0), axis=1)                
        pts2write = pts2write[~mask]
        #normalize input and generate colors using colormap
        v = df_DensityData['Dens_sphere_k10'].values
        v = v[~mask]
        mask = None
        write_LAS_intensity(pts2write, v, output_las_fn[:-3]+'las', fname)
        pts2write = None
        print('done.')

## Repeat for inspire2:
    fname = '/media/bodo/Windows/Golm-PCs/UAV_inspire2_1031cameras_highq_dense_pc_10cm_aligned2.laz'
    print('Loading input file: %s... '%fname, end='', flush=True)
    print('reading', fname)
    f = laspy.file.File(fname)
    x = f.x
    y = f.y
    z = f.z
    f.close()
    pc_xyz = np.transpose((x, y, z))
    print('loaded %s points'%"{:,}".format(pc_xyz.shape[0]))
    #you can verify memory usage of a variable with:
    #from sys import getsizeof    
    #getsizeof(x)    
    pc_xyz_pyKDTree_tree = pc_generate_pyKDTree(pc_xyz)
    pc_pyKDTree_distance, pc_pyKDTree_id = pc_query_pyKDTree(pc_xyz_pyKDTree_tree, pc_xyz, k=10)
    pc_dens_sphere_k10 = pc_density_sphere(pc_pyKDTree_distance, k=10)
    pc_pyKDTree_distance = None
    pc_pyKDTree_id = None    
    DensityData = {'UTM-X': pc_xyz[:,0], 'UTM-Y': pc_xyz[:,1], 'UTM-Z': pc_xyz[:,2], 
                   'Dens_sphere_k10': pc_dens_sphere_k10}
    df_DensityData = pd.DataFrame(DensityData, columns= ['UTM-X', 'UTM-Y', 'UTM-Z', 'Dens_sphere_k10'])
    output_hdf_fn = '_pykdtree_density_sphere.hdf'
    output_hdf_fn = fname.split('.')[:-1][0] + output_hdf_fn
    df_DensityData.to_hdf(output_hdf_fn, 
                          key='df_DensityData', mode='w', complevel=7)
    DensityData = None
    # Write to LAS/LAZ file (writing to LAZ file not yet supported by laspy, using work around with laszip)
    output_las_fn = '_pykdtree_density_sphere_k10.las'
    output_las_fn = fname.split('.')[:-1][0] + output_las_fn
    if os.path.exists(output_las_fn) == False:
        print('\tWriting density_sphere_k10 to LAZ file: %s... '%os.path.basename(output_las_fn), end='', flush=True)    
        pts2write = pc_xyz
        mask = np.all(np.isnan(pts2write) | np.equal(pts2write, 0), axis=1)                
        pts2write = pts2write[~mask]
        #normalize input and generate colors using colormap
        v = df_DensityData['Dens_sphere_k10'].values
        v = v[~mask]
        mask = None
        write_LAS(pts2write, v, output_las_fn[:-3]+'las', fname, cmap=cm.viridis)
        pts2write = None
        print('done.')

## Repeat for ALS dataset:
    fname = '/media/bodo/Windows/Golm-PCs/ALS_Golm_May06_2018_Milan_UTM33N_WGS84_6digit_cl_clip_v12.laz'
    print('Loading input file: %s... '%fname, end='', flush=True)
    print('reading', fname)
    f = laspy.file.File(fname)
    x = f.x
    y = f.y
    z = f.z
    f.close()
    pc_xyz = np.transpose((x, y, z))
    print('loaded %s points'%"{:,}".format(pc_xyz.shape[0]))
    #you can verify memory usage of a variable with:
    #from sys import getsizeof    
    #getsizeof(x)    

    pc_xyz_pyKDTree_tree = pc_generate_pyKDTree(pc_xyz)
    pc_pyKDTree_distance, pc_pyKDTree_id = pc_query_pyKDTree(pc_xyz_pyKDTree_tree, pc_xyz, k=10)
    pc_dens_sphere_k10 = pc_density_sphere(pc_pyKDTree_distance, k=10)
    pc_pyKDTree_distance = None
    pc_pyKDTree_id = None    
    DensityData = {'UTM-X': pc_xyz[:,0], 'UTM-Y': pc_xyz[:,1], 'UTM-Z': pc_xyz[:,2], 
                   'Dens_sphere_k10': pc_dens_sphere_k10}
    df_DensityData = pd.DataFrame(DensityData, columns= ['UTM-X', 'UTM-Y', 'UTM-Z', 'Dens_sphere_k10'])
    output_hdf_fn = '_pykdtree_density_sphere.hdf'
    output_hdf_fn = fname.split('.')[:-1][0] + output_hdf_fn
    df_DensityData.to_hdf(output_hdf_fn, 
                          key='df_DensityData', mode='w', complevel=7)
    DensityData = None
    # Write to LAS/LAZ file (writing to LAZ file not yet supported by laspy, using work around with laszip)
    output_las_fn = '_pykdtree_density_sphere_k10.las'
    output_las_fn = fname.split('.')[:-1][0] + output_las_fn
    if os.path.exists(output_las_fn) == False:
        print('\tWriting density_sphere_k10 to LAZ file: %s... '%os.path.basename(output_las_fn), end='', flush=True)    
        pts2write = pc_xyz
        mask = np.all(np.isnan(pts2write) | np.equal(pts2write, 0), axis=1)                
        pts2write = pts2write[~mask]
        #normalize input and generate colors using colormap
        v = df_DensityData['Dens_sphere_k10'].values
        v = v[~mask]
        mask = None
        write_LAS(pts2write, v, output_las_fn[:-3]+'las', fname, cmap=cm.viridis)
        pts2write = None
        print('done.')
