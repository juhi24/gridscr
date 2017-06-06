#!/bin/bash
for path in $(ls -d */|cut -d/ -f1); do
   tar caf $path.tar.gz $path --remove-files
done
