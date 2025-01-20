#!/bin/bash

NUM_STRUCTURES=$(ls -1 *.gout | wc -l)

for i in $(seq 0 $NUM_STRUCTURES)
do
    echo  "$i" "$(grep "Final energy =" "$i".gout) " >> gulp_energies
done


