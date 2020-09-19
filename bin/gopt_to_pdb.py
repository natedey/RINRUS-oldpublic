"""
This is a program written by Qianyi Cheng
at University of Memphis.
"""

from rms import *
from numpy import *
import sys, re, os
from read_write_pdb import *
import argparse
from read_gout import *

if __name__ == '__main__':
    """ Usage: gopt_to_pdb.py -o ../1.out -p ../template.pdb """
    parser = argparse.ArgumentParser(description='generate pdbfiles from 1.out')
    parser.add_argument('-o', dest='output',default='../1.out',help='output file')
    parser.add_argument('-p', dest='pdbf',default='../template.pdb',help='template pdb file')
    parser.add_argument('-f', dest='frame',default=None,help='select frame/range')


    args = parser.parse_args()
    pdbf = args.pdbf
    output = args.output

    pdb, res_info, tot_charge = read_pdb(pdbf)
#    map, xyz_i = get_ca(pdb)
    map, xyz_i = get_fatom(pdb)
    
    natoms = len(pdb)
    
    with open(output) as f:
        lines = f.readlines()
    rot_opt = gaussian_opt_xyz(lines,natoms)
    if args.frame is None:
        for key in range(len(rot_opt)):
            xyz_c = array(rot_opt[key])
            (c_trans,U,ref_trans) = rms_fit(xyz_i,xyz_c[map])
            xyz_n = dot( xyz_c-c_trans, U ) + ref_trans
            sel_atom = update_xyz(pdb,xyz_n)
            name = str(key)+'.pdb'
            write_pdb(name,sel_atom)
    elif args.frame == '-1':
        key = -1
        xyz_c = array(rot_opt[key])
        (c_trans,U,ref_trans) = rms_fit(xyz_i,xyz_c[map])
        xyz_n = dot( xyz_c-c_trans, U ) + ref_trans
        sel_atom = update_xyz(pdb,xyz_n)
        name = str(len(rot_opt)-1)+'.pdb'
        write_pdb(name,sel_atom)
    else:
        print("The frame is not clear!")
        sys.exit()
