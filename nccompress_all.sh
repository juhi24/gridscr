#!/bin/bash
#parallel nccompress.sh ::: $(find $1 -name cfrad.*.nc)
find $1 -name ncf*.nc -print0|xargs -P 2 -n 1 -0 nccompress.sh
