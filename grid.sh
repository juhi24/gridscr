#!/bin/bash
# Grid and compress a single cfradial file.
fpath=$1
site=$2
hdd=/media/jussitii/04fafa8f-c3ca-48ee-ae7f-046cf576b1ee
outfile=$(Radx2Grid -params $hdd/${site}_grid_params -f $fpath 2>&1|grep "Data written to"|awk -F " " '{print $NF}')
echo $outfile
$hdd/bin/nccompress.sh $outfile
