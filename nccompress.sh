#!/bin/bash
# compress one netcdf file
echo $1
tmpfile=/tmp/$(basename $1)
/usr/bin/nccopy -d4 -w $1 $tmpfile
mv $tmpfile $1
