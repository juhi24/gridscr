# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

#import numpy as np
#import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import radcomp.visualization as vis
from matplotlib import gridspec
from os import path
from scipy.io import loadmat
from j24 import home
from radcomp.qpe.radar import RADARS

I_RADAR = dict(ker=0, kum=1, van=2, com=3)
NAMES = dict(ker='KER', kum='KUM', van='VAN', com='Composite')
RADAR = dict(ker=RADARS['KER'], kum=RADARS['KUM'], van=RADARS['VAN'])
RESULTSDIR = path.join(home(), 'results', 'radcomp', 'brandon')
PROJECTION = ccrs.Orthographic(central_longitude=25, central_latitude=60)


def datalist4radar(i_radar, data, param='kdp'):
    dat = data['{}_three_radars'.format(param)]
    n_timesteps = dat.shape()[3]
    return [dat[:, :, i_radar, i] for i in range(n_timesteps)]


def datalist4timestep(i_timestep, data, param='kdp'):
    if param=='r':
        sitestrs = ['ker', 'kum', 'van', 'c']
        return [data['rain_{}'.format(site)][:, :, i_timestep] for site in sitestrs]
    dat = data['{}_three_radars'.format(param)]
    n_radars = dat.shape[2]
    out = [dat[:, :, i, i_timestep] for i in range(n_radars)]
    datalist = out + [data['{}_composite'.format(param)][:, :, i_timestep]]
    return datalist


def plot_fun(fun, field, **kws):
    return fun(field, **kws)


def plot_r(r, **kws):
    return plot_fun(vis.plot_r, r, **kws)


def plot_kdp(kdp, **kws):
    return plot_fun(vis.plot_kdp, kdp, **kws)


def plot_dbz(dbz, **kws):
    return plot_fun(vis.plot_dbz, dbz, **kws)


def plotvars_core(gs, data, plotfun=vis.plot_r, plot_radars=True,
                  projection=PROJECTION, **kws):
    """plot to shape (2, 3) gridspec"""
    trans = ccrs.PlateCarree()
    axd = dict(ker=plt.subplot(gs[0, 0], projection=projection),
               kum=plt.subplot(gs[0, 1], projection=projection),
               van=plt.subplot(gs[1, 0], projection=projection),
               com=plt.subplot(gs[1, 1], projection=projection))
    for key in ['ker', 'kum']:
        axd[key].set_xticks([])
    for key in ['kum', 'com']:
        axd[key].set_yticks([])
    ax_cb = plt.subplot(gs[:, -1])
    for key in NAMES.keys():
        ax = axd[key]
        ax.set_ymargin(0)
        ax.set_xmargin(0)
        plotfun(data[I_RADAR[key]], ax=ax, cax=ax_cb, transform=trans, **kws)
        ax.set_title(NAMES[key])
        ax.coastlines(resolution='10m')
        if plot_radars:
            if key != 'com':
                RADAR[key].draw_marker(ax=ax, transform=trans)
            else:
                for radarkey in ['ker', 'kum', 'van']:
                    RADAR[radarkey].draw_marker(ax=ax, transform=trans)
    return axd


def plotvars(**kws):
    fig = plt.figure(figsize=(10, 9.5))
    gs = gridspec.GridSpec(2, 3, width_ratios=(15, 15, 1))
    gs.update(left=0.04, wspace=0.04, hspace=0.08, right=.92, top=0.95, bottom=0.05)
    axd = plotvars_core(gs, **kws)
    return fig, axd


if __name__ == '__main__':
    plt.ion()
    plt.close('all')
    fig_r, axd_r = plotvars(plotfun=plot_r, data=datalist4timestep(-1, param='r'))
    fig_kdp, axd_kdp = plotvars(plotfun=plot_kdp, data=datalist4timestep(-1, param='kdp'))
    fig_dbz, axd_dbz = plotvars(plotfun=plot_dbz, data=datalist4timestep(-1, param='dbz'))
    figs = dict(KDP=fig_kdp, ZH=fig_dbz)#, R=fig_r)
    for param in figs.keys():
        figfname = '{param}_{name}.png'.format(param=param, name=name)
        figs[param].savefig(path.join(RESULTSDIR, figfname))
