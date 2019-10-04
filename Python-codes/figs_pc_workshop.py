# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

base =

#%% Figure 1 - Stepped Curves 

x = np.linspace(0,1,100)
y = x**3

plt.close('all')
f, ax = plt.subplots(1)
ax.plot(x, y, 'k')
ax.set_xlim(0,1)
ax.set_ylim(0,1)

ax.plot((x[0], x[-1]), (y[0], y[-1]), 'r--')
ax.plot((x[50], x[-1]), (y[50], y[-1]), 'b--')
ax.plot((x[0], x[50]), (y[0], y[50]), 'b--')

f.savefig(base + 'fig1.png', dpi=300)
plt.close('all')

#%% Figure 2 -- Stepped Curves 2

x = np.linspace(0,1,100)
y = x**2

plt.close('all')
f, ax = plt.subplots(1)
ax.plot(x, y, 'k')
ax.set_xlim(0,1)
ax.set_ylim(0,1)

ax.plot((x[50], x[-1]), (y[50], y[-1]), 'b-')
ax.plot((x[0], x[50]), (y[0], y[50]), 'b-')

x = np.linspace(-0.1,1.1,100)
y = x**2

ax.plot(x, y, 'k--')
ax.set_xlim(-0.1,1.1)
ax.set_ylim(0,1.25)

ax.plot((x[50], x[-1]), (y[50], y[-1]), 'r--')
ax.plot((x[0], x[50]), (y[0], y[50]), 'r--')

f.savefig(base + 'fig2.png', dpi=300)
plt.close('all')

#%% Figure 3 - Simple Gaussian Hill

def make_hill(n):
    # sym grid limits for area 10
    r0 = np.sqrt(10) / 2
    xmin, xmax = -r0, r0
    ymin, ymax = -r0, r0
    
    # cell boundaries
    xb = np.linspace(xmin, xmax, n+1)
    yb = np.linspace(ymin, ymax, n+1)
    #xx, yy = np.meshgrid(xb, yb)
    spacing = abs(xb[1]-xb[0])
    
    # cell center
    x = xb[:-1] + 0.5 * abs(xb[1]-xb[0])
    y = yb[:-1] + 0.5 * abs(yb[1]-yb[0])
    
    x, y = np.meshgrid(x, y)
    z = np.exp(-x*x-y*y)
    
    return x, y, z, spacing

x, y, z, spacing = make_hill(1001)
mask = np.where(z < 0.1)
z[mask] = np.nan

plt.close('all')
f, ax = plt.subplots(1)

cb = ax.imshow(z, vmin=0, vmax=1)
cb = plt.colorbar(cb, ax=ax)
cb.ax.tick_params(labelsize=16)
cb.set_label('Elevation', fontsize=18)
ax.set_xticks([])
ax.set_yticks([])

f.savefig(base + 'fig3.png', dpi=300)
plt.close('all')

#%% Simple Slope and Aspect Images

def slope_hill(x, y):
    mag = 2 * np.sqrt(x*x+y*y) * np.exp(-x*x-y*y)
    return np.arctan(mag) * 180 / np.pi

def aspects_hill(x, y):
    return np.arctan2(y, -1*x) * 180 / np.pi + 180

x, y, z, spacing = make_hill(1001)
mask = np.where(z < 0.1)
z[mask] = np.nan
slp = slope_hill(x, y)
asp = aspects_hill(x, y)
slp[mask] = np.nan
asp[mask] = np.nan

f, (ax, ax2) = plt.subplots(1,2)

cb = ax.imshow(slp, vmin=0, vmax=40, cmap=plt.cm.RdBu)
cb = plt.colorbar(cb, ax=ax)
cb.ax.tick_params(labelsize=12)
cb.set_label('Slope', fontsize=14)
ax.set_xticks([])
ax.set_yticks([])

