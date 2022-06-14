import filecmp, sys, argparse

parser = argparse.ArgumentParser(description='Identifies unique/duplicate PDBs and compiles interaction information about them from datafile')
parser.add_argument('-datafile', default='../ModSimpCombi.dat', help='name of the interaction datafile to build from')
parser.add_argument('-listfile', default='list', help='list file containing names of all of the pdbs to compare')
parser.add_argument('-uniquefile', default='UniqueModels.dat', help='list file containing names of the Unique PDBs ultimately selected from duplicates')
parser.add_argument('-savefile', default='ArpeggioCombiInteractions.csv', help='name of savefile')
args = parser.parse_args()

uniquenames = [item.strip() for item in open(args.uniquefile, 'r').readlines()]
listnames = open(args.listfile, 'r').readlines()
dupi = []
for i in range(0,len(listnames)):
    for j in range(i+1,len(listnames)):
        if filecmp.cmp(listnames[i].strip(), listnames[j].strip()) == True:
            mybool = False
            for item in dupi:
                if listnames[i].strip() in item or listnames[j].strip() in item:
                    mybool = True
                    item.extend([listnames[i].strip(), listnames[j].strip()])
            if mybool == False:
                dupi.append([listnames[i].strip(), listnames[j].strip()])

uniqdupi = {}
for item in dupi:
    temp = list(set(item))
    for i in range(0,len(temp)):
        if temp[i] in uniquenames:
            uniqdupi[temp[i]] = temp[:i]+temp[i+1:]

data = open(args.datafile, 'r').readlines()
interactions = ["Clash","Covalent","VdWClash","VdW","Proximal","Hbond","weakHbond","Halogen","Ionic","Metal","Aromatic","Hydrophobic","Carbonyl","Polar","weakPolar"]

def compileinters(l1):
    count = [0]*len(interactions)
    for i in l1:
        for j in i:
            count[interactions.index(j)] +=1
    return [len(l1)]+count

savefile = open(args.savefile, 'w')
savefile.write("Model,NumSets,"+",".join(interactions)+",DupModels\n")

for name in uniquenames:
    namei = int(name.split("_")[1].split(".")[0])
    isets = [x.split(",") for x in data[namei-1].strip().split('|')[1:]]
    interdata = compileinters(isets)
    
    altids = []

    if name in uniqdupi.keys():
        for name2 in uniqdupi[name]:
            namej = int(name2.split("_")[1].split(".")[0])
            jsets = [y.split(",") for y in data[namej-1].strip().split("|")[1:]]
            interdata2 = compileinters(jsets)
            interdata = [a+b for a,b in zip(interdata,interdata2)]
            altids.append(namej)
    
    savefile.write(str(namei)+","+",".join(map(str,interdata))+","+",".join(map(str,altids))+"\n")

savefile.close()

