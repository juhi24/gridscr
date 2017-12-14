#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import argparse
import textwrap
from radpy import kdp
from multiprocessing import Pool
from functools import partial


def make_parser():
    example = textwrap.dedent('''\
        Example:
          {} cf/*/cfrad.*kum-rvp9-radar_PPI_SHORT*.nc
        ''')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Calculate missing KDP from PHIDP.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='a file to process')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force kdp recalculation')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    parser.epilog = example.format(parser.prog)
    return parser


def main(filepaths, **kws):
    p = Pool()
    p.map(partial(kdp.kdp_recalc_if_missing, **kws), filepaths)


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    main(args.files, verbose=args.verbose, force_recalc=args.force)
