"""
This is a program written by qianyi cheng in deyonker research group
at university of memphis.
Version 1.2 
Read in residue atom information for trimming pdb
Date 6.25.2020
"""
import os, sys, re
from read_write_pdb import *
from copy import *
from check_residue_atom import *
import argparse

######################################   Example   #############################################################
### python3 rinrus_trim_pdb.py -pdb 3bwm_h_mg.ent -s A:300,A:301,A:302 -ratom res_atoms.dat -cres cres_atom.dat


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Trim large PDB file according to res_atoms.dat, write trimmed pdb in working directory')
    parser.add_argument('-pdb', dest='r_pdb', default='None', help='protonated pdbfile')
    parser.add_argument('-s', dest='seed', default='None', help='Chain:Resid,Chain:Resid')
    parser.add_argument('-ratom', dest='r_atom', default='res_atoms.dat', help='atom info for each residue')
    parser.add_argument('-cres', dest='cres', default='None', help='Noncanonical residue information')

    args = parser.parse_args()

    r_pdb = args.r_pdb
    seed  = args.seed
    atomf = args.r_atom
    cres  = args.cres
    if cres is not 'None':
        cres_atoms_all, cres_atoms_sc = get_noncanonical_resinfo(cres)
    else:
        cres_atoms_all = {}
        cres_atoms_sc = {}
    pdb, tres_info, ttot_charge = read_pdb(r_pdb)
    sel_key = get_sel_keys(seed)
    with open(atomf) as f:
        iratoms = f.readlines()

    res_atom = {}   # Residue atoms
    res_info = {}   # Freeze idx for residues

    pdb_res_name = {}
    pdb_res_atom = {}
    for line in pdb:
        key = (line[5],line[6])
        if key not in pdb_res_name.keys():
            pdb_res_name[key] = line[4].strip()
            pdb_res_atom[key] = [line[2].strip()]
        else:
            pdb_res_atom[key].append(line[2].strip())

    ### get res_atom info ###
    res_part_list = {}
    cha_res_list = {}
    Alist = [chr(i) for i in range(ord('A'),ord('Z')+1)]
    sm = len(iratoms)
    
    for i in range(sm):
        c = iratoms[i].split()
        if c[0] in Alist:
            cha = c[0]
            res_id = int(c[1])
            st = 2
        else:
            cha = ' '
            res_id = int(c[0])
            st = 1
        if cha not in res_part_list.keys(): #res_part_list[key1=chainID]={[key2=resid]:[atoms]}
            res_part_list[cha] = {}     #res_part_list[key1=chainID][key2=resid]=[atoms]
            res_part_list[cha][res_id] = []
            cha_res_list[cha] = [res_id]      #cha_res_list[cha]=[res_list]
        else: 
            res_part_list[cha][res_id] = [] 
            cha_res_list[cha].append(res_id)
        res_part_list[cha][res_id] = []
        for j in range(st,len(c)):
            res_part_list[cha][res_id].append(c[j])
    ### check residue atoms itself according to pdb file ###
    for cha in res_part_list.keys():
        for res_id in sorted(res_part_list[cha].keys()):
            key = (cha,res_id)
            if key in sel_key or pdb_res_name[key] in ('HOH', 'WAT','O'):
                res_part_list[cha][res_id] = pdb_res_atom[key]
                res_atom[key] = deepcopy(res_part_list[cha][res_id])
                res_info[key] = []
            else:
                value_list = deepcopy(res_part_list[cha][res_id])
                res_atom[key] = check_sc(pdb_res_name[key],value_list,cres_atoms_sc)
#                res_part_list[cha][res_id] = check_sc(pdb_res_name[key],res_part_list[cha][res_id],cres_atoms_sc)
                if not bool(set(res_atom[key])&set(['N','CA','C','O','H','HA','HA2','HA3'])) and 'CB' in res_atom[key]:
                    res_info[key] = ['CA','CB']
                    res_atom[key].append('CA')
                else:
                    res_info[key] = ['CA']
                    res_atom[key] = check_mc(pdb_res_name[key],res_atom[key])
    for cha in res_part_list.keys():
        for res_id in sorted(res_part_list[cha].keys()):
            key = (cha,res_id)
            if key not in sel_key and pdb_res_name[key] not in ('HOH', 'WAT','O'):
            ### Check one residue before according to "N and H" ###    
                #if bool(set(res_atom[key])&set(['N','H'])):
                if bool(set(res_atom[key])&set(['N','H'])) and (cha,res_id-1) in pdb_res_name.keys():
                    if (cha,res_id-1) not in res_atom.keys():
                        res_atom[(cha,res_id-1)] = ['CA','C','O','HA','HA2','HA3']
                    else:
                        for atom in ['CA','C','O','HA','HA2','HA3']:
                            if atom not in res_atom[(cha,res_id-1)]:
                                res_atom[(cha,res_id-1)].append(atom)
            ### Check one residue after according to "C and O" ###    
                #if bool(set(res_atom[key])&set(['C','O'])):
                if bool(set(res_atom[key])&set(['C','O'])) and (cha, res_id+1) in pdb_res_name.keys():
                    if (cha,res_id+1) not in res_atom.keys():
                        res_atom[(cha,res_id+1)] = ['CA','HA','HA2','HA3','N','H']
                    else:
                        for atom in ['CA','HA','HA2','HA3','N','H']:
                            if atom not in res_atom[(cha,res_id+1)]:
                                res_atom[(cha,res_id+1)].append(atom)

    ### Check one "CACA" ###    
    for key in sorted(res_atom.keys()):
        if key not in sel_key and pdb_res_name[key] not in ('HOH', 'WAT','O'):
            cha = key[0]
            res_id = key[1]
            if 'CA' in res_atom[key]:
                for atom in ['HA','HA2','HA3']:
                    if atom not in res_atom[key]:
                        res_atom[key].append(atom)
                if (cha,res_id+1) in res_atom.keys() and 'CA' in res_atom[(cha,res_id+1)]:
                    for atom in ['C','O']:
                        if atom not in res_atom[key]:
                            res_atom[key].append(atom)
                    for atom in ['N','H']:
                        if atom not in res_atom[(cha,res_id+1)]:
                            res_atom[(cha,res_id+1)].append(atom)

    ### Check frozen info ###
    for key in sorted(res_atom.keys()):
        if key not in res_info.keys():
            res_info[key] = ['CA']
#    for key in sorted(res_atom.keys()):
#        if 'CB' in res_info[key]: 
#            chainid, resid = key 
#            if (chainid,resid+1) in res_info.keys() or (chainid,resid+1) in res_info.keys():
#                res_info[key].pop('CB')

    res_num = len(res_atom.keys())
    res_pick,res_info = final_pick2(pdb,res_atom,res_info,sel_key)
    f1 = open('res_%s_atom_info.dat'%str(res_num),'w')        
    f2 = open('res_%s_froz_info.dat'%str(res_num),'w')        
    for key in sorted(res_atom.keys()):
        f1.write('%2s %5d '%(key[0],key[1]))
        f2.write('%2s %5d '%(key[0],key[1]))
        for atom in res_atom[key]:
            f1.write('%4s '%atom)
        f1.write('\n')
        for freeze in res_info[key]:
            f2.write('%4s '%freeze)
        f2.write('\n')
    f1.close()
    f2.close()

    outf = 'res_%s.pdb'%str(res_num)
    write_pdb(outf,res_pick)
