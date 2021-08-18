import os, sys, re
from read_write_pdb import *
from probe2rins import *

# reading inputs
model_fname = sys.argv[1]
probe_fname = sys.argv[2]
pdb_fname = sys.argv[3]

# read residues from the model_detail file
model_info = open(model_fname, 'r')
# generate dictionary containing lists of 
# the residues contained in each N residue model:
# {'N': 'Chain:Res1,Chain:Res2...'}
pdb_idx = None
res_dict = {}
for line in model_info.readlines():
    # corresponding PDB model number
    if("residue model" in line):
        pdb_idx = line.split(" ")[0]
        res_dict[pdb_idx] = ''
    # extract list of residues
    if("Chain" in line):
        a = line.split(",")
        m = re.search('Chain (.)', a[0])
        chain = ''
        if m:
            chain = m.group(1)
        res_list = a[1].lstrip().rstrip().split(" ")
        for i in res_list:
            if(res_dict[pdb_idx] != ''):
                res_dict[pdb_idx] += (",")
            res_dict[pdb_idx] += ("%s:%s" %(chain, i))
model_info.close()

# read in the PDB
pdb_list, res_count, tot_charge = read_pdb(pdb_fname)

# obtain a list of relevant resids for the set
for key in res_dict:
    # get interacting residues
    print("Generating for No.", key)
    res_list = res_dict[key].split(",") # list of explicitly-modeled residues
    # obtain list of interacting residues from probe file
    probe_result = probe_analysis(probe_fname, res_dict[key])
    env_res_list = probe_result[0] # list of interacting residue numbers
    res_acts = probe_result[1] # dict of interaction types per residue
    # get relevant residues from pdb file
    pdb_out_list = []
    for res in pdb_list:
        res_str = str(res[5]) + ":" + str(res[6])
        if(res_str in env_res_list):
            if(res_str not in res_list):
                pdb_out_list.append(res)
    # write gathered residuals list to new pdb
    write_pdb('res_%s_elastic.pdb' % str(key), pdb_out_list)
        



