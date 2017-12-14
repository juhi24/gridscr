#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type


import argparse
import matplotlib.pyplot as plt
import pyart


def make_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Plot radar file.')
    parser.add_argument('file', metavar='FILE', type=str,
                        help='a file to plot')
    parser.add_argument('-f', '--field', type=str,
                        help='radar variable to plot, default: DBZ')
    return parser


def plot_file(filepath, field='DBZ'):
    radar = pyart.io.read(filepath)
    display = pyart.graph.RadarDisplay(radar)
    fig, ax = plt.subplots()
    display.plot(field)
    display.plot_cross_hair(5)
    ax.set_ylim(-50, 50)
    ax.set_xlim(-50, 50)
    plt.show()


def main(*args, **kws):
    plot_file(*args, **kws)


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    main(args.file, field=args.field)
