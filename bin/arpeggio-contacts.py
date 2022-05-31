### This is a python script written by Qianyi Cheng for personal use ###
### Simply counts number of interactions between each residue and the seed ###
### It has the option to count or not count proximal ###

from numpy import *
import os, sys, re, argparse
from res_atoms import *

def check_atom(key,atom,dic):
    if key not in dic.keys():
        dic[key] = [atom]
    else:
        if atom not in dic[key]:
            dic[key].append(atom)
    return dic

def de_contacts(contactsf,seed,opt):
    seeds_in = seed.split(',')
    seeds = []
    for sel in seeds_in:
        selstr = sel.replace(':','/')
        selstr = selstr + '/'
        seeds.append(selstr)
    with open(contactsf) as f:
        lines = f.readlines()
    rnames = ['clash','covalent','vdw_clash','vdw','proximal','hbond','weak_hbond','halogen_bond','ionic','metal_complex','aromatic','hydrophobic','carbonyl','polar','weak_polar']
    rinrus = {}
    resinfo = {}

    f1 = open('node_info.dat','w')
    for l in lines:
        v = l.split()
        atom1,atom2 = v[:2]
        rins = v[2:-1]
        inter = v[-1]
        for selstr in seeds:
            seed_length = len(selstr)
            if selstr == atom1[:seed_length] or selstr == atom2[:seed_length]:
                chain1,resid1,aname1 = atom1.split('/')
                chain2,resid2,aname2 = atom2.split('/')
                key1 = (chain1,int(resid1))
                key2 = (chain2,int(resid2))
                rinrus = check_atom(key1,aname1,rinrus)
                rinrus = check_atom(key2,aname2,rinrus)
                if opt == 0:
                    for i in range(15):
                        if rins[i] != '0':
                            try:
                                resinfo[key1].append(1)
                            except:
                                resinfo[key1] = [1]
                            try:
                                resinfo[key2].append(1)
                            except:
                                resinfo[key2] = [1]
                            f1.write('%s %s %s %s\n'%(atom1,atom2,rnames[i],inter))
                else:
                    for i in range(15):
                        if i == 4: 
                            if rins[i] != '0':
                                try:
                                    resinfo[key1].append(0)
                                except:
                                    resinfo[key1] = [0]
                                try:
                                    resinfo[key2].append(0)
                                except:
                                    resinfo[key2] = [0]
                        else:
                            if rins[i] != '0':
                                try:
                                    resinfo[key1].append(1)
                                except:
                                    resinfo[key1] = [1]
                                try:
                                    resinfo[key2].append(1)
                                except:
                                    resinfo[key2] = [1]
                                f1.write('%s %s %s %s\n'%(atom1,atom2,rnames[i],inter))

    f2 = open('res_atom.dat','w')
    f3 = open('contact_counts.dat','w')
    for key in sorted(rinrus.keys()):
        f2.write('%4s %6d '%(key[0],key[1]))
        for i in rinrus[key]:
            f2.write('%6s '%i)
        f2.write('\n')
        #print(key,rinrus[key],sum(resinfo[key]))
        f3.write('%4d'%sum(resinfo[key]))
        for it in key:
            f3.write('%5s'%it)
        for it in rinrus[key]:
            f3.write('%6s'%it)
        f3.write('\n')
    f1.close()
    f2.close()
    f3.close()

if __name__ == '__main__':

    ################################################################################
    ### python3 arpeggio-contacts.py -c 2cht_h-TS.contacts -s A:202 -p 1 ###
    ################################################################################

    parser = argparse.ArgumentParser(description='Get contact information from Arpeggio output')
    parser.add_argument('-p', dest='opt', default=0, type=int, help='ignor proximal or not')
    parser.add_argument('-c', dest='cf', help='Arpeggio contact output file')
    parser.add_argument('-s', dest='seed', help='Seed residues, in the format A:601,A:602')

    args = parser.parse_args()
    opt = args.opt
    cf = args.cf
    seed = args.seed

    if opt == 0:
        de_contacts(cf,seed,0)        
    elif opt == 1:
        de_contacts(cf,seed,1)
    else:
        print("If you want to ignor proximal please add '-p 1' when running the script!")

