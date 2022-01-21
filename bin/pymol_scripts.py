#!/usr/bin/env python3
"""
This is a program written by qianyi cheng in deyonker research group
at university of memphis.
"""
import os, sys
import subprocess


def system_run(cmd):
    print(cmd)
    exit = os.system(cmd)
    if exit != 0:
        print("failed to run:")
        print(cmd)
        sys.exit()


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("pdbfilename", nargs="+")
parser.add_argument("--resids")
args = parser.parse_args()

with open("log.pml", "w") as logf:
    for pdbfilename in args.pdbfilename:
        name = os.path.splitext(pdbfilename)[0]
        outputfilename = f"{name}_h.pdb"
        logf.write(f"load {pdbfilename}\n")
        if args.resids is not None:
            logf.write(
                f'cmd.select("sel","{name} and not resi {args.resids} and not name NH1 and not name NH2")\n'
            )
            logf.write('cmd.h_add("sel")\n')
        else:
            logf.write(f'cmd.h_add("{name}")\n')
        logf.write(f'cmd.save("./{outputfilename}")\n')

cmd = "pymol -qc log.pml"
system_run(cmd)
