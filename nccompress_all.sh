#!/bin/bash

usage() {
  echo "Usage: $0 [-h] DIRECTORY
Run nccompress for all cfrad files in DIRECTORY." 1>&2
  exit 1
}

while getopts ":h" opt; do
  case $opt in
    h)
      usage
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

#parallel nccompress.sh ::: $(find $1 -name cfrad.*.nc)
find $1 -name cfrad.*.nc -print0|xargs -P 2 -n 1 -0 nccompress.sh
