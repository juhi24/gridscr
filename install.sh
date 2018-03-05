#!/bin/bash
prefix=/usr/local
cp -r radpy $prefix/lib/python3.5/site-packages/
cp *.sh $prefix/bin/
cp *.py $prefix/bin/
cp qpe_composite $prefix/bin/
cp var2nc $prefix/bin/
