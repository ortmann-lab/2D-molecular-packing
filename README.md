# 2D-molecular-packing
This repository provides a computational tool for predicting 2D molecular packing in crystalline thin films of flexible organic molecules. The method utilizes an efficient grid search approach to explore molecular arrangements, enabling accurate predictions of 2D packing motifs while significantly reducing computational costs.

---

## **How to Use**

### 1. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/ortmann-lab/2D-molecular-packing.git
cd 2D-molecular-packing
pip install -r requirements.txt
```
Install  3rd-party software for geometry optimization interface:
- `GULP v.6.0+`
- `DFTB+ v.22.1+`
                  

### 2. Running the scripts
Copy a `scripts` folder and insert all required input data (see below) and sequentially run:
- `prep_relax_gulp.sh`
- `run_relax_gulp.sh`
- `prep_cluster_gulp.sh`
- `run_cluster_gulp.sh`
- `prep_relax_dftb.sh`
- `run_relax_dftb.sh`

### 3. Input documentation

See the [input documentation](docs/input.md) for input creation guidelines.

### 4. Test 
The `test` folder contains inputs for Target 5 molecule (see publication) to test scripts behavior.   

---

## **License**
This project is licensed under the terms of the Apache License 2.0.

## **Citation**
If you use this tool, please cite the following article:

*A. Gudovannyy, et al., "Predicting 2D Crystal Packing in Thin Films of Small Molecule Organic Materials" Advanced Functional Materials, 2025; DOI: 10.1002/adfm.202421048 *
