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


def qchem_num(lines):
    for i in range(len(lines)):
        if 'Nuclear Repulsion Energy =' in lines[i]:
            natoms = int(lines[i-2].split()[0])
            elel = lines[i+1].split()
            nelectrons = [int(elel[2]),int(elel[5])]
            for j in range(10):
                if "basis functions" in lines[i+j]:
                    nbasis = int(lines[i+j].split()[5])
                    break
            break
    return nbasis, natoms, nelectrons


def qchem_energy(lines):
    for i in range(len(lines)):
        l = lines[i]
        if "This Molecule has" in l:
            nimag = int(l.split()[3])
        if "Zero point vibrational energy"  in l:
            zero = float(l.split()[-2])
        if "Translational Enthalpy" in l:
            tenthalpy = float(l.split()[-2])
        if "Rotational Enthalpy" in l:
            renthalpy = float(l.split()[-2])
        if "Vibrational Enthalpy" in l:
            venthalpy = float(l.split()[-2])
        if "gas constant" in l:
            gas_constant = float(l.split()[-2])
        if "Translational Entropy" in l:
            tentropy = float(l.split()[-2])
        if "Rotational Entropy" in l:
            rentropy = float(l.split()[-2])
        if "Vibrational Entropy" in l:
            ventropy = float(l.split()[-2])
        if "Total Enthalpy" in l:
            tot_enthalpy = float(l.split()[-2])
        if "Total Entropy" in l:
            tot_entropy = float(l.split()[-2])
    return nimag, zero, tenthalpy, renthalpy, venthalpy, gas_constant, tentropy, rentropy, ventropy, tot_enthalpy, tot_entropy   


def qchem_freq(lines,num_atoms):
    f_lines = []
    for i in range(len(lines)):
        if 'Frequency' in lines[i]:
            f_lines.append(i)
    ### Read in imaginary frequency
    freq_xyz  = {}
    freq_info = {}
    keys = []
    for i in range(len(f_lines)):
        start = f_lines[i] - 1
        end = f_lines[i]+6+num_atoms
        modes = lines[start].split()[1:]
        mag   = lines[start+1].split()[1:]
        force = lines[start+2].split()[2:]
        red   = lines[start+3].split()[2:]
        ir_it = lines[start+5].split()[2:]
        for j in range(3):
            key = int(modes[j])
            keys.append(key)
            freq_info[key] = (float(mag[j]),float(red[j]),float(force[j]),float(ir_it[j]))
            freq_xyz[key]  = []
        for j in range(start+8,end+2):
            v = lines[j].split()
            for k in range(3):
                freq_xyz[keys[i*3+k]].append([float(v[3*k+1]),float(v[3*k+2]),float(v[3*k+3])])
                
    return freq_xyz, freq_info

def get_scf(lines):
    scfe = []
    for l in lines:
        if "SCF   energy in the final basis set" in l:
            scfe.append(float(l.split('=')[-1]))
    return scfe

if __name__ == '__main__':
    """ Usage: python3 qchem_fenergy.py output_file """
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    scfe = get_scf(lines)
    nbasis, natoms, nelectrons = qchem_num(lines)
    freq_xyz, freq_info = qchem_freq(lines,natoms)

    temper = 298.15
    nimag, zero, tenthalpy, renthalpy, venthalpy, gas_constant, tentropy, rentropy, ventropy, tot_enthalpy, tot_entropy = qchem_energy(lines) 
    tot_g = tot_enthalpy-tot_entropy*temper/1000
    num_imag = 0
    for key in sorted(freq_info.keys()):
        if freq_info[key][0] < 0:
            num_imag += 1
#    print('SCF energy, zpve, tot_entropy (cal), tot_entralpy (kcal), H-TS, natoms, nbasis, nimag')
    print( "E(RB3LYP)", scfe[-1], scfe[-1]+zero, scfe[-1]+tot_entropy*temper/627.51, scfe[-1]+tot_enthalpy/627.51, scfe[-1]+tot_g/627.51, natoms, nbasis, "NImag", num_imag)#, nimag)
