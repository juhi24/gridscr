# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import datetime
from os import path
from pyart import io
from j24 import ensure_dir


def radar_start_datetime(radar):
    """task start datetime of a radar object"""
    time = io.mdv_grid._time_dic_to_datetime(radar.time)
    delta = datetime.timedelta(seconds=radar.time['data'][0])
    return time - delta


def cfrad_filename(radar, task_key='sigmet_task_name'):
    """Generate cfrad filename for radar object based on metadata."""
    time = radar_start_datetime(radar)
    timestr = time.strftime('%Y%m%d_%H%M%S')
    instrument = radar.metadata['instrument_name']
    task = radar.metadata[task_key].rstrip()
    naming = 'cfrad.{timestr}_{instrument}_{task}.nc'
    name = naming.format(timestr=timestr, instrument=instrument, task=task)
    return name


def sigmet2cfrad(filepath, outdir='cf', verbose=False):
    """Convert Sigmet raw radar data to cfradial format"""
    radar = io.read_sigmet(filepath)
    time = radar_start_datetime(radar)
    subdir = ensure_dir(path.join(outdir, time.strftime('%Y%m%d')))
    out_filepath =  path.join(subdir, cfrad_filename(radar))
    if verbose:
        print(out_filepath)
    io.write_cfradial(out_filepath, radar)

