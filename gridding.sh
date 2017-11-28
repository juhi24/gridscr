#!/bin/bash
# Takes input search folder as an argument.
hdd=/media/jussitii/04fafa8f-c3ca-48ee-ae7f-046cf576b1ee
declare -A searchterms
searchterms=(["KER"]="Kerava" ["VAN"]="VANTAA" ["KUM"]="Kumpula")
for site in VAN KER KUM; do
	find $1 -name "cfrad*${searchterms[$site]}*.nc" -print0|xargs -I fpath -P 4 -n 1 -0 timeout 10 $hdd/bin/grid.sh fpath $site
done
