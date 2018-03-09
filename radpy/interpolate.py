# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import itertools
import datetime
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib import gridspec
from os import path
from scipy.io import savemat
from radcomp.qpe import interpolation
from j24 import ensure_join, eprint
from .plotting import (plotvars_core, plot_r, plot_kdp, plot_dbz,
                      datalist4timestep, PROJECTION)


def round_datetime(dt, round_to_s=60):
   """Round a datetime to any time laps in seconds."""
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+round_to_s/2) // round_to_s * round_to_s
   return dt + datetime.timedelta(0, rounding-seconds, -dt.microsecond)


def plot_rainrate(r, subplot_spec, projection=PROJECTION, **kws):
    gs = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=subplot_spec,
                                          width_ratios=(35, 1),
                                          hspace=0.01, wspace=0.02)
    ax = plt.subplot(gs[0, 0], projection=projection)
    ax.set_ymargin(0)
    ax.set_xmargin(0)
    ax_cb = plt.subplot(gs[:, -1])
    plot_r(r, ax=ax, cax=ax_cb, **kws)
    return ax


def plotvars(subplot_spec, width_ratios=(15, 15, 1), data=None, **kws):
    gs = gridspec.GridSpecFromSubplotSpec(2, 3, subplot_spec=subplot_spec,
                                            width_ratios=width_ratios,
                                            hspace=0.1, wspace=0.02)
    axd = plotvars_core(gs, data=data, **kws)
    return axd


def plot_frame(r, i_timestep, tim, data=None):
    fig = plt.figure(figsize=(16, 15))
    gs = gridspec.GridSpec(2, 2, width_ratios=(1, 1), height_ratios=(1, 1))
    gs.update(left=0.02, right=.95, wspace=0.15, hspace=0.05,
              top=0.97, bottom=0.01)
    latlon = dict(lat=data['lat'], lon=data['lon'])
    axd_r = plotvars(gs[0, 0], plotfun=plot_r,
                     data=datalist4timestep(i_timestep, param='r', data=data), **latlon)
    axd_dbz = plotvars(gs[0, 1], plotfun=plot_dbz,
                       data=datalist4timestep(i_timestep, param='dbz', data=data), **latlon)
    axd_kdp = plotvars(gs[1, 0], plotfun=plot_kdp,
                       data=datalist4timestep(i_timestep, param='kdp', data=data), **latlon)
    ax = plot_rainrate(r, gs[1, 1], transform=ccrs.PlateCarree())
    ax.coastlines(resolution='10m')
    tstr = tim.strftime('%Y-%m-%d %H:%M')
    ax.set_title(tstr)
    return fig, dict(r=axd_r, zh=axd_dbz, kdp=axd_kdp)


def batch_process(name, data=None, write_mat=True, write_png=True,
                  resultsdir=None, interpolate=True, verbose=False):
    rc = data['rain_c']
    tstr = data['tim']
    tparser = lambda ts: datetime.datetime.strptime(ts[0][0], '%Y%m%d_%H%M%S')
    t = map(tparser, tstr)
    tr = map(round_datetime, t)
    n_timesteps = rc.shape[2]
    rs = [rc[:,:,i] for i in range(n_timesteps)]
    i = 0
    for j, (r0, r1, t0, t1) in enumerate(itertools.izip(rs, rs[1:], tr, tr[1:])):
        if interpolate:
            dt = t1 - t0
            dt_minutes = int(dt.total_seconds()/60)
            if dt_minutes > 5:
                eprint('Long interpolation period of {} minutes.'.format(dt_minutes))
            ri = interpolation.interp(r0, r1, n=dt_minutes-1)
            ra = [r0] + ri
        else:
            ra = [r0]
        for extra_minutes, r in enumerate(ra):
            i += 1
            tim = t0 + datetime.timedelta(minutes=extra_minutes)
            if verbose:
                print(str(tim))
            basename = tim.strftime('%Y%m%d_%H%M')
            if write_png:
                fig, axdd = plot_frame(r, j, tim, data=data)
                framedir = ensure_join(resultsdir, name, 'png')
                framepath = path.join(framedir, basename + '.png')
                fig.savefig(framepath)
                plt.close(fig)
            if write_mat:
                matdir = ensure_join(resultsdir, name, 'mat')
                mat_out_fpath = path.join(matdir, basename + '.mat')
                mdict = dict(time=np.array(str(tim)), R=r)
                savemat(mat_out_fpath, mdict, do_compression=True)

