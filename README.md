# RINRUS

Residue Interaction Network-based ResidUe Selector (RINRUS) is a QM-cluster model building tool.  Starting from a raw PDB file, after running a series of preparation tasks, the tool will
- select important residues for chemical reactions, and
- generate trimmed PDB files with the corresponding quantum chemical inputs.

## Installation

Clone this repository, then add the library code under `lib3` to your `PYTHONPATH`. For example, in `~/git`:
``` bash
cd ~/git
git clone git@github.com:MiloCheng17/RINRUS.git
export PYTHONPATH="~/git/RINRUS/lib3:$PYTHONPATH"
```

### Python dependencies

- Python >= 3.x
- NumPy
- pymol
  - If installing via conda, it's under `-c conda-forge pymol-open-source`.
- openbabel (required for Arpeggio)

For certain scripts (optional),
- matplotlib
- BioPython

### External dependencies

- [probe](https://github.com/rlabduke/probe) - version 2.16.130520 is packaged with RINRUS
- [reduce](https://github.com/rlabduke/reduce) - version 3.23 is packaged with RINRUS
- [arpeggio](http://biosig.unimelb.edu.au/arpeggioweb)

Currently, a precompiled copy of each is present in `bin/`.

which require
- CMake >= 3.10
- Any C/C++ compiler suite with C++11 support

Current production-level use cases are described in `/bin/test`.

## Usage example 1 - generating a single or a few input files with probe interaction count ranking 

<<<<<<< HEAD
## Usage example 2 - generating a single or a few input files with distance-based ranking
=======
6. To add hydrogens to fill the place where bonds were broken when the model was trimmed away, run the command below.
```bash
python3 ~/git/RINRUS/bin/pymol_scripts.py res_16.pdb 202 
```
## NOTE: The pymol_scripts.py script does not  work for now, so you need to copy `log.pml` from some old directory and edit the res_NN and the substrates information accordingly in `log.pml` file
 If this is your start time building models with RINRUS, copy log.pml file from here: `/home/dagbaglo/chem/2cht/XTAL/arpeggio/res_13-ts-01` (**This path needs to be changed for public**)
 Run log.pm as:
 ```bash
 pymol -qc log.pml
```
>>>>>>> 9b06a28c84ddda7d7f0d996a2e30fde529cc98fd

## Usage example 3 - generating a single or a few input files with arpeggio interaction-type ranking

## Usage example 4 - generating a single or a few input files with manual ranking (from SAPT, ML, or from some scheme that doesn't yet interface with RINRUS automatically)

## GENERATE ALL THE THINGS!!! Combinatorial model building from arpeggio or probe
## Usage example 5a - Combinatorial model building from arpeggio
## Usage example 5b - Combinatorial model building from probe
