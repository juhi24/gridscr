#!/bin/bash
# usage: composite_workflow.sh /log/dir
cfdir=cf
logdir=$1
echo "### Raw conversion."
raw2cfrad.py -v -o $cfdir ???data/*/*.raw ???data/*/*/*.RAW* > $logdir/raw2cfrad.log 2> $logdir/raw2cfrad.err
echo "### Adding extra variables."
mlenv.sh var2nc "$cfdir/*/cfrad.*.nc" > $logdir/var2nc.log 2> $logdir/var2nc.err
echo "### Checking KUM data for missing KDP."
recover_kdp.py -v $cfdir/*/cfrad.*Kum*.nc > $logdir/recover_kdp.log 2> $logdir/recover_kdp.err
echo "### Gridding."
gridding.sh $cfdir > $logdir/gridding.log 2> $logdir/gridding.err

