#!/usr/bin/env python3
import rms
import argparse
from read_write_pdb import *

def main():
    parser = argparse.ArgumentParser(description='calc rmsd')
    parser.add_argument('pdb1')
    parser.add_argument('pdb2')
    parser.add_argument('-H',dest='heavy_only',action='store_true',help='heavy atom only (no hydrogen)')
    parser.add_argument('-F',dest='frozen_only',action='store_true',help='frozen atom only')
    args = parser.parse_args()

    p1 = args.pdb1
    p2 = args.pdb2

    pdb1, res_info1, tot_charge1 = read_pdb(p1)
    pdb2, res_info2, tot_charge2 = read_pdb(p2)

    if args.heavy_only:
        pdb1 = get_heavy(pdb1)
        pdb2 = get_heavy(pdb2)

    if args.frozen_only:
        map1,pdb1 = get_frozen(pdb1)
        map2,pdb2 = get_frozen(pdb2)
#        print(map2)
        if map1 != map2:
            print("The frozen atoms do not match between pdb1 and pdb2!")
#        else:
#            map_p = array(map1)+1
#            print(map_p)

    c1 = get_coord(pdb1)
    c2 = get_coord(pdb2)
#    print(c2)

    rmsd = rms.rmsd(c1,c2)[0]
    print(rmsd)

def get_heavy(pdb):
    new_pdb = []
    for p in pdb:
        if ( p[2].strip()[0] == 'H' ): continue
        new_pdb.append(p)
    return new_pdb

if __name__ == '__main__':
    main()

