# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import rasterio
import cartopy.crs as ccrs
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Proj, transform
from os import path
from scipy.io import loadmat


if __name__ == '__main__':
    p1=Proj(init='epsg:4326')
    p2=Proj(init='epsg:3879')
    grid_origin_lat = 60.287500
    grid_origin_lon = 24.982076
    crs=rasterio.crs.CRS({"proj": "aeqd", "lat_0": grid_origin_lat, "lon_0": grid_origin_lon, "datum": "WGS84"})
    xo, yo = transform(p1, p2, grid_origin_lon, grid_origin_lat)
    proj = ccrs.Orthographic(central_longitude=25, central_latitude=60)
    hdd = '/media/jussitii/04fafa8f-c3ca-48ee-ae7f-046cf576b1ee'
    mat = path.join(hdd, 'composite/20171003/mat/20171003_0231.mat')
    gmat = path.join(hdd, 'grid.mat')
    data = loadmat(mat)
    r = data['R'].astype(rasterio.float32).T
    tstr = data['time'][0]
    grid = loadmat(gmat)
    xs, ys = transform(p1, p2, grid['lon'], grid['lat'])
    trans = rasterio.transform.from_bounds(xs[201,0], ys[-1, 201],
                                   xs[201,-1], ys[0, 201],
                                   width=r.shape[1], height=r.shape[0])
    with rasterio.open('/tmp/new.tif', 'w', driver='GTiff', height=r.shape[0],
                   width=r.shape[1], count=1, dtype=r.dtype,
                   crs='EPSG:3879', transform=trans) as dst:
        dst.write(r, 1)
