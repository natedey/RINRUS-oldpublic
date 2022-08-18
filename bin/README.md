
## Usage example 1 - generating a single or a few input files with probe interaction count ranking 

If your structure is not appropriately pre-processed then go through steps 1-4 to protonate and clean up substrate molecules. This is the user's responsibility to verify, since RINRUS will generate models from provided structure and cannot yet run sanity checks

1. After getting a raw PDB file (`3bwm.pdb`), check for nonstandard fragments, clean up atoms or residues with alternate positions/conformations. Listed below are some possible tasks that need to be done before starting the workflow:
   a) if there are multiple conformations for a residue then keep only one conformation
   b) If starting from MD simulation, you may want to delete neutralizing counterions if they have migrated into the active site
   c) If crystallographic symmetry is embedded into the pdb, one needs to be very careful and manually "unfold" the multimers from the PDB website. This might be more common with older X-ray crystal structures #We should find a way to have RINRUS recognize this and automate
  d) We have seen situations where AMBER truncates atom names of two-letter elements when writing to PDB format (turning FE into F for example). If PDB file comes from source other than PDB repository or similar database, check all atom names, residue names, and residue ID #s
  e) If coming from MD, check that metal coordination is correct

2. If the protein is not yet protonated, run `reduce` to generate a new protonated PDB file  (`3bwm_h.pdb`): (or protonate with other program of your choice). Skip this step if the pdb file is from MD simulation since it has been protonated already.
```bash
$HOME/git/RINRUS/bin/reduce -NOFLIP 3bwm.pdb > 3bwm_h.pdb 
``` 
###(check other flags of reduce program for your case by US)
###(version of reduce, permission to distribute reduce)

3. copy the protonated PDB to a new filename (`3bwm_h.pdb > 3bwm_h_modify.pdb`)

4. Check the new PDB file. Probe doesn't recognize covalent bonds, which becomes a big problem with metalloenzymes and metal-ligand coordination. Our workaround is to replace a metal coordination center with an atom that probe recognizes as a H-bond donor or acceptor to capture interactions with the coordinating ligand atoms. For example in COMT, we replace Mg with O), and save as a new PDB file.

5. Check all ligands, make sure H atoms were added correctly (may need to delete or add more H based on certain conditions). The user needs to protonate ligand and substrate properly since reduce does not recognize most substrates and may add H improperly. Check the ligand 2D drawing for the PDB entry on rcsb website for some guidance on substrate protonation if starting from scratch. Perform this step correctly is the user's responsibility! RINRUS will generate models from provided structure and does not have comprehensive sanity checks!
   
6. If there are any "CA" or "CB" atoms in substrate/ligands/noncanonical amino acids, replace them with "CA'" and "CB'", respectively. An example of this would be if the substrate is a polypeptide (like Tdp1). You would not want to freeze substrate Carbon alphas/betas. Renaming CA' / CA' will cause RINRUS to ignore these atoms when it makes the list of frozen atoms.  
###CAN THIS BE AUTOMATED?? Like after we run probe, could RINRUS go back through the PDB and "unfreeze" frozen atoms in seed residues?

7. Use the new PDB file (`3bwm_h_modify.pdb`) to run `probe` to generate .probe file	
``` bash
$HOME/git/RINRUS/bin/probe -unformated -MC -self "all" 3bwm_h_modify.pdb > 3bwm_h_modify.probe 
```
###NOTE: When creating QM-cluster models, remember to replace metal atom in PDB if it was replaced with O in step 4

***Step 8 is one of the most important steps of the QM-cluster model building process. The user must now define the "seed". What is the seed? Typically, the seed will be the substrate(s) (or ligand in biochemical terms) participating in the chemical reaction. Any amino acid residues, co-factors, or fragments which participate in the active site catalytic breaking and forming of chemical bonds may also need to be included as part of the seed, but this will generate much larger models compare to only using the substrate***

