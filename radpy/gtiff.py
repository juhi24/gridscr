# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import rasterio
from pyproj import Proj, transform
from os import path
from scipy.io import loadmat


GRID_FILE = '/usr/local/share/radpy/grid.mat'


def grid_transform(shape, gridpath=GRID_FILE, p2=Proj(init='epsg:3879')):
    p1 = Proj(init='epsg:4326') # WGS 84
    grid = loadmat(gridpath)
    xs, ys = transform(p1, p2, grid['lon'], grid['lat'])
    return rasterio.transform.from_bounds(xs[200,0], ys[-1, 200],
                                          xs[200,-1], ys[0, 200],
                                          width=shape[1], height=shape[0])


def savetif(r, metadata, tifpath, **kws):
    trans = grid_transform(shape=r.shape, **kws)
    with rasterio.open(tifpath, 'w', driver='GTiff', height=r.shape[0],
                       width=r.shape[1], count=1, dtype=r.dtype,
                       crs='EPSG:3879', transform=trans) as dst:
        dst.write(r, 1)
        dst.update_tags(**metadata)


def mat2tif(matpath, tifpath, **kws):
    """Convert deprecated mat output to geotiff."""
    data = loadmat(matpath)
    r = data['R'].astype(rasterio.float32).T
    meta = {'TIFFTAG_DATETIME': data['time'][0]}
    savetif(r, meta, tifpath, **kws)


if __name__ == '__main__':
    hdd = '/media/jussitii/04fafa8f-c3ca-48ee-ae7f-046cf576b1ee'
    mat = path.join(hdd, 'composite/20171003/mat/20171003_0231.mat')
    gmat = path.join(hdd, 'grid.mat')
    mat2tif(mat, '/tmp/new.tif', gridpath=gmat)
