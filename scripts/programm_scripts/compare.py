import itertools, os, glob

import numpy as np

from pymatgen.core import Lattice, Structure, Molecule
from pymatgen.analysis.structure_matcher import StructureMatcher

from ase import io as ase_io




files = glob.glob("*_gulp.cif")

number_of_structures = len(files) - len(files)%5
number_of_parts = 5

list_of_structures = list(range(number_of_structures))

def intervals(number_of_parts, number_of_structures):
    part = number_of_structures / number_of_parts
    return [(i * part, (i + 1) * part) for i in range(number_of_parts)]


def compare(a,b):

    cif_file_path1 = f'{a}_gulp.cif'
    cif_file_path2 = f'{b}_gulp.cif'

    structure1 = Structure.from_file(cif_file_path1)
    structure2 = Structure.from_file(cif_file_path2)

    matcher = StructureMatcher(scale=True)
    return matcher.fit(structure1, structure2)


intervals_list = intervals(number_of_parts, number_of_structures)

duplicates_set = set()

for interval_idx in range(len(intervals_list)):

    my_interval = intervals_list[interval_idx]

    combinations = list(itertools.combinations(range(int(my_interval[0]), int(my_interval[1])), 2))

    for idx, itm in enumerate(combinations):
        i, j = itm
        if compare(i, j) == True:
            duplicates_set.add(j)
            for pair in combinations[idx + 1:]:
                if j in pair:
                    combinations.remove(pair)



duplicates = list(duplicates_set)

unique_structures = [i for i in list_of_structures if i not in duplicates]

with open("unique_structures.txt", "w") as output:
    output.write(str(unique_structures))


for dupl in list_of_structures:
    if dupl not in unique_structures:
        os.remove(f'{dupl}_gulp.cif')


for i, j in zip(unique_structures, range(len(unique_structures))):
    atoms = ase_io.read(f'{i}_gulp.cif')
    atoms.write(f'{j}_gulp_unique.cif')	
