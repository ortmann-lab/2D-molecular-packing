import os

import numpy as np




Z = 2

def convert(path, new_idx):
    with open(f'{path}_relaxed.cif', 'r') as file:
        data = file.readlines()

        data[0] = f"data_{path}\n"
        data[7] = f"\n"
        data[8] = f"_space_group_symop_operation_xyz   'x, y, z'\n"
        data[9] = f"\n"


    with open(f'{new_idx}_gulp.cif', 'w') as file:
        file.writelines(data)


with open("gulp_energies") as f:
    gulp_energies = f.readlines()

list_wo_gaps = [line for line in gulp_energies if len(line) > 20]

with open('gulp_energies_new', 'w') as file:
    file.writelines(list_wo_gaps)

with open("gulp_energies_new") as f:
    gulp_energies = f.read()

new_energies = gulp_energies.replace('****************', '     1000000')

with open('new_energies', 'w') as file:
    file.writelines(new_energies)

e = np.loadtxt('new_energies', usecols=4)
v = np.loadtxt('gulp_volumes', usecols=5)

e_relative = np.array([(i - min(e)) for i in e])

num_labels = np.loadtxt('new_energies', usecols=0)
stacked = np.column_stack((num_labels, e_relative))
sorted_energy_list = stacked[stacked[:, 1].argsort()]
sorted_energy_list = sorted_energy_list[sorted_energy_list[:,1] < 10*Z]
numbers_of_sorted_energy_list = sorted_energy_list[:,0].astype(int)


min_v = min(v[numbers_of_sorted_energy_list])

print(min_v)

good_structures = []
for i in numbers_of_sorted_energy_list:
    if (v[i] - min_v) < min_v*0.33 :
        good_structures.append(i)


for bad_structure in range(len(v)):
    if bad_structure not in good_structures:
        try:
            os.remove(f'{bad_structure}_relaxed.cif')
        except Exception:
            pass


for i, j in enumerate(good_structures):
    convert(j, i)
    os.remove(f'{j}_relaxed.cif')





