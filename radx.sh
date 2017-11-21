#!/bin/bash
libpath=/usr/local/bin/radx_runtime_libs
if [ -n "$LD_LIBRARY_PATH" ]; then
  LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$libpath
else
  LD_LIBRARY_PATH=$libpath
fi
export LD_LIBRARY_PATH
exec $@
