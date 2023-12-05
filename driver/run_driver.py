import os, sys, re, argparse

def system_run(cmd):
    print(cmd)
    exit = os.system(cmd)
    if ( exit != 0 ):
        print('failed to run:')
        print(cmd)
        sys.exit()
 
### Environment setup, need to have env.yml file ###
system_run( 'source activate rinrus')

### Read user input driver information including PDB file, seed, ranking scheme, models for 1 or all, program to run calculations ###
### Check PDB file and user provided seed information, need to run reduce or not ###
### Use probe/arpeggio/sapt/distance to get RIN and residue ranking ###
### Trim PDB, generate one or all trimmed models ###
### Add H to trimmed models ###
### Generate input file for running calculations (may need more specific information) ###
