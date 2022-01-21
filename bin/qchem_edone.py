#!/usr/bin/env python3
"""
This is a program written by Qianyi Cheng
at University of Memphis.
"""

from rms import *
from numpy import *
import sys, re, os
from read_write_pdb import *
from sys_tools import *
import argparse

def get_opt_cycle(lines):
    eline   = []
    cycline = []
    conline = []
    for i in range(len(lines)):
        if "Optimization Cycle" in lines[i]:
            cycline.append(i)
            #cyc.append(int(l.split()[-1]))
        if "Energy is" in lines[i]:
            eline.append(i)
            #scfe.append(float(l.split()[2]))
        if "Cnvgd?" in lines[i]:
            conline.append(i)
    for i in range(len(cycline)):
        print(lines[cycline[i]][:-1])
        if i <= len(eline):
            print(lines[eline[i]][:-1])
        if i <= len(conline):
            for j in range(3):
                print(lines[conline[i]+j+1][:-1])


if __name__ == '__main__':
    """ Usage: python3 qchem_edone.py output_file """
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    get_opt_cycle(lines)

