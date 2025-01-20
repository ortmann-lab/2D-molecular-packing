import itertools

import numpy as np 
from scipy.spatial.transform import Rotation as R
from scipy.spatial import cKDTree

import constants




class MolSite:

    def __init__(self, elements = None, cart_coordinates = None, frac_coordinates = None, orientation = None, lattice_matrix = np.eye(3), ff_atom_types = None, charges = None) :

        self.elements = elements
        self._cart_coordinates = cart_coordinates
        self._frac_coordinates = frac_coordinates
        self.orientation = orientation
        self._lattice_matrix = lattice_matrix
        self.ff_atom_types = ff_atom_types
        self.charges = charges


    @property
    def lattice_matrix(self):
        return self._lattice_matrix

    @lattice_matrix.setter
    def lattice_matrix(self, value):
        self._lattice_matrix = value
        # Update frac_coordinates when lattice_matrix is set
        if self._cart_coordinates is not None:
            self._frac_coordinates = np.matmul(np.linalg.inv(value.T), self._cart_coordinates.T).T


    @property
    def cart_coordinates(self):
        if self._cart_coordinates is None:
            return np.matmul(self._lattice_matrix.T, self._frac_coordinates.T).T
        else:
            return self._cart_coordinates
        
        
    @cart_coordinates.setter
    def cart_coordinates(self, value):
        self._cart_coordinates = value
        self._frac_coordinates = np.matmul(np.linalg.inv(self._lattice_matrix.T), value.T).T

    
    @property
    def frac_coordinates(self):
        if self._frac_coordinates is None:
            return np.matmul(np.linalg.inv(self._lattice_matrix.T), self._cart_coordinates.T).T
        else:
            return self._frac_coordinates


    @frac_coordinates.setter
    def frac_coordinates(self, value):
        self._frac_coordinates = value
        self._cart_coordinates = np.matmul(self._lattice_matrix.T, value.T).T


    def get_inertia_tensor(self, weights=None, xyz = None):  #possible to apply a numpy.einsum function
        
        if xyz is not None:
            coordinates_copy = np.copy(xyz)
            coordinates_copy -= np.mean(coordinates_copy, axis=0)
        else:    
            coordinates_copy = np.copy(self.cart_coordinates)
            coordinates_copy -= np.mean(coordinates_copy, axis=0)  
        
        
        if weights is None: 
            weights = np.ones(len(coordinates_copy))

        InertiaTensor = np.zeros([3,3])
        InertiaTensor[0,0] = np.sum(weights*coordinates_copy[:,1]**2 + weights*coordinates_copy[:,2]**2)
        InertiaTensor[1,1] = np.sum(weights*coordinates_copy[:,0]**2 + weights*coordinates_copy[:,2]**2)
        InertiaTensor[2,2] = np.sum(weights*coordinates_copy[:,0]**2 + weights*coordinates_copy[:,1]**2)
        InertiaTensor[0,1] = InertiaTensor[1,0] = -np.sum(weights*coordinates_copy[:,0]*coordinates_copy[:,1])
        InertiaTensor[0,2] = InertiaTensor[2,0] = -np.sum(weights*coordinates_copy[:,0]*coordinates_copy[:,2])
        InertiaTensor[1,2] = InertiaTensor[2,1] = -np.sum(weights*coordinates_copy[:,1]*coordinates_copy[:,2])
        
        return InertiaTensor


    def get_vdw_radii(self):

        return np.array([constants.vdw_radii[item] for item in self.elements])


    def get_mol_plane(self, angle_deviation = 2, covalend_bond_threshold = 1.9):

        xyz = self.cart_coordinates
        tree = cKDTree(xyz)

        planes = []
        for atom_idx in range(len(xyz)):

            close_atoms_distances, close_atoms_indices = tree.query(xyz[atom_idx] , k = list(range(1,6)))
            close_atoms_matrix = np.column_stack((close_atoms_distances, close_atoms_indices))
            covalent_bonded_atoms_idx = list(map(int, [line[1] for line in close_atoms_matrix if line[0] < covalend_bond_threshold]))

            combinations_of_planes = list(itertools.combinations(covalent_bonded_atoms_idx, 3))
            valid_combinations_of_planes = [plane for plane in combinations_of_planes if atom_idx in plane]
            planes.extend([*valid_combinations_of_planes])


        in_plane_atom_idx = []
        for plane in planes:
            
            plane_normal = np.cross((xyz[plane[1]] - xyz[plane[0]]), (xyz[plane[1]] - xyz[plane[2]]))         
            
            temp_in_plane_atom_idx = []
            for atom_to_compare in range(len(xyz)):
                 
                angles = []
                for point in plane: 
                    
                    vector_to_compare  = xyz[atom_to_compare] - xyz[point]
                    angle = np.abs(90 - np.degrees(np.arccos(np.matmul(vector_to_compare, plane_normal)/(np.linalg.norm(vector_to_compare) * np.linalg.norm(plane_normal)))))
                    angles.append(angle)
                
                if angles[0] < angle_deviation and angles[1] < angle_deviation and angles[2] < angle_deviation:
                    temp_in_plane_atom_idx.append(atom_to_compare)
                

            if len(temp_in_plane_atom_idx) > len(in_plane_atom_idx):
                in_plane_atom_idx = temp_in_plane_atom_idx
                in_plane_atom_idx.extend([plane[0], plane[1], plane[2]])
      
        return xyz[in_plane_atom_idx]
    

    def aligh_mol(self, xyz = None):  # why multiplication in that way
        
        it = self.get_inertia_tensor(xyz = xyz)
        _, vec = np.linalg.eig(it)

        for idx, val in enumerate(np.diag(vec)): # save handness
            if val < 0:
                vec[:,idx] = vec[:,idx] * -1

        self.cart_coordinates = np.matmul(self.cart_coordinates, vec)  

        new_it = self.get_inertia_tensor(xyz = self.cart_coordinates)
        idx_of_max = np.argsort(np.diag(new_it))[::-1][0]

        if idx_of_max == 0:
            r = R.from_euler('y', 90, degrees=True)
            self.cart_coordinates = r.apply(self.cart_coordinates)
            
        if idx_of_max == 1:
            r = R.from_euler('x', 90, degrees=True)
            self.cart_coordinates = r.apply(self.cart_coordinates)
            

    def flip_site(self):
        
        c, s  = np.cos(np.deg2rad(180)), np.sin(np.deg2rad(180))
        
        R =  np.array([[1, 0, 0], 
                       [0, c,-s], 
                       [0, s, c]])
        
        self.cart_coordinates = np.matmul(R, self.cart_coordinates.T).T


    def rotate_site_z(self, deg):
        
        c, s = np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg))
        
        R = np.array([[c,-s, 0], 
                      [s, c, 0], 
                      [0, 0, 1]])
        
        self.cart_coordinates = np.matmul(R, self.cart_coordinates.T).T


    def translate_site(self, point):
        
        self.frac_coordinates = self.frac_coordinates + np.array(point)

    
    def cart2frac(self):

        return np.matmul(np.linalg.inv(self.lattice_matrix.T), self.cart_coordinates.T).T
    
    
    def frac2cart(self):

        return np.matmul(self.lattice_matrix.T, self.frac_coordinates.T).T
    


