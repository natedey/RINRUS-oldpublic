#!/usr/bin/env python3
import os, sys, argparse
from read_write_pdb import *

def compu_vec(wpdb, ref1nu, ref1na, ref2nu, ref2na, dist, ref3nu, ref3na):
    ref1x = ref1y = ref1z = None
    ref2x = ref2y = ref2z = None
    ref3x = ref3y = ref3z = None
    for line in wpdb:
        if line[6] == int(ref1nu) and line[2].strip() == ref1na:
            ref1x = line[8]
            ref1y = line[9]
            ref1z = line[10]
        if line[6] == int(ref2nu) and line[2].strip() == ref2na:
            ref2x = line[8]
            ref2y = line[9]
            ref2z = line[10]
        if line[6] == int(ref3nu) and line[2].strip() == ref3na:
            ref3x = line[8]
            ref3y = line[9]
            ref3z = line[10]
    norm = (((ref2x - ref1x)**2) + ((ref2y - ref1y)**2) + ((ref2z - ref1z)**2))**0.5
    vecx = (float(dist) * (ref1x - ref2x) / norm) + ref3x
    vecy = (float(dist) * (ref1y - ref2y) / norm) + ref3y
    vecz = (float(dist) * (ref1z - ref2z) / norm) + ref3z
    return vecx, vecy, vecz

def write_pdb2(filename, wpdb, resnumber, resname, x, y, z):
    for line in wpdb:
        if line[6] == int(resnumber) and line[2].strip() == resname:
            tup = tuple(line[0:8] + [x] + [y] + [z] + line[11:17])
            with open(filename, "a") as savefile:
                savefile.write("%6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f      %-4s%2s%2s%7s\n" %tup) 


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Computes new XYZ coordinates for atoms based on vector distances - Writes Parts and PDB2 files for usage in write_input.py')
    parser.add_argument('-pdb', dest='pdb', default=None, help='reference_pdb_file')
    parser.add_argument('-ops', dest='ops', default='ops.txt', help='operation_file')
    parser.add_argument('-parts', dest='parts', default='parts.txt', help='parts_file_to_write')
    parser.add_argument('-pdb2', dest='pdb2', default='pdb2.pdb', help='pdb2_file_to_write')
    args = parser.parse_args()

    mypdb, res_info, tot_charge = read_pdb(args.pdb)

    if os.path.exists(args.parts):
        os.remove(args.parts)
    if os.path.exists(args.pdb2):
        os.remove(args.pdb2)

    ops = open(args.ops).readlines()

    for oper in ops:
        if oper[0] == "#":
            continue
        ref1number = oper.split()[0]
        ref1name = oper.split()[1]
        ref2number = oper.split()[2]
        ref2name = oper.split()[3]
        opsnumber = oper.split()[4]
        opsname = oper.split()[5]
        dist = oper.split()[6]
        ref3number = oper.split()[7]
        ref3name = oper.split()[8]

        newx, newy, newz = compu_vec(mypdb, ref1number, ref1name, ref2number, ref2name, dist, ref3number, ref3name)
        
        with open(args.parts, "a") as partsfile:
            partsfile.write(str(opsnumber) + " " + opsname + "\n")
        
        write_pdb2(args.pdb2, mypdb, opsnumber, opsname, newx, newy, newz)



