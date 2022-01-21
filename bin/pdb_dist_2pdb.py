#!/usr/bin/env python3
import os, sys, re
from numpy import *
from read_write_pdb import *
from read_probe import *
from copy import *
import argparse
import operator


def get_model_res(idx_list,freqf,res_atom):
    qf = {}
    j = len(idx_list)
    qf[j] = {}
    for i in idx_list:
        try:
            qf[j][i[0]].append(i[1])
        except:
            qf[j][i[0]] = [i[1]]
    with open(freqf) as f:
        lines = f.readlines()
    sm = len(lines)
    for i in range(j,sm):
        c = lines[i].split()
        Alist = [chr(i) for i in range(ord('A'),ord('Z')+1)]
        if c[0] in Alist:
            cha = c[0]
            res = int(c[1])
            dist = float(c[2])
            if (cha,res) in idx_list: continue
            j += 1
            qf[j] = deepcopy(qf[j-1])
            try:
                qf[j][cha].append(res)
            except:
                qf[j][cha] = [res]
        else:
            cha = ' '
            res = int(c[0])
            dist = float(c[1])
            if (cha,res) in idx_list: continue
            j += 1
            qf[j] = deepcopy(qf[j-1])
            try:
                qf[j][cha].append(res)
            except:
                qf[j][cha] = [res]
        if (cha,res) not in res_atom.keys():
            res_atom[(cha,res)] = []
        for atom in range(3,len(c)):
            res_atom[(cha,res)].append(c[atom])
    return qf, res_atom        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Distance rule based model generator')
    parser.add_argument('-pdb', dest='pdbf', default=None, help='pdb_to_treat')
    parser.add_argument('-cut', dest='coff', default=3, help='cut_off_dist')
    parser.add_argument('-s', dest='seed', default=None, help='center_residues, examples: A:300,A:301,A:302')

    args = parser.parse_args()
    res_atom = {}
    res_name = {}
    res_info = {}
    pdb_res_name = {}
    cres_atom = {}
    nres_atom = {}


    pdbf = args.pdbf
    cut = float(args.coff)
    cres = args.seed
    pdb, tres_info, tot_charge = read_pdb(pdbf)

    res_atom, res_name, res_info, pdb_res_name = get_sel_atoms(pdb,cres,res_atom,res_name,res_info,pdb_res_name)
    sel_key = list(res_name.keys())


    qf, res_atom = get_model_res(sel_key,'dist_per_res-%.2f.dat'%cut,res_atom)
    res_pick = []
    for nm_res in sorted(qf.keys()):
        res_list = qf[nm_res]
        for key in res_list.keys():
            for res in sorted(res_list[key]):
                if (key,res) in sel_key or pdb_res_name[(key,res)] in ['HOH','WAT'] or pdb_res_name[(key,res)][:2] == 'WT':
                    cres_atom[(key,res)] = res_atom[(key,res)]
                else:
                    cres_atom[(key,res)] = get_res_parts(pdb_res_name[(key,res)],res_atom[(key,res)])

        for key in res_list.keys():
            for res in sorted(res_list[key]):
                key1 = (key,res)
                if pdb_res_name[key1] == 'HOH' or pdb_res_name[key1][:2] == 'WT':
                    res_info[key1] = []
                    nres_atom[key1] = cres_atom[key1]
                else:
                    nres_atom, res_info, res_name = check_b(key,res,cres_atom[key1],res_info,nres_atom,res_name,pdb_res_name)
                    nres_atom, res_info = check_s(key,res,cres_atom[key1],res_info,nres_atom)
                    nres_atom, res_info, res_name = check_a(key,res,cres_atom[key1],res_info,nres_atom,res_name,pdb_res_name)
        
        for key in sorted(nres_atom.keys()):
            nres_atom = check_bb(key[0],key[1],nres_atom)

        res_pick = final_pick(pdb,nres_atom,res_info)
        outf = 'dres_%s.pdb'%str(nm_res)
        write_pdb(outf,res_pick)
        
