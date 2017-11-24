#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import argparse
import textwrap
from radpy import datafilter


def make_parser():
    example = textwrap.dedent('''\
        Example:
          {} -vwd grids/???/*/ncf_?????????_??????.nc
        ''')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Filter unnecessary gridded data files.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='a file to process')
    parser.add_argument('-d', '--delete', action='store_true',
                        help='delete filtered files')
    parser.add_argument('-w', '--write-lists', action='store_true',
                        help='write lists of good files')
    parser.add_argument('-o', '--out', type=str,
                        help='directory to write output, implies -w')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    parser.epilog = example.format(parser.prog)
    return parser


def main(*args, **kws):
    datafilter.apply_file_filter(*args, **kws)


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    main(args.files, verbose=args.verbose, write_lists=args.write_lists,
         write_path=args.out, remove_bad=args.delete)
