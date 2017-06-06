#!/bin/bash
for site in KUM KER VAN; do
	cat /media/jussitii/04fafa8f-c3ca-48ee-ae7f-046cf576b1ee/grids/${site}_goodfiles.csv|grep ncf_20160904_00|sed 's/1ee/1ee\/test\/cf/g'>${site}_goodfiles.csv
done
