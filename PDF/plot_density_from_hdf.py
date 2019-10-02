#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 08:18:53 2019

@author: bodo
"""

import pandas as pd
import numpy as np

hdf_fname = '/media/bodo/Windows/Golm-PCs/ALS_Golm_May06_2018_Milan_UTM33N_WGS84_6digit_cl_clip_v12_pykdtree_density_sphere.hdf'
ALS_sphere_density = pd.read_hdf(hdf_fname, mode='r', key='df_DensityData')

#Find mean density of dataset:
np.mean(ALS_sphere_density['Dens_sphere_k10'])
#pts/m^3 for k=10 neighbors

np.mean(ALS_sphere_density['Dens_sphere_k20'])
#pts/m^3 for k=20 neighbors

np.mean(ALS_sphere_density['Dens_sphere_k30'])
#pts/m^3 for k=30 neighbors


ax.cla()
ax = ALS_sphere_density['Dens_sphere_k20'].plot.hist(bins=100, alpha=0.5)
ax = ALS_sphere_density['Dens_sphere_k30'].plot.hist(bins=100, alpha=0.5)
ax.set_xlabel("Volumetric Density (pts/m3) for k=10", fontsize=18)
ax.set_ylabel("Frequency", fontsize=18)
ax.legend(["Dens_sphere_k20", "Dens_sphere_k30"])


#Repeat analysis on UAV data: inspire2
hdf_fname = '/media/bodo/Windows/Golm-PCs/UAV_inspire2_1031cameras_highq_dense_pc_10cm_aligned2_pykdtree_density_sphere.hdf'
UAV_inspire2_sphere_density = pd.read_hdf(hdf_fname, mode='r', key='df_DensityData')
UAV_inspire2_density_mean = np.mean(UAV_inspire2_sphere_density['Dens_sphere_k10'])
print('The spherical volumetric density (pts/m3) of the UAV inspire 2 dataset for k=10 neighbors: %3.2f'%UAV_inspire2_density_mean)


hdf_fname = '/media/bodo/Windows/Golm-PCs/UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm_df_Density_sphere_pyKDTree.hdf'
UAV_mavicpro2_sphere_density = pd.read_hdf(hdf_fname, mode='r', key='df_DensityData')
UAV_mavicpro2_density_mean = np.mean(UAV_mavicpro2_sphere_density['Dens_sphere_k10'])
print('The spherical volumetric density (pts/m3) of the UAV MavicPro 2 dataset for k=10 neighbors: %3.2f'%UAV_mavicpro2_density_mean)


ax.cla()
ax = ALS_sphere_density['Dens_sphere_k10'].plot.hist(bins=100, alpha=0.5)
ax = UAV_inspire2_sphere_density['Dens_sphere_k10'].plot.hist(bins=100, alpha=0.5)
ax = UAV_mavicpro2_sphere_density['Dens_sphere_k10'].plot.hist(bins=100, alpha=0.5)
ax.set_xlabel("Volumetric Density (pts/m3) for k=10", fontsize=18)
ax.set_ylabel("Frequency", fontsize=18)
ax.legend(["ALS, k=10", "Inspire 2, k=10", "Mavic Pro 2, k=10"])
