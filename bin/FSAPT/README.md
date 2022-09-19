Background: The user has a cluster model PDB file that has already been 
cleaned/trimmed/protonated. A Psi4 FSAPT computation has been run on this 
PDB structure wherein the species of interest (e.g. the chorismate of 
chorismate mutase) is listed as the first interacting body and the enzyme
is the second interacting body. The atom ordering of the first body is 
in the same order as in the PDB file, and the atom ordering of the second 
body is in the same order as in the PDB file, but the overall atom 
indices do not need to be the same (e.g. it is okay that the chorismate 
is listed as the first body in the FSAPT calculation, but it does not 
appear first in the PDB file, as long as the order of the chorismate 
atoms is the same and the order of the rest of the enzyme atoms is the 
same). NOTE: If there is more than one seed fragment, the fragments must be in the
same order in the first body as they are in the pdb, even if they are noncontiguous 
fragments. The user wishes to automate the process of identifying the unique 
side/main chains and waters present in the cluster model and computing 
the FSAPT interaction between the first body and each of these functional 
groups.
Example using chorismate and chorismate mutase in path: /home/tsmmers1/chem/chorismate_mutase/SAPT/MD/f10000

1) Identify functional group atoms
-	The gen-FG-analysis.py script is a rudimentary script that can be used 
to identify which atoms of the cluster model PDB correspond to residue main 
chains, residue side chains, and waters. Because the atom indices between 
the PDB and the FSAPT computation may be different (e.g. with chorismate 
it is located in the middle of the PDB ordering but as the first body in 
the FSAPT calculation) the atom indices printed in the outputfile will be 
shifted according to the expected atom indices in the FSAPT calculation. 
Example script usage:
o	python3 gen-FG-atomIDs.py -p res_17_h.pdb -s A:128
	output: pdbFG.dat

-	The output pdbFG.dat file contains info on: how many atoms are in 
the structure (line 1), the atom names of the first body (line 2), and the 
names and corresponding shifted atom indices for the functional groups 
identified by the script (for example, the side chain of residue 7 of 
chain A would correspond to atoms 25-46 in the geom.xyz script generated 
by the FSAPT calculation in the fsapt directory for this computation).

2) Calculate all of the functional group atom interactions with the first body
-	Now that the atom indices of the functional groups have been 
identified and summarized in the generated pdbFG.dat file, we can 
automate the calculation of their interaction energies with the 
first body using the analyze-FG-SAPT.py script. The script needs 
to be run within the fsapt directory output by the FSAPT computation 
in the computation's scratch directory as this directory contains the 
data files required for calculating the energies among the user-specified 
functional groups/partitions. Assuming that the pdbFG.dat file is located 
in the directory before the fsapt directory (this location can be changed 
with the flag -p ) the script can be run as-is. 
o	What the script does is uses the information within pdbFG.dat to 
generate file fA.dat, which contains the functional group information for 
the first body (by default using the whole first body [i.e. the whole 
chorismate], though this can be changed to indicate only a particular 
functional group of the first body [i.e. only one of the carboxylates] 
using the -a flag), and then file fB.dat, which contains the functional 
group information for the second body. The script will begin by setting 
fB.dat to the first functional group (specifically the enzyA within 
fB.dat will correspond to the atom indices of the first functional group 
and enzyB will correspond to the atom indices of the rest of the enzyme 
of the second body). The Psi4 fsapt.py script will then be automatically 
executed to calculate the FSAPT interaction energies, and then the 
specific interactions between the two bodies of interest (specifically 
enzyA of fB.dat and seedA of fA.dat) will be saved. The fB.dat file is 
then re-written using the next functional group in the pdbFG.dat file 
as the next enzyA functional group, and the process is repeated until 
all of the functional groups interaction energies has been computed. 
Example usage (within the fsapt directory):
	python3 ../analyze-FG-SAPT.py
	output: ../FG-SAPT.dat

3) (Additional) Gather probe counts and arpeggio interactions for functional group atoms
The gen-FG-analysis-probe.py script counts the contacts for 
the functional groups interacting with a user-specified seed. Requires 
a probe file to have been run on the PDB. 
Example usage:
o	python3 gen-FG-analysis-probe.py -p 2cht.10000.probe -s A:128
	output: FG-probe.dat which lists the functional groups and the number of contacts with the seed

The gen-FG-analysis-arpeggio.py script counts the interactions for 
the functional groups interacting with a user-specified seed. 
Requires an arpeggio contacts file to have been run on the cluster PDB. 
Example usage:
o	python3 gen-FG-analysis-arpeggio.py -c res_17_h.contacts -p res_17_h.pdb -s A/128
	output: FG-arpeggio.dat which lists the functional groups and the 
	number of given interaction types. The order of the interaction 
	types column is the same as in the contacts file, which can be found in the README of Arpeggio

The sapt2rins.py script generates the res_atoms.dat, which then allows you to create models for quantum chemistry software packages (step 9 of the original workflow)

Example usage:
o	python3 sapt2rins.py -p ../FG-SAPT.dat -c ../contact_counts.dat -s A:293,A:294 

