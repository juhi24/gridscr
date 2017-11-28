# coding: utf-8
import copy
import getpass
import pandas as pd
import netCDF4 as nc
from os import path, remove
from j24 import eprint

basepath = path.join('/media', getpass.getuser(), '04fafa8f-c3ca-48ee-ae7f-046cf576b1ee')
GRIDPATH = path.join(basepath, 'grids')

try:
    FileNotFoundError
except NameError:
    class FileNotFoundError(IOError): pass

def data_is_bad(ncdata):
    """DEPRECATED. Check if gridded data is not good for rainrate composite."""
    lvar = list(ncdata.variables)
    bad_post = bad_postprocessing_result(lvar)
    z = ncdata.variables['z0']
    not_ppi = False # TODO
    high_elev = z[0] > 1.5 # too high elevation angle
    low_elev = z[0] < 0.05 # too low elevation angle
    is_correct_van_elev = int(round(z[0]*10)) == 7
    van_wrong_elev = ncdata.title == 'VANTAA' and not is_correct_van_elev
    # KUM is missing required field
    weird_kum = 'kum' in ncdata.title and not ('UNKNOWN_ID_73' in lvar or 'UNKNOWN_ID_74' in lvar)
    return high_elev or not_ppi or van_wrong_elev or low_elev or weird_kum or bad_post


def bad_postprocessing_result(lvar):
    no_kdp = 'KDP' not in lvar # no KDP
    extra_missing = 'range_km' not in lvar
    return no_kdp or extra_missing


def filter_filepaths(filepaths_all, remove_bad=False, verbose=False):
    """skip or remove filepaths that trigger bad_postprocessing_result"""
    filepaths_good = copy.deepcopy(filepaths_all)
    for filepath in filepaths_all:
        try:
            with nc.Dataset(filepath, 'r') as ncdata:
                if bad_postprocessing_result(list(ncdata.variables)):
                    filepaths_good.remove(filepath)
                    if remove_bad:
                        remove(filepath)
                        if verbose:
                            eprint('rm ' + filepath)
                    elif verbose:
                        eprint('filtered ' + filepath)
        except FileNotFoundError:
            eprint('Filtering unfound file {}.'.format(filepath))
            filepaths_good.remove(filepath)
    return filepaths_good


def fpath(site, gridpath=GRIDPATH):
    """file list path"""
    return path.join(gridpath, '{}_goodfiles.csv'.format(site))


def apply_file_filter(filepaths, sites=['VAN', 'KER', 'KUM'],
                      write_lists=False, write_path=None, **kws):
    """Filter filepaths and optionally write lists of good files."""
    write_path = write_path or path.realpath(path.join(filepaths[0], '..', '..', '..'))
    filepaths.sort()
    # filtering takes a lot of time
    filepaths_good = filter_filepaths(filepaths, **kws)
    if write_lists or write_path:
        for site in sites:
            paths = []
            for k in filepaths_good:
                if '/{}/'.format(site) in k:
                    paths.append(k)
                    print(k)
            outpath = fpath(site, gridpath=write_path)
            spaths = pd.Series(paths)
            spaths.to_csv(path=outpath, index=False)


def load(**kws):
    """Load file list."""
    out = dict(KUM=None, KER=None, VAN=None)
    for site in out:
        out[site] = pd.read_csv(fpath(site, **kws), header=None, names=['filepath'])
    return out
