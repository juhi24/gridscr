#!/bin/bash
prefix=/usr/local
#cpconf=--no-preserve=mode,ownership
cpconf="--chown=root:root -pogt --chmod=go=rx"
method=rsync
rsync $@ --chown=root:root --chmod=Fgo=r,Dgo=rx -rpogt radpy $prefix/lib/python2.7/site-packages/
$method $@ $cpconf *.sh $prefix/bin/
$method $@ $cpconf *.py $prefix/bin/
$method $@ $cpconf qpe_composite $prefix/bin/
$method $@ $cpconf var2nc $prefix/bin/
# Install datafiles
mkdir -p --mode=755 $prefix/share/radpy/
$method $@ --chown=root:root -pogt --chmod=go=r data/grid.mat $prefix/share/radpy/
