#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import argparse
import textwrap
import gc
import matplotlib.pyplot as plt
from os import path
from scipy.io import loadmat
from radpy.interpolate import batch_process


def make_parser():
    example = textwrap.dedent('''\
        Example:
          {} -ipmv -o composite brancomp/*.mat
        ''')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Composite postprocessing.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='input composite mat files')
    parser.add_argument('-i', '--interpolate', action='store_true',
                        help='interpolate output to 1 min resolution')
    parser.add_argument('-p', '--png', action='store_true',
                        help='store image output')
    parser.add_argument('-m', '--mat', action='store_true',
                        help='store mat output')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    parser.add_argument('-o', '--out-dir', type=str, default='.')
    parser.epilog = example.format(parser.prog)
    return parser


def main(mats, **kws):
    for matpath in mats:
        data = loadmat(matpath)
        name = path.splitext(path.split(matpath)[-1])[0]
        batch_process(name, data=data, **kws)
        gc.collect()


if __name__ == '__main__':
    plt.ioff()
    plt.close('all')
    parser = make_parser()
    args = parser.parse_args()
    main(args.files, write_mat=args.mat, write_png=args.png,
         interpolate=args.interpolate, resultsdir=args.out_dir,
         verbose=args.verbose)
    
