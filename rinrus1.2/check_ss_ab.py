"""
This is a program written by Qianyi Cheng in DeYonker Research Group
at University of Memphis.
Version 1.1
"""

import sys, os, re
from numpy import *
from res_atoms import *

def get_sel_keys(seed_list):  
    seeds = seed_list.split(',')
    sel_keys = []
    for seed in seeds:
        res_id = seed.split(':')
        sel_keys.append((res_id[0],int(res_id[1])))
    sel_keys.sort(key = lambda x: x[1]) #by res id
    sel_keys.sort(key = lambda x: x[0]) #by chain id
    return sel_keys

def check_mc(res,value):
    case1 = ['N','H']
    case2 = ['C','O']
    case3 = ['N','CA','C','O','H','HA','HA2','HA3']
    case4 = ['CA','HA','HA2','HA3']
    ### if res name is PRO, then include entire residue ###
    if res == 'PRO':
        value = res_atoms_all[res]

    if bool(set(value)&set(case1)) and 'C' not in value and 'O' not in value:
        for i in ['N','CA','H','HA','HA2','HA3']:
            if i not in value:
                value.append(i)
    elif bool(set(value)&set(case2)) and 'N' not in value and 'H' not in value:
        for i in ['CA','C','O','HA','HA2','HA3']:
            if i not in value:
                value.append(i)
    elif 'N' not in value and 'H' not in value and 'C' not in value and 'O' not in value:
        for i in ['CA','HA','HA2','HA3']:
            if i not in value:
                value.append(i)
    elif bool(set(value)&set(case1)) and bool(set(value)&set(case2)):
        for i in case3:
            if i not in value:
                value.append(i)
    else:
        for i in case3:
            value.append(i)
    return value

def check_sc(res,value,cres_atoms_sc):
    if res in res_atoms_sc.keys():
        if bool(set(value)&set(res_atoms_sc[res])):
            for i in res_atoms_sc[res]:
                if i not in value:
                    value.append(i)
    elif res in cres_atoms_sc.keys():
        if bool(set(value)&set(cres_atoms_sc[res])):
            for i in cres_atoms_sc[res]:
                if i not in value:
                    value.append(i)
    else:   
        print("Residue %s is either canonical or nocanonical, please check!"%res)
    return value

def final_check_mc(chain,id,res_atom):
    case1 = ['N','H','HA','HA2','HA3']
    case2 = ['C','O','HA','HA2','HA3']
    case3 = ['CA','C','O','H','HA','HA2','HA3']
    
    if (chain,id-1) in res_atom.keys():
        if 'CA' in res_atom[(chain,id)] and 'C' in res_atom[(chain,id-1)]:
            for i in case1:
                if i not in res_atom[(chain,id)]:
                    res_atom[(chain,id)].append(i)
    if (chain,id+1) in res_atom.keys():
        if 'CA' in res_atom[(chain,id)] and 'N' in res_atom[(chain,id+1)]:
            for i in case2:
                if i not in res_atom[(chain,id)]:
                    res_atom[(chain,id)].append(i)
    if 'CA' in res_atom[(chain,id)] and not bool(set(res_atom[(chain,id)])&set(['N','C','O','CB'])):
        if 'CA' in res_atom[(chain,id+1)]:
            for i in case3:
                if i not in res_atom[(chain,id)]:
                    res_atom[(chain,id)].append(i)
            for i in case1:
                if i not in res_atom[(chain,id+1)]:
                    res_atom[(chain,id+1)].append(i)
    return res_atom

### check self ###
def check_s(chain,id,atom,res_info,res_atom):
    if (chain,id) in res_atom.keys() and (chain,id) not in res_info.keys():
        res_info[(chain,id)] = []
    
    if 'CA' in atom:
        if 'CA' not in res_info[(chain,id)]:
            res_info[(chain,id)].append('CA')
            if 'CB' in atom and not bool(set(['C','O','N'])&set(atom)):
                if 'CB' not in res_info[(chain,id)]:
                    res_info[(chain,id)].append('CB')
    elif 'CA' not in atom and 'CB' in atom:
        res_atom[(chain,id)].append('CA')
        if (chain,id) in res_info.keys():
            if 'CA' not in res_info[(chain,id)]:
                res_info[(chain,id)].append('CA')
            if 'CB' not in res_info[(chain,id)]:
                res_info[(chain,id)].append('CB')
        else:
            res_info[(chain,id)] = ['CA','CB']
    else:
        print('Both CA and CB are not in %d atom list!'%id)
    return res_atom, res_info

