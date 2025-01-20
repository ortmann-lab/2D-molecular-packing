#!/bin/bash

states=(00 01)

for conformer in {1..5}
do
	cd "$conformer"
	for state in "${states[@]}"
	do
		cd "$state"
		mkdir gulp_clustering
		cp gulp/*_temp/*.cif gulp_clustering
		cp gulp/*_temp/*.gout gulp_clustering
		cd gulp_clustering
		cp ../../../programm_scripts/compare.py .
		cp ../../../job_scripts/master_gulp_compare.sh master.sh
		cp ../../../programm_scripts/get_volume.sh .
		cp ../../../programm_scripts/get_energy.sh .
		./get_energy.sh &
		./get_volume.sh
		cp ../../../programm_scripts/gulp_filter.py .
		python gulp_filter.py
		rm *.gout
		cd ../..
	done
	
	cd ..

done



