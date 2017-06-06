#!/bin/bash
rsync -rv --ignore-existing --exclude='*.RHI*' --exclude='*.ZDRCAL*' --include-from $1 --include='*/' --exclude='*' login.physics.helsinki.fi:/data/scratch2/uhradar/RadarData/ .
