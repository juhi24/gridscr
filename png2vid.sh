#!/bin/bash
ffmpeg -framerate 10 -pattern_type glob -i "$1" -c:v libx264 $2
