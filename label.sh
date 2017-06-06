#!/bin/bash
for filepath in $(readlink -f $@)
do
dirpath=$(dirname $filepath)
filename=$(basename $filepath)
mkdir -p $dirpath/timestamped
fname=$(echo $filename|cut -d '.' -f 1)
yyyy=$(echo $fname|cut -b 7-10)
mm=$(echo $fname|cut -b 11-12)
dd=$(echo $fname|cut -b 13-14)
HH=$(echo $fname|cut -b 16-17)
MM=$(echo $fname|cut -b 18-19)
#SS=$(echo $fname|cut -b 20-21)
#tld=$(echo $filename|cut -d '.' -f 2)
convert $filepath -fill black -pointsize 9 -annotate +10+10 "$yyyy-$mm-$dd $HH:$MM" $dirpath/timestamped/$filename
done
