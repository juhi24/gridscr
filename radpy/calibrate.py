# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import radcomp.visualization as vis
from plotting import load, PROJECTION
from radcomp.qpe.radar import RADARS
import matplotlib.ticker as mticker

plt.ion()
plt.close('all')
name = 'out17'

data = load(name)

def dropna(x):
    return x[~np.isnan(x)]

def cdf(x, bins=100, **kws):
    data = dropna(x)
    size = data.size
    values, base = np.histogram(data, bins=bins, **kws)
    return base, np.cumsum(values)/size

def cartopy_xlabel(ax, x_lons, myproj, tick_fs=10):    
    #transform the corner points of my map to lat/lon
    xy_bounds = ax.get_extent()
    ll_lonlat = ccrs.Geodetic().transform_point(xy_bounds[0],xy_bounds[2], myproj)
    lr_lonlat = ccrs.Geodetic().transform_point(xy_bounds[1],xy_bounds[2], myproj)
    #take the median value as my fixed latitude for the x-axis
    l_lat_median = np.median([ll_lonlat[1],lr_lonlat[1]]) #use this lat for transform on lower x-axis
    x_lats_helper = np.ones_like(x_lons)*l_lat_median
    x_lons = np.asarray(x_lons)
    x_lats_helper = np.asarray(x_lats_helper)
    x_lons_xy = myproj.transform_points(ccrs.Geodetic(), x_lons,x_lats_helper)
    x_lons_xy = list(x_lons_xy[:,0]) #only lon pos in xy are of interest     
    x_lons = list(x_lons)
    x_lons_labels =[]
    for j in range(len(x_lons)):
        if x_lons[j]>0:
            ew=r'$^\circ$E'
        else:
            ew=r'$^\circ$W'
        x_lons_labels.append(str(x_lons[j])+ew)
    ax.set_xticks(x_lons_xy)
    ax.set_xticklabels(x_lons_labels,fontsize=tick_fs)

def cartopy_ylabel(ax, y_lats, myproj, tick_fs=10):        
    xy_bounds = ax.get_extent()
    ll_lonlat = ccrs.Geodetic().transform_point(xy_bounds[0],xy_bounds[2], myproj)
    ul_lonlat = ccrs.Geodetic().transform_point(xy_bounds[0],xy_bounds[3], myproj)
    l_lon_median = np.median([ll_lonlat[0],ul_lonlat[0]]) #use this lon for transform on left y-axis
    y_lons_helper = np.ones_like(y_lats)*l_lon_median
    y_lats = np.asarray(y_lats)    
    y_lats_xy = myproj.transform_points(ccrs.Geodetic(), y_lons_helper, y_lats)
    y_lats_xy = list(y_lats_xy[:,1]) #only lat pos in xy are of interest 
    y_lats = list(y_lats)
    y_lats_labels =[]
    for j in range(len(y_lats)):
        if y_lats[j]>0:
            ew=r'$^\circ$N'
        else:
            ew=r'$^\circ$S'
        y_lats_labels.append(str(y_lats[j])+ew)
    ax.set_yticks(y_lats_xy)
    ax.set_yticklabels(y_lats_labels,fontsize=tick_fs)

if __name__ == '__main__':
    trans = ccrs.PlateCarree()
    #box = (250, 360, 40, 150)
    box = (5, 90, 220, 315)
    lat = data['lat']
    lon = data['lon']
    kerz = data['dbz_ker']#-19.6+1.75
    vanz = data['dbz_van']
    diff = vanz-kerz
    mdiff = np.ma.masked_array(diff, mask=np.isnan(diff))
    #vanz[np.isnan(kerz)] = np.nan
    #kerz[np.isnan(vanz)] = np.nan
    selection = np.zeros(kerz.shape, dtype=bool)
    selection[box[0]:box[1], box[2]:box[3]] = True
    base_van, cd_van = cdf(vanz[selection])
    base_ker, cd_ker = cdf(kerz[selection])
    base_diff, cd_diff = cdf(diff[selection])
    fcd, axcd = plt.subplots()
    axcd.plot(base_van[:-1], cd_van, label='VAN')
    axcd.plot(base_ker[:-1], cd_ker, label='KER')
    axcd.plot(base_diff[:-1], cd_diff, label='VAN-KER')
    axcd.grid()
    axcd.set_ylim(bottom=0, top=1)
    axcd.set_xlabel('ZH, dBZ')
    axcd.set_ylabel('CDF')
    axcd.legend()
    irect = np.zeros(kerz.shape, dtype=bool)
    irect[box[0], box[2]:box[3]]=True
    irect[box[1], box[2]:box[3]]=True
    irect[box[0]:box[1], box[2]]=True
    irect[box[0]:box[1], box[3]]=True
    mirect = np.ma.masked_array(irect, mask=~irect)
    mapfig = plt.figure()
    ax = plt.subplot(projection=PROJECTION)
    vis.plot_base(mdiff, lon=lon, lat=lat, cmap='seismic',vmin=-10, vmax=10,
                  ax=ax, transform=trans, cblabel='$Z_{VAN}-Z_{KER}$, dBZ')
    #plt.colorbar();
    ax.pcolormesh(lon, lat, mirect, cmap='gray', transform=trans)
    ax.coastlines(resolution='10m')
    x_lons = [24.5, 25, 25.5] #want these longitudes as tick positions
    y_lats = [60, 60.2, 60.4, 60.6] #want these latitudes as tick positions
    tick_fs = 9
    #my workaround functions:
    cartopy_xlabel(ax,x_lons, PROJECTION, tick_fs)
    cartopy_ylabel(ax,y_lats, PROJECTION, tick_fs)
    bbox = dict(facecolor='white', pad=1.2)
    for radar in (RADARS['VAN'], RADARS['KER']):
        radar.draw_marker(ax=ax, withname=True, bbox=bbox, transform=trans)
    #for rid in ('van', 'ker', 'com'):
    #    axd_dbz[rid].pcolormesh(lon, lat, mirect, cmap='gray')

