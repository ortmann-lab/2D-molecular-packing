#!/bin/bash

states=(00 01)

for conformer in {1..5}
do
	cd "$conformer"
	for state in "${states[@]}"
	do
		cd "$state"
		mkdir dftb
		cp gulp_clustering/*_gulp_unique.cif dftb
		cd dftb
		cp ../../../programm_scripts/cif2gen.py .
		cp ../../../relax_input/dftb_in.hsd .
		cp ../../../job_scripts/master_dftb_relax.sh master.sh
		python cif2gen.py
		cd ../..
	done
	
	cd ..

done



