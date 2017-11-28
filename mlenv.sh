#!/bin/bash
# usage: mlenv.sh bin_name [ARGS]...
# Run compiled matlab functions in the directory of this script.
SCRDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCRROOT=/opt/MATLAB/R2017a
LD_LIBRARY_PATH=.:${MCRROOT}/runtime/glnxa64 ;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/bin/glnxa64 ;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/sys/os/glnxa64;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/sys/opengl/lib/glnxa64;
export LD_LIBRARY_PATH;
exec $SCRDIR/"$@"
