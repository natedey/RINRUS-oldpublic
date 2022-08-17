#!/usr/bin/env python3
import sys, os, re
from read_write_pdb import *
from numpy import *
from itertools import *

def compare_2(idx1,idx2,pdb1,pdb2):
        heavy = 0
        count = 0
        for i in range(len(pdb1)):
            if 'H' not in pdb1[i][2]:
                heavy += 1
                if pdb1[i][2] == pdb2[i][2]:
                    count += 1
        if heavy == count:
            print("%s and %s probably are the same, please double check!"%(idx1,idx2))


if __name__ == '__main__':
    files = []
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    pdb_key = []
    pdb_dic = []
    pdb_res = []
    pdb_chg = []
    for i in range(len(lines)):
        pdb_key.append(lines[i].strip())
        f = '%s/template.pdb'%lines[i].strip()
        pdb, res_info, tot_charge_t = read_pdb(f)
        pdb_dic.append(pdb)
        pdb_res.append(res_info)
        pdb_chg.append(tot_charge_t)
    
    pdb_len = []
    for i in range(len(lines)):
        pdb_len.append(len(pdb_dic[i]))

    overlap = list(set([x for x in pdb_len if pdb_len.count(x) > 1]))    
    pdb_len = array(pdb_len)
    for i in range(len(overlap)):
        idx = where(pdb_len==overlap[i])[0]
        for pair in combinations(idx,2):
            compare_2(pdb_key[pair[0]],pdb_key[pair[1]],pdb_dic[pair[0]],pdb_dic[pair[1]])
