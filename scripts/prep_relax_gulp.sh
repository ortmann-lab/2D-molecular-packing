#!/bin/bash

states=(00 01)

for conformer in {1..5}
do
	mkdir "$conformer"
	cd "$conformer"
	for state in "${states[@]}"
	do
		mkdir "$state"
		cd "$state"
		mkdir gulp
		cd gulp
		mkdir input_structures
		cd input_structures
		cp ../../../../programm_scripts/*.py .
		cp ../../../../gen_input_"$state" gen_input
		cp ../../../../input_conformer_"$conformer"/mol_* .
		python generate.py
		cd ..
		cp ../../../job_scripts/master_gulp_relax.sh master.sh
		cd ../..
	done
	
	cd ..

done



