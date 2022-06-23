#! /usr/bin/python
import sys, os
import argparse, re

parser = argparse.ArgumentParser(description='generates res_atoms.dat files for probe freq models from freq_per_res.dat and master res_atoms.dat files')
parser.add_argument('-freq', default='freq_per_res.dat', help='freq_per_res.dat file')
parser.add_argument('-atom', default='res_atoms.dat', help='master res_atoms.dat file')
parser.add_argument('-seed', default=None, help='seed selection written in format A:1,A:2,A:3')
args = parser.parse_args()

#Extract atom information
datoms = {}
with open(args.atom, 'r') as atomfile:
    for line in atomfile:
        chain = line.split()[0]
        res = line.split()[1]
        atoms = line.split()[2:]
        datoms[chain+":"+res] = atoms

#Extract freq information
freqorder = []
with open(args.freq, 'r') as freqfile:
    for line in freqfile:
        chain = line.split()[0]
        res = line.split()[1]
        freqorder.append(chain+":"+res)

#Find largest seed index
tres = args.seed.split(',')
start = max([freqorder.index(x) for x in tres])

for i in range(start, len(freqorder)):
    savefile = open("res_atoms_"+str(i)+".dat","w")
    for j in range(0, i+1):
        chain = freqorder[j].split(":")[0]
        res = freqorder[j].split(":")[1]
        info = "  ".join(datoms[freqorder[j]])
        savefile.write(chain+"    "+res+"    "+info+"\n")
    savefile.close()



