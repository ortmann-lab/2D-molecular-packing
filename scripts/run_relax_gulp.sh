#!/bin/bash

states=(00 01)

for conformer in {1..5}
do
	cd "$conformer"
	for state in "${states[@]}"
	do
		cd "$state"/gulp
		sbatch master.sh
		cd ../..
	done
	
	cd ..

done
