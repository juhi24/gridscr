#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import argparse
import textwrap
from os import path
from multiprocessing import Pool, Manager
from functools import partial
from radpy.pyart_tools import sigmet2cfrad
from pyart import config


def make_parser():
    example = textwrap.dedent('''\
        Example:
          {} ???data/*/*.raw ???data/*/*/*.RAW*
        ''')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Convert raw Sigmet radar data to cfradial.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='a file to process')
    default_out = 'cf'
    parser.add_argument('-o', '--outdir', metavar='OUTPUT_DIR', type=str,
                        default=default_out,
                        help='output directory, default: {}'.format(default_out))
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    parser.epilog = example.format(parser.prog)
    return parser


def main(filepaths, **kws):
    p = Pool()
    m = Manager()
    dirlock = m.Lock()
    p.map(partial(sigmet2cfrad, dirlock=dirlock, **kws), filepaths)


if __name__ == '__main__':
    conf_path = path.join(path.dirname(path.realpath(__file__)), 'radpy', 'pyart_config.py')
    conf = config.load_config(conf_path)
    parser = make_parser()
    args = parser.parse_args()
    main(args.files, outdir=args.outdir, verbose=args.verbose)
