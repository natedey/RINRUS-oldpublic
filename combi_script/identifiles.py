import filecmp, sys

filenames = open(sys.argv[1],"r").readlines()

dupi = []
for i in range(0,len(filenames)):
    for j in range(i+1,len(filenames)):
        if filecmp.cmp(filenames[i].strip(), filenames[j].strip()) == True:
            mybool = False
            for item in dupi:
                if filenames[i].strip() in item or filenames[j].strip() in item:
                    mybool = True
                    item.extend([filenames[i].strip(), filenames[j].strip()])
            if mybool == False:
                dupi.append([filenames[i].strip(), filenames[j].strip()])

for item in dupi:
    temp = list(set(item))
    for i in range(1,len(temp)):
        filenames.remove(temp[i]+"\n")

savefile = open("UniqueModels.dat", "w")
for name in filenames:
    savefile.write(name)
savefile.close()

