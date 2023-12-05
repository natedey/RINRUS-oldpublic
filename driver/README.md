


```bash
$HOME/git/RINRUS/drive-test202302/Taylor_driver_test.py -i driver_input -nor False 
``` 
### Driver Flag options
- -i <filename>:
  - The template format input file is the file **_driver_input_**  
- -nor <boolean>:
  - **_False_** reduce is used and this is the default.
  - **_True_** reduce is not used.

### Log file
The driver log file is names **_newfile.log_**

## Input File Format
- PDB filename
- Seed: format <chain_id:number>
- Type of RIN program (The input options are below)
  - _Probe_
  - _Arpeggio_
  - _Distance_
  - _Manual_
- Substrate charge
- Multiplicity
- Computational Program
- Path to the input template file
- Path to the basis set library
- Path to the RINRUS bin directory

## Driver script commands and flags that are included when running. ##
### Reduce Command
```bash
$HOME/git/RINRUS/bin/reduce -NOFLIP -Quiet PDB.pdb > PDB_h.pdb 
```
### Probe Command
```bash
$HOME/git/RINRUS/bin/probe -unformated -MC -self "all" -Quiet ' PDB_h > PDB.probe
```
Then runs the rinrus trim script, pymol script and write inputs script in the manual command section
### Arpeggio Command
```bash
$HOME/git/RINRUS/bin/arpeggio/arpeggio.py PDB.pdb
```

```bash
$HOME/git/RINRUS/bin/arpeggio2rins.py -f PDB.contacts -s seed_number
```

```bash
$HOME/git/RINRUS/bin/rinrus_trim2_pdb.py -s seed_number -pdb PDB.pdb -c contact_counts.dat -model NNN
```
Then runs the pymol script and write inputs script in the manual command section

### Distance Command
```bash
$HOME/git/RINRUS/bin/pdb_dist_rank.py -pdb PDB.pdb -s seed -cut distance -type avg/mass
```
-Once res_atom file made switch program option too manual


### Manual Command
_Rinrus Trim script_
```bash
$HOME/git/RINRUS/bin/rinrus_trim2_pdb.py -s seed -pdb PDB_modify.pdb -model NNN
```
_Pymol Scripts_
```bash
$HOME/git/RINRUS/bin/pymol_scripts.py -ignore_ids ### -pdbfilename res_#.pdb
```
_Write Inputs script_
```bash
$HOME/git/RINRUS/bin/write_input.py -intmp path_to_template -format computational_program -basisinfo path_to_basis_info -c charge -noh res_#.pdb -adh res_#_h.pdb
```






