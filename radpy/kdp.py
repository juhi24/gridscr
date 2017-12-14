# coding: utf-8
"""
Calculate missing kdp from phidp for KUM
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import numpy as np
import matplotlib.pyplot as plt
import pyart
from j24 import eprint


def kdp_recalc_if_missing(fpath, verbose=True, force_recalc=False):
    radar = pyart.io.read_cfradial(fpath)
    try:
        kdp, phif, phir = pyart.retrieve.kdp_maesaka(radar, psidp_field='PHIDP')
    except IndexError:
        eprint('Error. Skipping {}.'.format(fpath))
        return
    if verbose:
        print(fpath)
    kdp_old = radar.get_field(0, 'KDP')
    # if none of kdp values make sense
    if not (abs(kdp_old < 1)).any() or force_recalc:
        mask_phi = radar.get_field(0, 'PHIDP').mask
        mask_kdp = ~kdp_old.mask + mask_phi  # inverted kdp mask
        kdp['data'] = np.ma.masked_array(kdp['data'], mask=mask_kdp,
                                         fill_value=kdp_old.fill_value)
        radar.add_field('KDP', kdp, replace_existing=True)
        pyart.io.write_cfradial(fpath, radar)  # overwrite changes
        if verbose:
            eprint('KDP recalculated. File rewritten.')
    elif verbose:
        eprint('KDP already present. File left untouched.')


def plot_dp(radar):
    disp_kdp = pyart.graph.RadarDisplay(radar)
    disp_phidp = pyart.graph.RadarDisplay(radar)
    fig_kdp = plt.figure()
    disp_kdp.plot_ppi('KDP', vmin=0, vmax=0.5)
    fig_phidp = plt.figure()
    disp_phidp.plot_ppi('PHIDP')
    return fig_kdp, fig_phidp

