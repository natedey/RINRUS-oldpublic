#!/usr/bin/env python
import os, sys
import argparse, itertools
from collections import defaultdict

parser = argparse.ArgumentParser(description="Generate a series of files containing model atom information based upon taking combinations of different probe contacts")
parser.add_argument("-f", help="Input probe file")
parser.add_argument("-seed", nargs="+", help="Specify the seed residue(s)/atom(s) in the format chain/index/atom(s). Specifying only chain/index (e.g. A/10) will use all atom types for given index as seed. Multiple specific atoms for a specific index can be specified using comma separation (e.g. A/10/N,H,C,O,CA). Multiple seed indices can be indicated by space separation (e.g. A/10 B/20 ...)")
parser.add_argument("-perm", nargs="+", default=None, help="Optional ability to specify specific atom(s) to always be included in the models in the format chain/index/atom(s). Multiple specific atoms for an index can be specified using comma separation (e.g. A/10/N,H,C,O,CA). Multiple indices can be indicated by space separation (e.g. A/10/N,H,CA,HA B/20/N,H,CA,HA ...)")
parser.add_argument("-info", default="probe_model_combinations.dat", help="Optional name for output datafile detailing generated models with combinations of contact types, default is probe_model_combinations.dat")
parser.add_argument("-o", default="res_atoms_", help="Optional prefix used for constructing res_atoms_#.dat output files, default is 'res_atoms_'")
args = parser.parse_args()

def identify_contact_type(contact, resname, atom):
    mc_atoms = ['C', 'O', 'N', 'H']
    water_names = ['WAT', 'HOH']

    if resname in water_names:
        return "WAT:"+contact
    elif atom in mc_atoms:
        return "MC:"+contact
    else:
        return "SC:"+contact


if __name__ == '__main__':

    #Identify seed part(s)
    whole_seed = []
    part_seed = []
    for i in args.seed:
        if len(i.split("/")) == 2:
            whole_seed.append(i)
        elif len(i.split("/")) == 3:
            for j in i.split("/")[-1].split(","):
                part_seed.append(i.rsplit("/",1)[0]+"/"+j)

    #Extract probe information
    contacts = defaultdict(set)
    seed_atoms = set()

    with open(args.f, 'r') as probefile:
        for line in probefile:
            contact_type = line[6:8]

            chain1 = line[10]
            id1 = line[11:16].strip()
            name1 = line[16:19].strip()
            atom1 = line[19:25].strip()
            
            chain2 = line[27]
            id2 = line[28:33].strip()
            name2 = line[33:36].strip()
            atom2 = line[36:42].strip()

            if chain1+"/"+id1 in whole_seed or chain1+"/"+id1+"/"+atom1 in part_seed:
                seed_atoms.add(chain1+"/"+id1+"/"+atom1)
                #Exclude counting seed-seed interactions
                if chain2+"/"+id2 in whole_seed: continue
                if chain2+"/"+id2+"/"+atom2 in part_seed: continue
                
                contact_class = identify_contact_type(contact_type, name2, atom2)
                contacts[contact_class].add(chain2+"/"+id2+"/"+atom2)

            elif chain2+"/"+id2 in whole_seed or chain2+"/"+id2+"/"+atom2 in part_seed:
                seed_atoms.add(chain2+"/"+id2+"/"+atom2)
                #Exclude counting seed-seed interactions
                if chain1+"/"+id1 in whole_seed: continue
                if chain1+"/"+id1+"/"+atom1 in part_seed: continue

                contact_class = identify_contact_type(contact_type, name1, atom1)
                contacts[contact_class].add(chain1+"/"+id1+"/"+atom1)
                
    #Identify all combinations of contact types (powerset)
    powerset = itertools.chain.from_iterable(itertools.combinations(list(contacts.keys()), r) for r in range(len(list(contacts.keys()))+1))
    
    #Identify all unique model compositions from contact powerset
    models = defaultdict(list)

    if args.perm != None:    #initialize minimal model using seed atoms as base 
        for i in args.perm:
            for j in i.split("/")[-1].split(","):
                seed_atoms.add(i.rsplit("/",1)[0]+"/"+j)
    
    for subset in list(powerset):    #compile atom lists for each contact set
        m = seed_atoms.copy()
        for c in subset:
            m.update(contacts[c])
        models[frozenset(m)].append(subset)

    #Construct models and corresponding key information
    keyfile = open(args.info, 'w')
    model_index = 0

    for item in models.keys():
        model_name = args.o+str(model_index)+".dat"

        #save keyfile info
        keyfile.write(model_name+"\t"+",".join(list(item))+"\t"+",".join(map(str, models[item]))+"\n")

        #summarize atom/residue info
        summary = defaultdict(list)
        for atom in item:
            summary[atom.rsplit("/",1)[0]].append(atom.rsplit("/",1)[1])
        sortednames = list(summary.keys())
        sortednames.sort()

        #save model info
        with open(model_name, 'w') as savefile:
            for res in sortednames:
                savefile.write("\t".join([res.split("/")[0], res.split("/")[1]]+summary[res])+"\n")
        
        model_index +=1

    keyfile.close()
