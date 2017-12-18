#!/bin/bash

usage() {
	echo "usage: $0 [-d YYYYMMDD] [-c CF_DIR] [-l LOG_DIR] [-h]"
}

# Input argument defaults
DATE_GLOB='*'
LOG_DIR='.'
CF_DIR='cf'

while getopts ":d:l:c:h" opt; do
	case $opt in
		d) DATE_GLOB="$OPTARG";;
		c) CF_DIR=$OPTARG;;
		l) LOG_DIR=$OPTARG;;
		h)
			usage
			exit 0;;
		\?)
			echo "Invalid option: -$OPTARG" >&2
			exit 1;;
		:)
			echo "Option -$OPTARG requires an argument." >&2
			exit 1;;
	esac
done

echo "### Raw conversion."
trap "exit" INT
for f in ???data/*/*.raw ???data/*/*/*.RAW*; do
 	raw2cfrad.py -vd -o $CF_DIR "$f" >> $LOG_DIR/raw2cfrad.log 2>> $LOG_DIR/raw2cfrad.err
done
echo "### Adding extra variables."
mlenv.sh var2nc "$CF_DIR/*/cfrad.*.nc" > $LOG_DIR/var2nc.log 2> $LOG_DIR/var2nc.err
echo "### Recover KUM Kdp."
recover_kdp.py -fv $CF_DIR/*/cfrad.*Kum*.nc > $LOG_DIR/recover_kdp.log 2> $LOG_DIR/recover_kdp.err
echo "### Gridding."
gridding.sh $CF_DIR > $LOG_DIR/gridding.log 2> $LOG_DIR/gridding.err
echo "### Compositing."
qpe_composite.sh grids > $LOG_DIR/qpe_composite.log 2> $LOG_DIR/qpe_composite.err
echo "### Postprocessing."
compost.py -ipmv -o composite brancomp/$DATE_GLOB.mat
