#!/usr/bin/env python3
"""
This is a program written by Qianyi Cheng 
at university of memphis.
"""
from numpy import *
import os, sys, re, argparse
from res_atoms import *

def get_fg_sapt(fgfile):
    with open(fgfile,'r') as f:
        lines = f.readlines()

    res_list = {}
    for i in range(1,len(lines)):
        v = lines[i].split()
        key = v[0]
        res_list[key] = []
        for value in v[1:]:
            res_list[key].append(float(value))
    return res_list

#res_list = get_fg_sapt('/home/qcheng1/projects/gnmt/sapt-rank/fsapt/gly/FG-SAPT.dat')

def gen_res_atom(res_list,old_res_atom):
    new_res_list = sorted(res_list.items(),key=lambda x:abs(x[1][-1]),reverse=True)
    with open(old_res_atom,'r') as f:
        lines = f.readlines()
    res_part = []
    for i in new_res_list:
        res_part.append(i[0])
    
    key_list = []
    res_atom = []
    for key in res_part:
        chain, res_id, part = key.split(':')
        if part == 'SC':
            if (chain,res_id) not in key_list:
                key_list.append((chain,res_id))
                res_atom.append(['CB'])
            else:
                atom_list = res_atom[key_list.index((chain,res_id))]
                atom_list.append('CB')
                res_atom.append(atom_list)
                key_list.append((chain,res_id))
        elif part == 'MC':
            if (chain,res_id) not in key_list:
                key_list.append((chain,res_id))
                atom_list = []
                for line in lines:
                    v = line.split()
                    if v[0] == chain and v[1] == res_id:
                        for value in v[3:]:
                            if value in ['CA','N','C','O','HA']:
                                atom_list.append(value)
                            else:
                                atom_list.append('CA')
                res_atom.append(atom_list)
            else:
                idx = key_list.index((chain,res_id))
                atom_list = res_atom[idx]
                for line in lines:
                    v = line.split()
                    if v[0] == chain and v[1] == res_id:
                        for value in v[3:]:
                            if value in ['CA','N','C','O','HA']:
                                atom_list.append(value)
                            else:
                                atom_list.append('CA')
                res_atom.append(atom_list)
                key_list.append((chain,res_id))
    return res_part, key_list, res_atom

#res_part, key_list, res_atom = gen_res_atom(res_list,'/home/qcheng1/projects/gnmt/arpeggio/sam-gly/contact_counts.dat')

def write_res_atom(res_list,res_part,key_list,res_atom,seed):
    f = open('res_atoms-fsapt.dat','w')
    seeds_in = seed.split(',')
    seeds = []
    for sel in seeds_in:
        v = sel.split(':')
        seeds.append((v[0],v[1]))
    for sd in seeds:
        if sd not in key_list:
            f.write('%8s%8s\n'%(sd[0],sd[1]))
            idx = len(res_part)+1
        else:
            idx = key_list.index(sd)
            f.write('%8s%8s'%(key_list[idx][0],key_list[idx][1]))
            f.write('%12.3f'%res_list[res_part[idx]][-1])
            for atom in res_atom[idx]:
                f.write('%6s'%atom)
            f.write('\n')
    #print(idx)
    for i in range(len(res_part)):
        if i != idx:
            f.write('%8s%8s'%(key_list[i][0],key_list[i][1]))
            f.write('%12.3f'%res_list[res_part[i]][-1])
            for atom in res_atom[i]:
                f.write('%6s'%atom)
            f.write('\n')
    f.close()

if __name__ == '__main__':
    ################################################################################
    ### python3 sapt2rin.py -f FG-sapt.dat -c contact_counts.dat
    ################################################################################

    parser = argparse.ArgumentParser(description='Get contact information from SAPT energy')
    parser.add_argument('-p', dest='fg',help='FG-sapt energy dat')
    parser.add_argument('-c', dest='cf',help='contact data from other programs')
    parser.add_argument('-s', dest='seed',help='seed residues, in the format "A:293,A;294"')

    args = parser.parse_args()
    fg_file = args.fg
    ct_file = args.cf
    seed = args.seed
    
    res_list = get_fg_sapt(fg_file)
    res_part, key_list, res_atom = gen_res_atom(res_list,ct_file)


    write_res_atom(res_list,res_part,key_list,res_atom,seed)