##Using the example of PDB:3BWM, we will select the PDB residue ID# of three fragments: 300(metal Mg2+), 301 (SAM) and 302 (Catechol - the substrate) as the seed. 3BWM only has one chain, so we must specify chain A throughout. If the PDB does not have chain identifiers, you will need specify ":XXX" where XXX is residue id number to use them in this step and beyond. If the protein is multimeric, use the chain of your choice for seed fragments. Note that some multimeric x-ray crystal structures may not necessarily have equivalent active sites!
###Does this automatically use chain A if chain isn't specified? No, defaults are wonky, especially if there is no chain ID in the PDB. We need to make better defaults here. 
8. Run `probe2rins.py`. The seed is a comma-separated list of colon-separated pairs, the first part being the ID of the PDB subunit, the second part being the residue number in that subunit:(Chein:ResID)
``` bash
python3 $HOME/git/RINRUS/bin/probe2rins.py -f 3bwm_h_modify.probe -s A:300,A:301,A:302
```
This produces `freq_per_res.dat`, `rin_list.dat`, `res_atoms.dat`, and `*.sif`.

10. With the res_atoms.dat file generated, use this file to generate the trimmed PDB model using the RINRUSv2 script:
```bash
python3 ~/git/RINRUS/bin/rinrus_trim2_pdb.py -s A:300,A:301,A:302 -pdb 3bwm_h_modify.pdb 
```
This generates automatically generate the entire "ladder" of possible models based on a ranking scheme which contain `res_NNN.pdb`, `res_NNN_froz_info.dat` and `res_NNN_atom_info.dat` for the all models, where `NNN` is the number of residues in that model.

#Note: if you want to  generate one model based on a any ranking scheme, you will need to run a same script with the flag `-model NNN` as 
```bash
python3 ~/git/RINRUS/bin/rinrus_trim2_pdb.py -s A:300,A:301,A:302 -pdb 3bwm_h_modify.pdb -model NNN
```

11. The trimming procedure creates uncapped backbone pieces. Next use pymol_script.py to add capping hydrogens where bonds were broken when the model was trimmed. Run `pymol_scripts.py` to add hydrogens to one or more `res_NNN.pdb` files:


#####The pymol script file (log.pml) is correct, but it currently doesn't run automatically. Need to manually run log.pml scripts in pymol to add hydrogens###
####How does pymol_scripts read resids if they are in a different chain?! - NJD###

which
- generates a `log.pml` PyMOL input file containing commands that perform the hydrogen addition, and then
- runs PyMOL to perform the addition.
If `-resids` is specified, those residue IDs will not have hydrogens added. NOTE: This is an important part of the process and you will most likely want to put the seed residues in this list. If you don't, pymol might (probably will) reprotonate your noncanonical amino acids/substrate molecules and make very poor decisions. 
```bash
python3 $HOME/git/RINRUS/bin/pymol_scripts.py -resids 300,301,302 -pdbfilename res_.pdb
```

Note-You will have to write a bash or python script to loop over all the models. Example of bash loop is given here.
```bash
ls -lrt| grep -v slurm |awk '{print $9}'|grep -E _atom_info |cut -c 5-6 |cut -d_ -f1>list; mkdir pdbs; for i in `cat list`; do mkdir model-${i}-01; cd model-${i}-01; mv ../res_${i}.pdb .;mv ../res_${i}_atom_info.dat  .;mv ../res_${i}_froz_info.dat .; python3 ~/git/RINRUS/bin/pymol_scripts.py -resids 300,301,302 -pdbfilename *.pdb; cp *_h.pdb model-${i}_h.pdb; cp model-${i}_h.pdb ../pdbs/ ; cd ..; done
```

12. Run `write_input.py` for a single model to generate a template file and input file:
```bash
python3 ~/git/RINRUS/bin/write_input.py -intmp input_template -c -2 -noh res_NN.pdb -adh res_NN_h.pdb
```

## Usage example 2 - generating a single or a few input files with distance-based ranking: 

1. Follow step 1-5 from example 1 to get protonated pdb, in this case we will work with `3bwm.pdb` and after step 2 of example 1 it will generate `3bwm_h.pdb`, if you have modified anything from `3bwm_h.pdb` then use that for following process.

