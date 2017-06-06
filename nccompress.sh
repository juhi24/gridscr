#!/bin/bash
tmpfile=/tmp/$(basename $1)
/usr/bin/nccopy -d4 -w $1 $tmpfile
mv $tmpfile $1