### check one residue after ### 
def check_a(chain,id,atom,res_info,res_atom):
    if 'C' in atom:
        if (chain,id+1) not in res_atom.keys(): 
            res_atom[(chain,id+1)] = ['N','CA']
        else:
            if 'N' not in res_atom[(chain,id+1)]:
                res_atom[(chain,id+1)].append('N')
            if 'CA' not in res_atom[(chain,id+1)]:
                res_atom[(chain,id+1)].append('CA')
        if (chain,id+1) not in res_info.keys():
            res_info[(chain,id+1)] = ['CA']
        else:
            if 'CA' not in res_info[(chain,id-1)]:
                res_info[(chain,id+1)].append('CA')
    return res_atom, res_info

### check one residue before ###
def check_b(chain,id,atom,res_info,res_atom):
    if 'N' in atom:
        if (chain,id-1) not in res_atom.keys():
            res_atom[(chain,id-1)] = ['CA','C','O']
        else:
            if 'CA' not in res_atom[(chain,id-1)]:
                res_atom[(chain,id-1)].append('CA')
            if 'C' not in res_atom[(chain,id-1)]:
                res_atom[(chain,id-1)].append('C')
            if 'O' not in res_atom[(chain,id-1)]:
                res_atom[(chain,id-1)].append('O')
        if (chain,id-1) not in res_info.keys():
            res_info[(chain,id-1)] = ['CA']
        else:
            if 'CA' not in res_info[(chain,id-1)]:
                res_info[(chain,id-1)].append('CA')
    return res_atom, res_info


def check_bb(chain,id,res_atom):
    if 'CA' in res_atom[(chain,id)]:
        if (chain,id-1) in res_atom.keys() and 'CA' in res_atom[(chain,id-1)]:
            if 'N' not in res_atom[(chain,id)]:
                res_atom[(chain,id)].append('N') 
            if 'H' not in res_atom[(chain,id)]:
                res_atom[(chain,id)].append('H') 
        if (chain,id+1) in res_atom.keys() and 'CA' in res_atom[(chain,id+1)]:
            if 'C' not in res_atom[(chain,id)]:
                res_atom[(chain,id)].append('C')
            if 'O' not in res_atom[(chain,id)]:
                res_atom[(chain,id)].append('O')
    return res_atom

def final_pick(pdb,nres_atom,nres_info,sel_key):
    list_cb = ['ARG','LYS','GLU','GLN','MET','TRP','TYR','PHE']
    res_pick = []
    for line in pdb:
        key = (line[5],line[6])
        if key in nres_atom.keys():
            if key in sel_key:
                res_pick.append( [line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],' 0'] )
            elif line[2].strip() in nres_atom[(line[5],line[6])]:
                if line[2].strip() in nres_info[key]:
                    res_pick.append( [line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],'-1'] )
                else:
                    res_pick.append( [line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],' 0'] )
            else:
                continue
    return res_pick

def get_noncanonical_resinfo(cres):
    with open(cres) as f:
        lines = f.readlines()
    cres_atoms_all = {}
    cres_atoms_sc = {}
    for i in range(len(lines)):
        c = lines[i].split()
        if c[0] not in cres_atoms_all.keys():
            cres_atoms_all[c[0]] = []
            for j in range(1,len(c)):
                cres_atoms_all[c[0]].append(c[j])
        else:
            if c[0] not in cres_atoms_sc.keys():
                cres_atoms_sc[c[0]] = []
                for j in range(1,len(c)):
                    cres_atoms_sc[c[0]].append(c[j])
    return cres_atoms_all, cres_atoms_sc

