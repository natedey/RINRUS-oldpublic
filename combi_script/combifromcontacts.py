#! /usr/bin/env python
import sys, argparse, itertools
from collections import defaultdict

parser = argparse.ArgumentParser(description='Compute Combinatorics of Interaction types from Arpeggio .contacts file')
parser.add_argument('contfile', help='name of .contact file')
parser.add_argument('-int', help='interactions to always include')
parser.add_argument('seed', help='comma-seaparated list of seed residues in format chain/resnum')
parser.add_argument('sift', help='sift file')
parser.add_argument('-addseed', help='comma-separated list of residue parts in format /chain/resnum/part')

args = parser.parse_args()
d = defaultdict(list) #dict with res+waters combined
#e = defaultdict(list) #dict with res and water contacts separated
seedres = args.seed.split(',')

def classres(d, line, name):
    sep = line.split()
    if sep[2] == "1" and name not in d["Clash"]:
        d["Clash"].append(name)
    if sep[3] == "1" and name not in d["Covalent"]:
        d["Covalent"].append(name)
    if sep[4] == "1" and name not in d["VdWClash"]:
        d["VdWClash"].append(name)
    if sep[5] == "1" and name not in d["VdW"]:
        d["VdW"].append(name)
    if sep[6] == "1" and name not in d["Proximal"]:
        d["Proximal"].append(name)
    if sep[7] == "1" and name not in d["Hbond"]:
        d["Hbond"].append(name)
    if sep[8] == "1" and name not in d["weakHbond"]:
        d["weakHbond"].append(name)
    if sep[9] == "1" and name not in d["Halogen"]:
        d["Halogen"].append(name)
    if sep[10] == "1" and name not in d["Ionic"]:
        d["Ionic"].append(name)
    if sep[11] == "1" and name not in d["Metal"]:
        d["Metal"].append(name)
    if sep[12] == "1" and name not in d["Aromatic"]:
        d["Aromatic"].append(name)
    if sep[13] == "1" and name not in d["Hydrophobic"]:
        d["Hydrophobic"].append(name)
    if sep[14] == "1" and name not in d["Carbonyl"]:
        d["Carbonyl"].append(name)
    if sep[15] == "1" and name not in d["Polar"]:
        d["Polar"].append(name)
    if sep[16] == "1" and name not in d["weakPolar"]:
        d["weakPolar"].append(name)

def classwat(d, line, name):
    sep = line.split()
    if sep[2] == "1" and name not in d["WatClash"]:
        d["WatClash"].append(name)
    if sep[3] == "1" and name not in d["WatCovalent"]:
        d["WatCovalent"].append(name)
    if sep[4] == "1" and name not in d["WatVdWClash"]:
        d["WatVdWClash"].append(name)
    if sep[5] == "1" and name not in d["WatVdW"]:
        d["WatVdW"].append(name)
    if sep[6] == "1" and name not in d["WatProximal"]:
        d["WatProximal"].append(name)
    if sep[7] == "1" and name not in d["WatHbond"]:
        d["WatHbond"].append(name)
    if sep[8] == "1" and name not in d["WatweakHbond"]:
        d["WatweakHbond"].append(name)
    if sep[9] == "1" and name not in d["WatHalogen"]:
        d["WatHalogen"].append(name)
    if sep[10] == "1" and name not in d["WatIonic"]:
        d["WatIonic"].append(name)
    if sep[11] == "1" and name not in d["WatMetal"]:
        d["WatMetal"].append(name)
    if sep[12] == "1" and name not in d["WatAromatic"]:
        d["WatAromatic"].append(name)
    if sep[13] == "1" and name not in d["WatHydrophobic"]:
        d["WatHydrophobic"].append(name)
    if sep[14] == "1" and name not in d["WatCarbonyl"]:
        d["WatCarbonyl"].append(name)
    if sep[15] == "1" and name not in d["WatPolar"]:
        d["WatPolar"].append(name)
    if sep[16] == "1" and name not in d["WatweakPolar"]:
        d["WatweakPolar"].append(name)

seedatoms = []
with open(args.contfile,"r") as contfile:
    for line in contfile:
        ignoreflags = ['INTRA','INTRA_SELECTION','INTRA_NON_SELECTION','NON_SELECTION_WATER','WATER_WATER']
        if line.split()[-1] in ignoreflags : continue

        if line.split()[0].rsplit("/",1)[0] in seedres:
            atom = line.split()[1]
            seedatoms.append(line.split()[0])
        else: 
            atom = line.split()[0]
            seedatoms.append(line.split()[1])

        if line.split()[-1] == "SELECTION_WATER":
            classres(d, line, atom)
