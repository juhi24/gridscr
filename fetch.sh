#!/bin/bash
rsync -rv --ignore-existing --include-from $1 --include='*/' --exclude='*' login.physics.helsinki.fi:/data/scratch2/uhradar/RadarData/ . $@
#chown -R :uhradar $radardir