2. For 5 Angstrom from center of mass OR average of xyz cordinate of seed residues A:300,A:301,A:302, and with OR without hydrogen example is given below. Add "-nohydro" to neglact hydrogen if needed, and change seed (Chain:Resid,Chain:Resid) and distance as per requirement in -cut flag.
```bash
python3 ~/git/RINRUS/bin/pdb_dist_rank.py -pdb 3bwm_h.pdb -s A:300,A:301,A:302 -cut 5 -type avg -nohydro
python3 ~/git/RINRUS/bin/pdb_dist_rank.py -pdb 3bwm_h.pdb -s A:300,A:301,A:302 -cut 5 -type avg
python3 ~/git/RINRUS/bin/pdb_dist_rank.py -pdb 3bwm_h.pdb -s A:300,A:301,A:302 -cut 5 -type mass -nohydro
python3 ~/git/RINRUS/bin/pdb_dist_rank.py -pdb 3bwm_h.pdb -s A:300,A:301,A:302 -cut 5 -type mass
```
this will generate a file named `dist_per_res-5.00.dat` which contain information about all residue atoms within 5 Angstrom distance in increasing order. and `res_atom-5.00.dat` which contain information about important atoms to be included in selected residues. 

3. Once the `res_atom-5.00.dat` file generated, use this file to generate the trimmed PDB model using the RINRUSv2 script:
```bash
python3 ~/git/RINRUS/bin/rinrus_trim2_pdb.py -s A:300,A:301,A:302 -pdb 3bwm_h.pdb -c res_atom-5.00.dat 
```
This generates automatically generate the entire "ladder" of possible models based on a ranking scheme which contain `res_NNN.pdb`, `res_NNN_froz_info.dat` and `res_NNN_atom_info.dat` for the all models, where `NNN` is the number of residues in that model.

#Note: if you want to  generate one model based on a any ranking scheme, you will need to run a same script with the flag `-model NNN` as 
```bash
python3 ~/git/RINRUS/bin/rinrus_trim2_pdb.py -s A:300,A:301,A:302 -pdb 3bwm_h.pdb -c res_atom-5.00.dat -model NNN
```

4. follow step 11 and 12 of example 1 to protonate pdb and generate a template file and input file.

## Usage example 3 - generating a single or a few input files with arpeggio interaction-type ranking: 

   Note: Before starting, ensure that the pdb is cleaned. Use step 1 to 7 above to clean your pdb
1. With a clean pdb run 'openbabel/2.4.1' ensure you have openbabel/2.4.1 installed on your terminal 
````bash 
module load openbabel/2.4.1
````
2. Run arpeggio.py script to generate the contact file 
````bash
python3 ~/git/RINRUS/bin/arpeggio/arpeggio.py 2cht_h-TS.pdb
````
3. Use the `arpeggio2rins.py` script to generate: "contact_counts.dat",  "contype_counts.dat" and, "node_info.dat"  
````bash
python3 ~/git/RINRUS/bin/arpeggio2rins.py -f 2cht_h-TS.contacts -s C:202
````
Then you can choose to use either contact_counts or contype_counts to generate model by running:

4. Run the commend below to generate specific model say model 7 
 ```bash
python3 ~/git/RINRUS/bin/rinrus_trim2_pdb.py -pdb 2cht_h-TS.pdb -c contact_counts.dat -s C:202 -model 7
```
If you want to generate all the incremental models use the command above without '-model' flag

5. Run the pymol_script.py to add hydrogens to place where bonds were broken
 ```bash
python3 ~/git/RINRUS/bin/pymol_scripts.py -resids 202 -pdbfilename res_7.pdb 
```
## Note: You can write a bash script to loop over all the models. See an example below
```bash
ls -lrt| grep -v slurm |awk '{print $9}'|grep -E _atom_info |cut -c 5-6 |cut -d_ -f1>list; mkdir pdbs; for i in `cat list`; do mkdir model-${i}-01; cd model-${i}-01; mv ../res_${i}.pdb .;mv ../res_${i}_atom_info.dat  .;mv ../res_${i}_froz_info.dat .; python3 ~/git/RINRUS/bin/pymol_scripts.py -resids 202 -pdbfilename *.pdb; cp *_h.pdb model-${i}_h.pdb; cp model-${i}_h.pdb ../pdbs/ ; cd ..; done
```
7. Run `write_input.py` for a single model to generate a template file and input file:
```bash
python3 ~/git/RINRUS/bin/write_input.py -intmp input_temp -c -2 -noh res_8.pdb -adh res_8_h.pdb -format gaussian
```

