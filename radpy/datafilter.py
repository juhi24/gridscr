# coding: utf-8
import copy
import getpass
import pandas as pd
import netCDF4 as nc
from os import path, remove
from glob import glob
from j24 import eprint

basepath = path.join('/media', getpass.getuser(), '04fafa8f-c3ca-48ee-ae7f-046cf576b1ee')
GRIDPATH = path.join(basepath, 'grids')


def data_is_bad(ncdata):
    lvar = list(ncdata.variables)
    z = ncdata.variables['z0']
    not_ppi = False # TODO
    no_kdp = 'KDP' not in lvar # no KDP
    high_elev = z[0] > 1.5 # too high elevation angle
    low_elev = z[0] < 0.05 # too low elevation angle
    is_correct_van_elev = int(round(z[0]*10)) == 7
    van_wrong_elev = ncdata.title == 'VANTAA' and not is_correct_van_elev
    # KUM is missing required field
    weird_kum = 'kum' in ncdata.title and not ('UNKNOWN_ID_73' in lvar or 'UNKNOWN_ID_74' in lvar)
    extra_missing = 'range_km' not in lvar
    return no_kdp or high_elev or not_ppi or van_wrong_elev or low_elev or weird_kum or extra_missing


def filter_filepaths(filepaths_all, remove_bad=False, verbose=False):
    """skip or remove filepaths that trigger data_is_bad"""
    filepaths_good = copy.deepcopy(filepaths_all)
    for filepath in filepaths_all:
        with nc.Dataset(filepath, 'r') as ncdata:
            if data_is_bad(ncdata):
                filepaths_good.remove(filepath)
                if remove_bad:
                    remove(filepath)
                    if verbose:
                        eprint('rm ' + filepath)
                elif verbose:
                    eprint('filtered ' + filepath)
    return filepaths_good


def fpath(site, gridpath=GRIDPATH):
    return path.join(gridpath, '{}_goodfiles.csv'.format(site))


def apply_file_filter(filepaths, sites=['VAN', 'KER', 'KUM'],
                      write_lists=False, write_path=None, **kws):
    write_path = write_path or path.realpath(path.join(filepaths[0], '..', '..', '..'))
    filepaths.sort()
    # filtering takes a lot of time
    filepaths_good = filter_filepaths(filepaths, **kws)
    if write_lists or write_path:
        for site in sites:
            paths = []
            for k in filepaths_good:
                if '/{}/'.format(site) in k:
                    paths.append(path)
                    print(k)
            outpath = fpath(site, gridpath=write_path)
            spaths = pd.Series(paths)
            spaths.to_csv(path=outpath, index=False)


def load(**kws):
    out = dict(KUM=None, KER=None, VAN=None)
    for site in out:
        out[site] = pd.read_csv(fpath(site, **kws), header=None, names=['filepath'])
    return out
