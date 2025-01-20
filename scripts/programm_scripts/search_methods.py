import itertools

import numpy as np 




class SearchGrid:

    def __init__(self, a_values, b_values, c_values, alpha_values, beta_values, gamma_values, sites_values, same_kind = True, dimensionality = "2D"):

        self.a_values = a_values
        self.b_values = b_values 
        self.c_values = c_values
        self.alpha_values = alpha_values
        self.beta_values = beta_values
        self.gamma_values = gamma_values
        self.sites_values = sites_values
        self.same_kind = same_kind
        self.dimensionality = dimensionality

    
    def search_paramenters(self):

        if self.dimensionality == "3D":
            search_parameters = [self.a_values, self.b_values, self.c_values, self.alpha_values, self.beta_values, self.gamma_values]
            for site in self.sites_values:
                search_parameters.extend([*site])
    
        if self.dimensionality == "2D":
            search_parameters = [self.a_values, self.b_values, self.gamma_values]
            for site in self.sites_values:
                search_parameters.extend([*site])
            
        parameters_len = [*map(len, search_parameters)]
        estimated_number_of_structures = 1
        for x in parameters_len:
            estimated_number_of_structures *= x

        if estimated_number_of_structures > 15*10**6:
            raise Exception(f'You want to generate too many structures. Number of structures should not exceed 15 millions. Your input number is {estimated_number_of_structures}')

        return search_parameters


    def make_raw_grid(self):
        
        """Actually I dont know how it works, I just copy-pasted it from stackoverflow 
        (https://stackoverflow.com/questions/11144513/cartesian-product-of-x-and-y-array-points-into-single-array-of-2d-points/49445693#49445693)."""

        parameters = self.search_paramenters()
        la = len(parameters)
        dtype = np.result_type(*parameters)        
        arr = np.empty((la, *map(len, parameters)), dtype=dtype)
        idx = slice(None), *itertools.repeat(None, la)
        
        for i, a in enumerate(parameters):
            arr[i, ...] = a[idx[:la-i]]
            
        return arr.reshape(la, -1).T


    def check_same_position_configuration(self, configuration):

        positions_combination = list(itertools.combinations(range(len(self.sites_values)), 2))

        for pair in positions_combination:
            if configuration[4 + 3*pair[0]] == configuration[4 + 3*pair[1]] and configuration[4 + 3*pair[0] + 1] == configuration[4 + 3*pair[1] + 1]:
                return True
            else:
                continue
        
        return False


    def make_final_grid(self):

        return [configuration for configuration in self.make_raw_grid() if self.check_same_position_configuration(configuration) == False]
    