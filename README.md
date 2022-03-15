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

For certain scripts (optional),
- matplotlib
- BioPython

### External dependencies

- [probe](https://github.com/rlabduke/probe)
- [reduce](https://github.com/rlabduke/reduce)

Currently, a precompiled copy of each is present in `bin/`.

which both require
- CMake >= 3.10
- Any C/C++ compiler suite with C++11 support

## Usage example
If your structure is not prepared then go through 1-4 steps to add H and cleanup.
   ##this all corrections are users responsibility to check and recheck, since RINRUS will generate models from provided structure).

1. After getting a raw PDB file (`3bwm.pdb`), check for ambiguous atoms and do general clean up.
  (Example: if there is multiple conformation for residue then keep only one conformation, delete extra ions present in pdb)
  (keep only chain A or keep only one chain to generate models properly by RINRUS)
  (one sample example may be here of may be in tutorial example) 
  (structure taken from md simulation might have Na Cl or other ions which is not reqiored)
  (if structures is converted from other format like MD simulation file then need to check all atom names, residue names and number is correct).
  (ligand and metal cordinated atoms need their protonation state carefully checked)

2. Run `reduce` to generate a new H-added PDB file (`3bwm_h.pdb`): (or protonate with other program of your choice)
```bash
$HOME/git/RINRUS/bin/reduce -NOFLIP 3bwm.pdb > 3bwm_h.pdb 
   ###(check other flags of reduce program for your case by US)
```        (version of reduce, permission to distribue reduce)

3.save the file to a new file (`3bwm_h.pdb > 3bwm_h_modify.pdb`)

4. Check the new PDB file.If there is metal, replace with an atom with same coordination (if there is Mg, replace Mg with O), and save as a new PDB file.
   ##if metal is going to be part of seed then we need to replace metal with O to get correct cordination for probe)

5. Check all ligands, make sure H atoms were added correctly (may need to delete or add more H based on certain conditions)
   ##user needs to protonate ligand and substrate properly since reduce does not able to recognize and add H properly sometimes)
   ##check ligand table in rcsb website for more details of substrate Hydrogens).
   ##this all corrections are users responsibility to check and recheck, since RINRUS will generate models from provided structure).
   
6. If there are any "CA" or "CB" atoms in ligands, replace them with "CA'" and "CB'", respectively. (This will decide Freezing patterns so we don't want to freeze something in substrate mostly).
##THIS CAN BE AUTOMATED?? If ligand has canomical amino acids then many problems can arise later). eg. TDP1

7. Use this new PDB file (`3bwm_h_modify.pdb`) to run `probe` and save the result.
``` bash
$HOME/git/RINRUS/bin/probe -unformated -MC -self "all" 3bwm_h_modify.pdb > 3bwm_h_modify.probe 
```
(Default RIN generator is probe you can use arpeggio?) Instruction for arpeggio.
(Instructions for Distance based model building).

What is seed?, how to choose residue number from pdb file for seed, user needs to have seed number ready for)
(A good default seeds are substrates participating in chemical reaction is selected as seed by user.) 
A second useful seeds are a substrate and any residues or co-factor,fragmens, which is breaking and forming bonds- This will generate much larger models compare to first seed example.
For example of 3bwm we have selected 300(metal Mg2+),301 (SAM) and 302 (Catechol) as a seeds.
 
8. Run `probe2rins.py`. The seed is a comma-separated list of colon-separated pairs, the first part being the ID of the PDB subunit, the second part being the residue number in that subunit:(Chein:ResID)
``` bash
python3 $HOME/git/RINRUS/bin/probe2rins.py -f 3bwm_h_modify.probe -s 'A:300,A:301,A:302'
```
This produces `freq_per_res.dat`, `rin_list.dat`, `res_atoms.dat`, and `*.sif`.

9. Run "probe_freq_2pdb.py' to generate models, you need the correct pdb file probe file, and freq_per_res.dat file and the seed:
(more description how to build the models, which critia, alternative building schemes)
``` bash
python3 $HOME/git/RINRUS/bin/probe_freq_2pdb.py 3bwm_h_mg.ent 3bwm_h.probe freq_per_res.dat 'A:300,A:301,A:302'
```
This creates a `model_detail.dat` file that associates model sizes (residue count) with the residue numbers in that model, plus a `res_NNN.pdb` for each model, where `NNN` is the number of residues in that model.
- For example, if the largest model generated from the network has 34 residues, and the network seed contained 3 residues, then 32 files will be created: `res_34.pdb`, `res_33.pdb`, ..., `res_4.pdb`, and `res_3.pdb`.

10. Run `pymol_scripts.py` to add hydrogens to one or more `res_NNN.pdb` files:
```bash
python3 $HOME/git/RINRUS/bin/pymol_scripts.py res_NNN.pdb [res_NNN-1.pdb ...] --resids 300,301,302
```
which
- generates a `log.pml` PyMOL input file containing commands that perform the hydrogen addition, and then
- runs PyMOL to perform the addition.
If `--resids` is specified, those residue IDs will not have hydrogens added.

11. Run `write_input.py` for a single model to generate a template file and input file:
```bash
python3 $HOME/git/RINRUS/bin/write_input.py -noh res_NNN.pdb -adh res_NNN_h.pdb -intmp input_template
```

### Distance based rules

1. Run `python3 ~/git/RINRUS/bin/pdb_2dist_freq.py -pdb 3bwm_h_mg.ent -s A:300,A:301,A:302 -cut 5`
this will generate a file named `dist_per_res-5.00.dat`

2. Then Run `python3 ~/git/RINRUS/bin/pdb_dist_2pdb.py -pdb 3bwm_h_mg.ent -s A:300,A:301,A:302 -cut 5`
This will generate a set of trimmed pdb files such as `dres_3.pdb, dres_4.pdb...`

3. Then run `python3 ~/git/RINRUS/bin/pymol_scripts.py dres_3.pdb dres_3_h.pdb`
This will generate the H added pdb files.