## Usage example 4 - generating a single or a few input files with manual ranking (from SAPT, ML, or from some scheme that doesn't yet interface with RINRUS automatically)

## Usage example 5 - GENERATE ALL THE THINGS!!! Combinatorial model building from probe and arpeggio

## Usage example 5a - Combinatorial model building from arpeggio
1. Refer to usage example 3 steps 1 to 3 to generate arpeggio contact files to compute combinations

2. Run combifromcontacts.py script with the defined seed (chain/residue numbers) which takes combinations of the different interactions 
```bash
python3 ~/git/RINRUS/combi_script/combifromcontacts.py 2cht_h.contacts A/203 2cht_h.sift 
```
This generates LongCombi.dat, SimpCombi.dat, and ModSimpCombi.dat

3. Run genmodelfiles.py to remove redundant models ModSimpCombi.dat file
```bash
python3 ~/git/RINRUS/combi_script/genmodelfiles.py ModSimpCombi.dat
```

4. Use res_atoms_*.dat files generated to prepare modified list of models. The res_atoms_*.dat files are then translated   into their corresponding PDB files 
```bash 
ls res_atoms_*.dat > list
```

5. Open the list and remove "res_atoms_" and ".dat" to leave only the model numbers within list, run the command below after you 
```bash
*********rinrus_trim.py needs to be changed******
for i in `cat list`; do python3 ~/git/RINRUS/bin/rinrus_trim_pdb.py -pdb 2cht_h.pdb -s A:203 -ratom res_atoms_${i}.dat; mv res_*_atom_info.dat atom_info_${i}.dat; mv res_*_froz_info.dat froz_info_${i}.dat; mv res_*.pdb model_${i}.pdb; done
```

6. To identify which pdbs are identical, create a new list of the various model pdb names and run the identifiles.py script
```bash
ls model_*.pdb > list
```
```bash
python3 ~/git/RINRUS/combi_script/identifiles.py list
```
The generated file (UniqueModels.dat) lists all the unique models and removes redundant models

7. Complete the valences by adding protons to severed bonds and waters via PyMol
 ```bash 
 for i in `cat list`; do python3 ~/git/RINRUS/bin/pymol_scripts.py ${i} 203; ~qcheng1/bin/pymol -qc log.pml; done
 ```
## Usage example 5b - Combinatorial model building from probe
1. Refer to usage example 1 steps 1 to 7 to generate arpeggio probe files to compute combinations

2. Run gen-probe-combi.py script with the defined seed (chain/residue numbers/atom(s)) which takes combinations of the different interactions 
```bash
python3 ~/git/RINRUS/git/combi_script/gen-probe-combi.py -f 2cht_h_ac_aligned.probe -seed A/203/C1,O1,C2,O2,C3,O3,C4,O4,C5,O5,C6,O7,C8,C9, C10,C11,HO5,H01,H02,H03,H04,H05,H06,H07
```
Note: Multiple seed indices can be indicated by space separation as A/202 A/202 

3. Run the next step which combine multiple step but remember to edit the necessary part

```bash

*********rinrus_trim.py needs to be changed******
ls -lrt| grep -v slurm |awk '{print $9}'|grep -E res_atoms_|cut -c 11-12|cut -d. -f1>list; mkdir pdbs; for i in `cat list`; do mkdir model-${i}-01; cd model-${i}-01; mv ../res_atoms_${i}.dat .; python3 ~/git/RINRUS/bin/rinrus_trim_pdb.py -s A:203 -ratom res_atoms_${i}.dat -pdb ../2cht_h_ac_aligned.pdb; python3 ~/git/RINRUS/bin/pymol_scripts.py -resids 203 -pdbfilename *.pdb; cp *_h.pdb model-${i}_h.pdb; cp model-${i}_h.pdb ../pdbs/; cp res_atoms_${i}.dat ../pdbs/${i}.dat ; cd ..; done
```
Be aware that while the res_atoms_#.dat model sets generated are technically unique to each other, once RINRUS generates the full trimmed QM-models, a lot of the them will no longer be unique and will be identical to others. So there a need to check to determine which QM-models are still unique (and not redundant)
