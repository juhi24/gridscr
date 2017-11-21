#!/bin/bash
for path in $(ls -d VANdata/*); do
   radx.sh RadxConvert -params convert_params -f $path/*
   #rm -rf $path
done
for path in $(ls -d K**data/MonthlyArchivedData/*); do
   radx.sh RadxConvert -params convert_params -f $path/*
   #rm -rf $path
done