cb = ax2.imshow(asp, vmin=0, vmax=360, cmap=plt.cm.inferno)
cb = plt.colorbar(cb, ax=ax2)
cb.ax.tick_params(labelsize=12)
cb.set_label('Aspect', fontsize=14)
ax2.set_xticks([])
ax2.set_yticks([])

#%% Figure 4 - Slope and Aspect Difference from Perfect Surfaces

from mpl_toolkits.axes_grid1 import make_axes_locatable

def colorbar(mappable):
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    return fig.colorbar(mappable, cax=cax, extend='both')

def aspects_np(z, spacing):
    y, x = np.gradient(z, spacing)
    return np.arctan2(-1*y, x) * 180 / np.pi + 180

def slopes_np(z, spacing):
    y, x = np.gradient(z, spacing)
    mag = np.sqrt(x*x + y*y)
    return np.arctan(mag) * 180 / np.pi

x, y, z, spacing = make_hill(1001)
mask = np.where(z < 0.1)
z[mask] = np.nan
slp = slope_hill(x, y)
asp = aspects_hill(x, y)
slp[mask] = np.nan
asp[mask] = np.nan

slp_np, asp_np = slopes_np(z, spacing), aspects_np(z, spacing)
slp_dif = slp_np - slp
asp_dif = asp_np - asp

plt.close('all')
f, (ax, ax2) = plt.subplots(1,2)

vmin, vmax = np.nanpercentile(slp_dif, [5, 95])
cb = ax.imshow(slp_dif, vmin=vmin, vmax=vmax)            
cb = colorbar(cb)
cb.formatter.set_powerlimits((-1, 4))
cb.update_ticks()
cb.set_label('Slope Difference (degree)', fontsize=18)
cb.ax.tick_params(labelsize=16)
cb.ax.yaxis.offsetText.set_fontsize(16)
ax.set_xticks([])
ax.set_yticks([])

vmin, vmax = np.nanpercentile(asp_dif, [5, 95])
cb = ax2.imshow(asp_dif, vmin=vmin, vmax=vmax, cmap=plt.cm.seismic)   
cb = colorbar(cb)
cb.formatter.set_powerlimits((-1, 4))
cb.update_ticks()
cb.set_label('Aspect Difference (degree)', fontsize=18)
cb.ax.tick_params(labelsize=16)
cb.ax.yaxis.offsetText.set_fontsize(16)
ax2.set_xticks([])
ax2.set_yticks([])

#%% Figure 5 - Thinly Sliced Curve

x = np.linspace(0,1,100)
y = x**3

plt.close('all')
f, ax = plt.subplots(1)
ax.plot(x, y, 'k')
ax.set_xlim(0,1)
ax.set_ylim(0,1)

l = np.linspace(0, 100, 5)
for i, val in enumerate(l[1:]):
    v0 = int(l[i])
    val = int(val)
    ax.plot((x[v0], x[val-1]), (y[v0], y[val-1]), 'r--')

f.savefig(base + 'fig6.png', dpi=300)
plt.close('all')

#%% Function Definitions - Truncation and Propagated Errors

def trunc_err_slope(z, d):
    n = z.shape[0]
    dy, dx = np.gradient(z, d)
    _, ddx = np.gradient(dx, d)
    ddy, _ = np.gradient(dy, d)
    _, dddx = np.gradient(ddx, d)
    dddy, _ = np.gradient(ddy, d)
    del ddx, ddy
    ex = d * d * dddx / 6.
    ey = d * d * dddy / 6.
    del dddx, dddy
    g2 = dx*dx+dy*dy
    sg = np.arctan(np.sqrt((dx+ex)**2+(dy+ey)**2))
    sg -= np.arctan(np.sqrt((dx-ex)**2+(dy-ey)**2))
    return np.sign(sg)*np.sqrt((dx*dx*ex*ex+dy*dy*ey*ey+2*dx*dy*ex*ey)/g2/(1+g2)/(1+g2))*180/np.pi

