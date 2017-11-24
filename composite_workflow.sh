#!/bin/bash
cfdir=cf
echo "### Raw conversion."
raw2cfrad.py -v -o $cfdir ???data/*/*.raw ???data/*/*/*.RAW*
echo "### Adding extra variables."
var2nc.sh "$cfdir/*/cfrad.*.nc"
echo "### Checking KUM data for missing KDP."
recover_kdp.py -v $cfdir/*/cfrad.*Kum*.nc
echo "### Gridding."
gridding.sh $cfdir
