#!/bin/bash
GRIDPATH=$1
mlenv.sh qpe_composite "$GRIDPATH/KER/*/*.nc" "$GRIDPATH/KUM/*/*.nc" "$GRIDPATH/VAN/*/*.nc" brancomp
