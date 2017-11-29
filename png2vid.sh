#!/bin/bash

usage() {
	echo "usage: $0 \"INPUT_PATTERN\" output_filename.mkv"
}

while getopts ":h" opt; do
	case $opt in
		h)
			usage
			exit 0;;
		\?)
			echo "Invalid option: -$OPTARG" >&2
			exit 1;;
	esac
done

ffmpeg -framerate 10 -pattern_type glob -i "$1" -s 1920x1080 -c:v libx264 -preset slow $2
