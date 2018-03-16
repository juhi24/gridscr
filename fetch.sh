#!/bin/bash
# usage: fetch.sh LIST_FILE [RSYNC_ARGS...]
# fetch kumpula and kerava radar data based on a file list
user=radarop
for ndisk in 0 1; do
  for radardir in KUMdata KERdata; do
    rsync -rv --ignore-existing --include-from $1 --include='*/' --exclude='*' $user@drizzle.atm.helsinki.fi:/disk$ndisk/$radardir/ ./$radardir "${@:2}"
  done
done
