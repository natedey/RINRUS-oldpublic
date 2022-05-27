#! /usr/bin/env python
import sys, argparse, re
from collections import defaultdict

parser = argparse.ArgumentParser(description='Translate model combinatorics datafile of Arpeggio interactions into files for generating PDB models')
parser.add_argument('datafile', help='name of the datafile to build from')
args = parser.parse_args()

with open(args.datafile, "r") as data:
    counter = 1
    for line in data:
        resatoms = defaultdict(list)
        for atom in line.split("|",1)[0].split(","):
            res = atom.rsplit("/",1)[0]
            resatoms[res].append(atom.rsplit("/",1)[1])
        sortres = sorted(resatoms.keys(), key=lambda x: int(re.search(r'\d+$',x).group()))
        genfilename = "res_atoms_" + str(counter) + ".dat"
        genfile = open(genfilename, "w")
        for res in sortres:
            s = '{:4} {:8} '+' '.join(['{:4}']*len(resatoms[res]))+"\n"
            d = [res.split("/")[0], res.split("/")[1]]+resatoms[res]
            genfile.write(s.format(*d))
            #genfile.write("\t".join([res.split("/")[0], res.split("/")[1]] + resatoms[res]) + "\n")
        genfile.close()
        counter+=1

        
