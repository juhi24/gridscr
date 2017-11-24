# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import datetime
from os import path
from pyart import io, config
from j24.path import ensure_dir, filename_friendly


conf_path = path.join(path.dirname(path.realpath(__file__)), 'radpy', 'pyart_config.py')
conf = config.load_config(conf_path)


def radar_start_datetime(radar):
    """task start datetime of a radar object"""
    time = io.mdv_grid._time_dic_to_datetime(radar.time)
    delta = datetime.timedelta(seconds=radar.time['data'][0])
    return time - delta


def cfrad_filename(radar, task_key='sigmet_task_name'):
    """Generate cfrad filename for radar object based on metadata."""
    time = radar_start_datetime(radar)
    timestr = time.strftime('%Y%m%d_%H%M%S')
    instrument = filename_friendly(radar.metadata['instrument_name']).decode('utf-8')
    task = filename_friendly(radar.metadata[task_key]).decode('utf-8')
    naming = 'cfrad.{timestr}_{instrument}_{task}.nc'
    name = naming.format(timestr=timestr, instrument=instrument, task=task)
    return name


def sigmet2cfrad(filepath, outdir='cf', dirlock=None, verbose=False):
    """Convert Sigmet raw radar data to cfradial format"""
    radar = io.read_sigmet(filepath)
    time = radar_start_datetime(radar)
    if dirlock:
        dirlock.acquire()
    subdir = ensure_dir(path.join(outdir, time.strftime('%Y%m%d')))
    if dirlock:
        dirlock.release()
    out_filepath =  path.join(subdir, cfrad_filename(radar))
    if verbose:
        print(out_filepath)
    io.write_cfradial(out_filepath, radar)


def is_bad(radar):
    """Check if pyart data is useless for rainrate composite."""
    instrument = radar.metadata['instrument_name']
    if instrument == 'VANTAA':
        bad_instr = is_bad_van(radar)
    elif 'Kerava' in instrument:
        bad_instr = is_bad_ker(radar)
    elif 'Kumpula' in instrument:
        bad_instr = is_bad_kum(radar)
    return bad_instr


def is_bad_van(radar, task_key='sigmet_task_name'):
    task = radar.metadata[task_key]
    return ('PPI' not in task) or ('_B' not in task)


def is_bad_ker(radar):
    return False


def is_bad_kum(radar):
    return False