#            classwat(e, line, atom)
        else:
            classres(d, line, atom)
#            classres(e, line, atom)
seedatoms = list(set(seedatoms))
seedatoms.sort()

dInterCombi = []
#eInterCombi = []
for i in range(1,len(d.keys())+1):
    dInterCombi.extend(list(combi) for combi in itertools.combinations(d.keys(), i))
#for i in range(1, len(e.keys())+1):
#    eInterCombi.extend(list(combi) for combi in itertools.combinations(e.keys(), i))

def InterToRes(mylist, mydict):
    newlist = []
    for inter in mylist:
        newlist.extend(mydict[inter])
    newlist = list(set(newlist))
    newlist.sort()
    return newlist

dResCombi = []
#eResCombi = []
for combi in dInterCombi:
    dResCombi.append(InterToRes(combi, d))
#for combi in eInterCombi:
#    eResCombi.append(InterToRes(combi, e))

#Unaltered Long Form
savelong1 = open("LongCombi.dat","w")
#savelong2 = open("LongSepWat.dat","w")
for i in range(0, len(dInterCombi)):
    savelong1.write(",".join(dInterCombi[i]) + "|" + ",".join(dResCombi[i]) + "\n")
#for i in range(0, len(eInterCombi)):
#    savelong2.write(",".join(eInterCombi[i]) + "|" + ",".join(eResCombi[i]) + "\n")
savelong1.close()
#savelong2.close()

#Unaltered Simple Form
dSimp = defaultdict(list)
#eSimp = defaultdict(list)
for i in range(0, len(dResCombi)):
    dSimp[",".join(dResCombi[i])].append(dInterCombi[i])
#for i in range(0, len(eResCombi)):
#    eSimp[",".join(eResCombi[i])].append(eInterCombi[i])
savesimp1 = open("SimpCombi.dat","w")
#savesimp2 = open("SimpSepWat.dat","w")
for model in dSimp.keys():
    savesimp1.write(model + "|" + "|".join([str(x) for x in dSimp[model]]) + "\n")
#for model in eSimp.keys():
#    savesimp2.write(model + "|" + "|".join([str(x) for x in eSimp[model]]) + "\n")
savesimp1.close()
#savesimp2.close()

#Identify availale residues in sift file
availres = defaultdict(list)
with open(args.sift, "r") as siftfile:
    for line in siftfile:
        availres[line.split()[0].rsplit("/",1)[0]].append(line.split()[0].rsplit("/",1)[1])

#Altered include Seed, specified Interactions, specified Res, and (where applicable) Alanine corrections
if args.int != None:
    intopts = ["Clash","Covalent","VdWClash","VdW","Proximal","Hbond","weakHbond","Halogen","Ionic","Metal","Aromatic","Hydrophobic","Carbonyl","Polar","weakPolar"]
    for inter in args.int.split(","):
        if inter not in intopts: 
            print("Available interactions limited to: Clash, Covalent, VdWClash, VdW, Proximal, Hbond, weakHbond, Halogen, Ionic, Metal, Aromatic, Hydrophobic, Carbonyl, Polar, weakPolar")
            sys.exit()
    for i in range(0, len(dInterCombi)):
        for item in args.int.split(","):
            if item not in dInterCombi[i]: dInterCombi[i].extend([item])

dResCombi.clear()
dSimp.clear()
for combi in dInterCombi:
    newlist = []
    newdict = defaultdict(list)
    for inter in combi:
        newlist.extend(d[inter])
    newlist.extend(seedatoms)
    if args.addseed != None:
        newlist.extend(args.addseed.split(","))
    for atom in newlist:
        newdict[atom.rsplit("/",1)[0]].append(atom.rsplit("/",1)[1])
    for res in newdict.keys():
        if newdict[res] == ["CA"] and res.split("/")[0]+"/"+str(int(res.split("/")[1])-1) not in newdict.keys() and res.split("/")[0]+"/"+str(int(res.split("/")[1])+1) not in newdict.keys():
            if "C" in availres[res] or "O" in availres[res]:
                newlist.append(res+"/C")
            if "N" in availres[res] or "H" in availres[res]:
                newlist.append(res+"/N")
    newlist = list(set(newlist))
    newlist.sort()
    dResCombi.append(newlist)
for i in range(0,len(dResCombi)):
    dSimp[",".join(dResCombi[i])].append(dInterCombi[i])
savesimp3 = open("ModSimpCombi.dat","w")
for model in dSimp.keys():
    savesimp3.write(model + "|" + "|".join([",".join(x) for x in dSimp[model]]) + "\n")
savesimp3.close()
        


