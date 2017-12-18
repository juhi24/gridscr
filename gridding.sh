#!/bin/bash
# Takes input search folder as an argument.
declare -A searchterms
searchterms=(["KER"]="Kerava" ["VAN"]="VANTAA" ["KUM"]="Kumpula")
for site in VAN KER KUM; do
	find $1 -name "cfrad*${searchterms[$site]}*.nc" -print0|xargs -I fpath -P 4 -n 1 -0 timeout 10 grid.sh fpath $site
done
