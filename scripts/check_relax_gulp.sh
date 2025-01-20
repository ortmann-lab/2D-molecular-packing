#!/bin/bash

states=(00 01)

for conformer in {1..5}
do	
        cd "$conformer"
	for state in "${states[@]}"
	do
		cd "$state"/gulp
		echo "Conformer : "$(($conformer))"" && echo "State: "$(($state))""
		echo "Input:" && ls -1 input_structures/*.gin | wc -l
		echo "Result:" && ls -1 *_temp/*.gout | wc -l
		echo "CIFs:" && ls -1 *_temp/*.cif | wc -l 
		echo "___________________________" 

               cd ../..
	done
	
	cd ..

done



