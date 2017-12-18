#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type


import argparse
import matplotlib.pyplot as plt
from radpy.pyart_tools import radar_info
import pyart


def make_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Plot radar file.')
    parser.add_argument('file', metavar='FILE', type=str,
                        help='a file to plot')
    parser.add_argument('-f', '--field', type=str,
                        help='radar variable to plot, default: DBZ')
    parser.add_argument('-d', '--max-dist', type=int,
                        help='crop distance from radar (km)')
    return parser


def plot_file(filepath, field='DBZ', max_dist=None, **kws):
    radar = pyart.io.read(filepath)
    radar_info(radar)
    display = pyart.graph.RadarDisplay(radar)
    fig, ax = plt.subplots()
    display.plot(field, **kws)
    display.plot_cross_hair(5)
    if max_dist:
        ax.set_ylim(-max_dist, max_dist)
        ax.set_xlim(-max_dist, max_dist)
    plt.show()
    return radar


def main(*args, **kws):
    return plot_file(*args, **kws)


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    radar = main(args.file, field=args.field, max_dist=args.max_dist)