def trunc_err_aspect(z, d):
    n = z.shape[0]
    dy, dx = np.gradient(z, d)
    _, ddx = np.gradient(dx, d)
    ddy, _ = np.gradient(dy, d)
    _, dddx = np.gradient(ddx, d)
    dddy, _ = np.gradient(ddy, d)
    del ddx, ddy
    ex = d * d * dddx / 6.
    ey = d * d * dddy / 6.
    del dddx, dddy
    g2 = dx*dx+dy*dy
    u2 = np.cos(np.arctan2(dy, dx))**4
    sg = np.arctan2(dy+ey, dx+ex) - np.arctan2(dy-ey, dx-ex)
    return np.sign(sg)*np.sqrt(u2*(ex*ex*dy*dy/dx/dx+ey*ey-2*dy/dx*ex*ey)/dx/dx)*180/np.pi

def peu_aspect_field(z, d, std):
    dy, dx = np.gradient(z, d)
    v = dy / dx
    u = np.cos(np.arctan2(dy, dx))
    u *= u
    u *= 90. / np.pi
    u /= d * np.abs(dx)
    n = std.shape[0]
    m = std.shape[1]
    ex1 = np.hstack((std[:,1:], np.zeros(n)[:, None]))
    ex2 = np.hstack((np.zeros(n)[:, None], std[:,:-1]))
    ey1 = np.vstack((std[1:,:], np.zeros(m)))
    ey2 = np.vstack((np.zeros(m), std[:-1,:]))
    u *= np.sqrt(v*v*(ex1*ex1+ex2*ex2)+ey1*ey1+ey2*ey2)
    return u

def peu_slope_field(z, d, std):
    dy, dx = np.gradient(z, d)
    v = np.sqrt(dx*dx + dy*dy)
    u = 90. / np.pi / d
    u /= v * (1 + v*v)
    n = std.shape[0]
    m = std.shape[1]
    ex1 = np.hstack((std[:,1:], np.zeros(n)[:, None]))
    ex2 = np.hstack((np.zeros(n)[:, None], std[:,:-1]))
    ey1 = np.vstack((std[1:,:], np.zeros(m)))
    ey2 = np.vstack((np.zeros(m), std[:-1,:]))
    u *= np.sqrt(dx*dx*(ex1*ex1+ex2*ex2)+dy*dy*(ey1*ey1+ey2*ey2))
    return u

#%% Function Definition - Quality Ratio
    
def QR(z, spacing, std, mask):
    '''
    Function that takes an elevation, grid spacing, elevation std, and a mask
    to return the Quality Ratio for both slope and aspect calculations
    '''
    trunc_slp = trunc_err_slope(z, spacing) 
    trunc_asp = trunc_err_aspect(z, spacing) / 4. 
    trunc_slp[mask] = np.nan
    trunc_asp[mask] = np.nan
    peu_slp = peu_slope_field(z, spacing, std) 
    peu_asp = peu_aspect_field(z, spacing, std) / 4.
    peu_slp[mask] = np.nan
    peu_asp[mask] = np.nan
    
    QRslp = (1 / (1 + np.abs(trunc_slp))) * (1 / (1 + np.abs(peu_slp)))
    QRasp = (1 / (1 + np.abs(trunc_asp))) * (1 / (1 + np.abs(peu_asp)))
    QRslp[mask] = np.nan
    QRasp[mask] = np.nan
    
    return QRslp, QRasp

#%% Figure 8 - Slope and Aspect Quality Ratios for Pozo Catchment 
    
import gdalnumeric
spacing = 10
dem = base + 'example/DEM/Pozo_UTM11_NAD83_g_' + str(spacing) + 'm.tif'
uncertainty = base + 'example/STD/Pozo_UTM11_NAD83_g_' + str(spacing) + 'm_std.tif'

#Load the data as arrays
elev = gdalnumeric.LoadFile(dem).astype(float)
std = gdalnumeric.LoadFile(uncertainty).astype(float)

#Mask out water areas
mask = np.where(elev < 0)
elev[mask] = np.nan
std[mask] = np.nan

