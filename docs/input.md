## Required input data:

1. gen_input_xx main input file. xx means chirality configuration. For Z = 2, only two possibilities - 00, 01 (see publication for details). Required for variable $states in scrips/*.sh.
2. input_conformer_N/ folder where N number of conformer. input_conformer_N/ content:
    1. mol_x.xyz - xyz file of molecule.
    2. mol_x_atom_types - column array of atomic types according internal GULP library types 
    3. mol_x_charges - column array of calculated charge on each atom of the molecule
    where x - molecule's name from the "composition" setting.
3. Additionally required relax_input/ folder which contain 3rd party code input folder (e.g. dftb_in.hsd)       

### gen_input_xx settings:
"search type": "grid", 						                - search method.
"system type": "layer" 						                - system type.
"Z" : 2,    							                    - molecules per unit cell.			
"composition": [1, 1],					                    - molecule's name. Used in "input_conformer_N" folder.
"planar chirality": [false, false],			                - apply molecular flipping to simulate planar chirality.
"aligh according cycles" : [false, false]                   - align and locate molecule in a plane according most planar part of the molecule.
"a" : [40, 40, 1],						                    - a lattice constant scan values in format start:stor:step.
"b" : [40, 40, 1],						                    - b lattice constant scan values in format start:stor:step.
"c" : [20, 20, 1],						                    - c lattice constant scan values in format start:stor:step.
"alpha" : [90, 90, 1],						                - alpha angle scan values in format start:stor:step. Not relevant for layers.
"beta"  : [90, 90, 1],						                - beta angle scan values in format start:stor:step. Not relevant for layers.
"gamma" : [90, 90, 1]						                - gamma angle scan values in format start:stor:step. Relevant for layers.				
"rotations" : [[0, 360, 30],				                - phi_1 molecular orientation angle scan values in format start:stor:step. Depends on Z value.
               [0, 360, 30]],
"unit cell grid translation" : [[[0.5, 0.5, 1], [0, 0, 1]],	- molecular position values in fractional coordinates in format start:stor:step. Depends on Z value.
                               [[0, 1, 2], [0, 1, 2]]]

  
