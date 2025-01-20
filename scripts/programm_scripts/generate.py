import copy, json, time

import numpy as np

import crystal, molecular_site, search_methods

#######################################################
#--------------------INPUT-PARSING--------------------#   (DEFINE PARAMETERS FOR SINGLE MOLECULE)
#######################################################

with open('gen_input', 'r') as gen_input:
    input = json.load(gen_input)


search_type = input['general']['search type']
Z = input['system description']['Z']

mol_composition = input['system description']['composition']
mol_planar_chirality = input['system description']['planar chirality']
mol_orientation = input['system description']['aligh according cycles']

a_values = np.linspace(input['unit cell parameters']['a'][0], input['unit cell parameters']['a'][1], int(input['unit cell parameters']['a'][2]))
b_values = np.linspace(input['unit cell parameters']['b'][0], input['unit cell parameters']['b'][1], int(input['unit cell parameters']['b'][2]))
c_values = np.linspace(input['unit cell parameters']['c'][0], input['unit cell parameters']['c'][1], int(input['unit cell parameters']['c'][2]))
alpha_values = np.linspace(input['unit cell parameters']['alpha'][0], input['unit cell parameters']['alpha'][1], int(input['unit cell parameters']['alpha'][2]))
beta_values = np.linspace(input['unit cell parameters']['beta'][0], input['unit cell parameters']['beta'][1], int(input['unit cell parameters']['beta'][2]))
gamma_values = np.linspace(input['unit cell parameters']['gamma'][0], input['unit cell parameters']['gamma'][1], int(input['unit cell parameters']['gamma'][2]))


sites_values = []

for site in range(Z):
    sites_values.append((np.linspace(input['sites tranformations']['rotations'][site][0], input['sites tranformations']['rotations'][site][1], int(input['sites tranformations']['rotations'][site][2]), endpoint=False),
                         np.linspace(input['sites tranformations']['unit cell grid translation'][site][0][0], input['sites tranformations']['unit cell grid translation'][site][0][1], int(input['sites tranformations']['unit cell grid translation'][site][0][2]), endpoint=False),
                         np.linspace(input['sites tranformations']['unit cell grid translation'][site][1][0], input['sites tranformations']['unit cell grid translation'][site][1][1], int(input['sites tranformations']['unit cell grid translation'][site][1][2]), endpoint=False)))



#######################################################
#------------------MOLECULES-READING------------------#
#######################################################

sites = []

for idx, molecule in zip(range(Z), mol_composition):
    input_elemements = np.genfromtxt(f'mol_{molecule}.xyz', skip_header=2, usecols = 0, dtype='str')
    input_coordinates = np.loadtxt(f'mol_{molecule}.xyz', skiprows=2, usecols=(1,2,3))

    input_ff_atom_types = np.genfromtxt(f'mol_{molecule}_atom_types', dtype='str')
    input_charges = np.loadtxt(f'mol_{molecule}_charges')

    input_planar_chirality = mol_planar_chirality[idx]
    input_mol_orientation = mol_orientation[idx]


    site = molecular_site.MolSite(elements=input_elemements, cart_coordinates=input_coordinates, ff_atom_types = input_ff_atom_types, charges = input_charges)

    if input_mol_orientation == True:
        site.aligh_mol(site.get_mol_plane())
        site.cart_coordinates -= np.mean(site.get_mol_plane(), axis=0)
    else:
        site.aligh_mol()
        site.cart_coordinates -= np.mean(site.cart_coordinates, axis=0)

    if input_planar_chirality == True:
        site.flip_site()

    sites.append(site)


######################################################
#---------------STRUCTURES GENERATING----------------#
######################################################

test_grid = search_methods.SearchGrid(a_values = a_values, b_values = b_values, c_values = c_values,
                                      alpha_values = alpha_values, beta_values = beta_values,
                                      gamma_values = gamma_values, sites_values = sites_values,
                                      same_kind = True, dimensionality = "2D").make_final_grid()


idx = 0
for configuration in test_grid:

    sites_copy = copy.deepcopy(sites)
    cs = crystal.CrystalStruture(a = configuration[0], b = configuration[1], c = c_values[0], gamma = configuration[2], sites=sites_copy)

    for site_idx in range(len(cs.sites)):

        cs.sites[site_idx].lattice_matrix = cs.lattice_matrix
        cs.sites[site_idx].rotate_site_z(configuration[3 + 3*site_idx])
        cs.sites[site_idx].translate_site([configuration[4 + 3*site_idx], configuration[4 + 3*site_idx + 1], 0.5])

    if cs.single_cell_overlap() == False and cs.super_cell_overlap() == False:
        cs.write_gulp(f'{idx}')
        idx+=1
    else:
        continue