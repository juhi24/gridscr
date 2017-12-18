#!/bin/bash
# Grid and compress a single cfradial file.
fpath=$1
site=$2
echo $fpath
outfile=$(radx.sh Radx2Grid -params ./${site}_grid_params -f $fpath 2>&1|grep "Data written to"|awk -F " " '{print $NF}')
echo $outfile
nccompress.sh $outfile