#Calculate the Quality Ratios
QRslp, QRasp = QR(elev, i, std, mask)
QRslp[mask] = np.nan
QRasp[mask] = np.nan
    
plt.close('all')
f, (ax, ax2) = plt.subplots(1,2)

vmin, vmax = np.nanpercentile(QRslp, [5, 95])
cb = ax.imshow(QRslp, vmin=vmin, vmax=vmax)            
cb = colorbar(cb)
cb.formatter.set_powerlimits((-1, 4))
cb.update_ticks()
cb.set_label('Slope QR', fontsize=18)
cb.ax.tick_params(labelsize=16)
cb.ax.yaxis.offsetText.set_fontsize(16)
ax.set_xticks([])
ax.set_yticks([])

vmin, vmax = np.nanpercentile(QRasp, [5, 95])
cb = ax2.imshow(QRasp, vmin=vmin, vmax=vmax, cmap=plt.cm.seismic)   
cb = colorbar(cb)
cb.formatter.set_powerlimits((-1, 4))
cb.update_ticks()
cb.set_label('Aspect QR', fontsize=18)
cb.ax.tick_params(labelsize=16)
cb.ax.yaxis.offsetText.set_fontsize(16)
ax2.set_xticks([])
ax2.set_yticks([])


#%% Figure 9 - Slope and Aspect Quality Ratios vs Grid Spacing

spacings = range(2, 31)[::-1]
qr_s, qr_a = [], []
for i in spacings:
    dem = base_dir + 'example/DEM/Pozo_UTM11_NAD83_g_' + str(i) + 'm.tif'
    uncertainty = base_dir + 'example/STD/Pozo_UTM11_NAD83_g_' + str(i) + 'm_std.tif'
    
    #Load the data as arrays
    elev = gdalnumeric.LoadFile(dem).astype(float)
    std = gdalnumeric.LoadFile(uncertainty).astype(float)
    
    #Mask out water areas
    mask = np.where(elev < 0)
    elev[mask] = np.nan
    std[mask] = np.nan
    
    #Calculate the Quality Ratios
    QRslp, QRasp = QR(elev, i, std, mask)
    QRslp[mask] = np.nan
    QRasp[mask] = np.nan
    
    #Append the QR mean values to a list
    qr_s.append(np.nanmean(QRslp))
    qr_a.append(np.nanmean(QRasp))
    print(i)
    
#Plot the QR curves    
plt.close('all')
f, (ax, ax2) = plt.subplots(2)
ax.plot(spacings, qr_s, 'k-')
ax2.plot(spacings, qr_a, 'k-')
ax2.set_xlabel('Grid Resolution (m)', fontsize=16)
ax.set_ylabel('QR - Slope', fontsize=16)
ax2.set_ylabel('QR - Aspect', fontsize=16)
ax.set_xlim(0, 30)
ax2.set_xlim(0, 30)

#Get the max
qr_s, qr_a = np.array(qr_s), np.array(qr_a)
ideal_space_slp = spacings[np.where(qr_s == np.nanmax(qr_s))[0][0]]
ideal_space_asp = spacings[np.where(qr_a == np.nanmax(qr_a))[0][0]]

#Add the max to the plot
ym, ya = ax.get_ylim()
ax.plot((ideal_space_slp, ideal_space_slp), (ym, ya), 'r--')
ax.text(ideal_space_slp, (ym + ya)/2, str(ideal_space_slp) + 'm', va='top', rotation='vertical', fontsize=16, color='r')
ax.set_ylim(ym, ya)

ym, ya = ax2.get_ylim()
ax2.plot((ideal_space_asp, ideal_space_asp), (ym, ya), 'r--')
ax2.text(ideal_space_asp, (ym + ya)/2, str(ideal_space_slp) + 'm', va='top', rotation='vertical', fontsize=16, color='r')
ax2.set_ylim(ym, ya)

plt.tight_layout()
plt.show()
f.savefig(base + 'optimal_res.png', dpi=300)
    



