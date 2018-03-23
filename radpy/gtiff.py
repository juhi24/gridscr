# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Proj, transform
from os import path
from scipy.io import loadmat


if __name__ == '__main__':
    grid_origin_lat = 60.287500
    grid_origin_lon = 24.982076
    crs = rasterio.crs.CRS({"proj": "aeqd", "lat_0": grid_origin_lat, "lon_0": grid_origin_lon, "datum": "WGS84"})
    p1 = Proj(init='epsg:4326')
    #p2=Proj(init='epsg:3879')
    p2 = Proj(crs)
    xo, yo = transform(p1, p2, grid_origin_lon, grid_origin_lat)
    hdd = '/media/jussitii/04fafa8f-c3ca-48ee-ae7f-046cf576b1ee'
    mat = path.join(hdd, 'composite/20171003/mat/20171003_0231.mat')
    gmat = path.join(hdd, 'grid.mat')
    data = loadmat(mat)
    r = data['R'].astype(rasterio.float32).T
    tstr = data['time'][0]
    grid = loadmat(gmat)
    xs, ys = transform(p1, p2, grid['lon'], grid['lat'])
    trans = rasterio.transform.from_bounds(-50000, 50000,
                                   50000, -50000,
                                   width=r.shape[1], height=r.shape[0])
    with rasterio.open('/tmp/new1.tif', 'w', driver='GTiff', height=r.shape[0],
                   width=r.shape[1], count=1, dtype=r.dtype,
                   crs=crs, transform=trans) as dst:
        dst.write(r, 1)
