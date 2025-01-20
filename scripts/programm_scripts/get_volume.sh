#!/bin/bash

NUM_STRUCTURES=$(ls -1 *.gout | wc -l)

for i in $(seq 0 $NUM_STRUCTURES)
do 
    vol=$(grep "Primitive cell volume" "$i".gout)
    if [ ! -z "$vol" ]; then echo " "$i" "$vol" " >> gulp_volumes; else echo " "$i"  Primitive cell volume = 99999.000000 Angs**3" >> gulp_volumes; fi
done





