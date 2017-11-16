#!/bin/bash
# compress one netcdf file
tmpfile=$(mktemp)

trap "rm -f tmpfile" EXIT # clean on signal
echo $1
/usr/bin/nccopy -d4 -w $1 $tmpfile
mv $tmpfile $1
