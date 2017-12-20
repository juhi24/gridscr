# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import datetime
from os import path, remove
from pyart import io, config
from j24.path import ensure_dir, filename_friendly
from j24 import eprint


def radar_start_datetime(radar):
    """task start datetime of a radar object"""
    time = io.mdv_grid._time_dic_to_datetime(radar.time)
    delta = datetime.timedelta(seconds=radar.time['data'][0])
    return time - delta


def instrument_name(radar):
    """radar name in filename friendly format"""
    return filename_friendly(radar.metadata['instrument_name'])


def task_name(radar, task_key='sigmet_task_name'):
    """radar task name in filename friendly format"""
    return filename_friendly(radar.metadata[task_key])


def radar_info(radar):
    """Print basic info of a radar object."""
    print('instrument: {}'.format(instrument_name(radar)))
    print('task: {}'.format(task_name(radar)))
    print('elevation: {}'.format(radar.elevation['data'].mean()))
    print('fields: {}'.format(list(radar.fields)))


def cfrad_filename(radar, **kws):
    """Generate cfrad filename for radar object based on metadata."""
    time = radar_start_datetime(radar)
    timestr = time.strftime('%Y%m%d_%H%M%S')
    instrument = instrument_name(radar)
    task = task_name(radar)
    naming = 'cfrad.{timestr}_{instrument}_{task}.nc'
    name = naming.format(timestr=timestr, instrument=instrument, task=task)
    return name


def sigmet2cfrad(filepath, outdir='cf', dirlock=None, verbose=False, filter_raw=False):
    """Convert Sigmet raw radar data to cfradial format"""
    radar = io.read_sigmet(filepath)
    if is_bad(radar):
        if filter_raw:
            if verbose:
                eprint('rm {}'.format(filepath))
            remove(filepath)
        return
    time = radar_start_datetime(radar)
    if dirlock:
        dirlock.acquire()
    subdir = ensure_dir(path.join(outdir, time.strftime('%Y%m%d')))
    if dirlock:
        dirlock.release()
    out_filepath = path.join(subdir, cfrad_filename(radar))
    if verbose:
        print(out_filepath)
    io.write_cfradial(out_filepath, radar)


def is_bad(radar):
    """Check if pyart data is useless for rainrate composite."""
    instrument = radar.metadata['instrument_name']
    if 'VANTAA' in instrument:
        bad_instr = is_bad_van(radar)
    elif 'Kerava' in instrument:
        bad_instr = is_bad_ker(radar)
    elif 'Kumpula' in instrument:
        bad_instr = is_bad_kum(radar)
    bad_common = is_bad_common(radar)
    return bad_instr or bad_common


def is_bad_common(radar):
    """common rejection conditions for all radars"""
    no_dualpol = 'PHIDP' not in radar.fields
    not_ppi = radar.sweep_mode['data'][0] != 'azimuth_surveillance'
    elevation = radar.get_elevation(0).mean()
    high_elev = elevation > 1.5
    low_elev = elevation < 0.05
    return no_dualpol or not_ppi or high_elev or low_elev


def is_bad_van(radar, **kws):
    """Vantaa radar data rejection conditions"""
    task = task_name(radar, **kws)
    wrong_task = ('PPI' not in task) or ('_B' not in task)
    no_kdp = 'KDP' not in radar.fields
    return wrong_task or no_kdp


def is_bad_ker(radar):
    """Kerava radar data rejection conditions"""
    return False


def is_bad_kum(radar, **kws):
    """Kumpula radar data rejection conditions"""
    task = task_name(radar, **kws)
    instrument = instrument_name(radar)
    #wrong_task = ('APHID' in task) or ('ADS' in task)
    wrong_task = 'PPI_SHORT' not in task
    wrong_radar = 'Radar_2' in instrument
    return wrong_task or wrong_radar
