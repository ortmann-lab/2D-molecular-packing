import glob

from ase import io




files = glob.glob("*_gulp_unique.cif")

number_of_structures = len(files)

for i in range(number_of_structures):
    atoms = io.read(f'{i}_gulp_unique.cif', store_tags=True)
    atoms.write(f'{i}_dftb.gen', format='dftb')

