#! /usr/bin/env python
import os, sys, re
import argparse
from collections import Counter

parser = argparse.ArgumentParser(description='Analyzes probe data')
parser.add_argument('-data',type=argparse.FileType('r'), help='file containing probe information')
# parser.add_argument('-res', help='residue information provided in format chain:residue,chain:residue,...')
parser.add_argument('-model',type=argparse.FileType('r'),help='pdb file containing model information')
# parser.add_argument('-meshname', default='probemesh.dat', help='name of probe mesh savefile')
# parser.add_argument('-resname', default='outerres.dat', help='name of outer residues savefile')
args = parser.parse_args()
writeto= "probemesh_rin.dat" # It will create and write in "probemesh.dat"
meshxyz= "probemesh_rin.xyz" # It will create and write in "probemesh.xyz"

def get_side(c):
    cha    = c[:2].strip()          # chain 
    res_id = c[2:6].strip()         # res_id 
    res_nm = c[6:10].strip()        # res_name
    atom   = c[10:-1].strip()       # atom_name
    if c[-1] == ' ':
        spe_c = 'A'
    else:
        spe_c = c[-1]
    return cha, res_id, res_nm, atom, spe_c
#######################################################################
## Next Part create and print list of residues from given info.
#######################################################################
with args.data as f:
    lines=f.readlines()

with args.model as m:
    mlines=m.readlines()

keymodel=[]
for line in mlines:
    record = line[:6].strip()
    serial = ( line[6:11].strip() )
    atomname = line[12:16].strip()
    altloc = line[16].strip()
    resname = line[17:20].strip()
    chain = line[21].strip()
    resnum = ( line[22:26].strip() )
    achar = line[26].strip()
    x = float(line[30:38])
    y = float(line[38:46])
    z = float(line[46:54])
    # print(atomname,x,y,z)
    # keym = atomname+':'+resname+':'+chain+':'+resnum
    keym = chain+':'+resnum+':'+resname+':'+atomname
    keymodel.append(keym)

#  pdb.append( [ record, serial, atomname, altloc, resname, chain, resnum, achar, x, y, z, occ, tfactor, segid, elsymbol, charge.strip(), fix ] )
  #     1          0       1       2       3       4           5   6       7      8  9  10 11   12         13      14      15      16


#######################################################################
## Next Part write atom and xyz cordinates using Model and Mesh residues. 
#######################################################################
linecount=0
with open (f"{writeto}","w") as writestart:
    for line in lines:
        c = line.split(':')
        obj1 = c[1]
        acts = c[2]
        xcordinate= c[-5]
        ycordinate= c[-4]
        zcordinate= c[-3]
        atom= c[-7]
        score1= c[-9]
        score2= c[-8]
        cha1, res_id1, res_nm1, atom1, spe_c1 = get_side(c[3])           
        cha2, res_id2, res_nm2, atom2, spe_c2 = get_side(c[4])  

        if cha1 == cha2 and res_id1 == res_id2: continue
        key1 = cha1+':'+res_id1+':'+res_nm1+':'+atom1
        key2 = cha2+':'+res_id2+':'+res_nm2+':'+atom2

        if key1 in keymodel:
            if (acts == "hb"):
                printlist=["H",xcordinate,ycordinate,zcordinate,"@",acts,key2,score1,score2]
            elif (acts == "bo" or acts == "so"):
                printlist=["N",xcordinate,ycordinate,zcordinate,"@",acts,key2,score1,score2] 
            else:
                printlist=["O",xcordinate,ycordinate,zcordinate,"@",acts,key2,score1,score2]
            list_to_string='   '.join((printlist)) 
            writestart.writelines('%s\n' % list_to_string)
            linecount += 1

        if key2 in keymodel:
            if (acts == "hb"):
                printlist=["H",xcordinate,ycordinate,zcordinate,"@",acts,key1,score1,score2]
            elif (acts == "bo" or acts == "so"):
                printlist=["N",xcordinate,ycordinate,zcordinate,"@",acts,key1,score1,score2] 
            else:
                printlist=["O",xcordinate,ycordinate,zcordinate,"@",acts,key1,score1,score2]
            list_to_string='   '.join((printlist)) 
            writestart.writelines('%s\n' % list_to_string)
            linecount += 1
#######################################################################
## Next Part count atoms and create xyz format file from all cordinates.
#######################################################################

readstart= open(f"{writeto}")
xyzlines= readstart.readlines()

with open (f"{meshxyz}","w") as writexyzstart:
    writexyzstart.writelines(str('%s\n' % linecount))
    writexyzstart.writelines(str('%s\n' % (" ")))
    for xline in xyzlines:
        xline1,xline2= xline.split('@')
        writexyzstart.writelines('%s\n' %xline1)

print(f"xyz cordinates saved in {writeto} and saving xyz molecule format in {meshxyz} is completed.\n H = hb (hydrogen bond), N = so,bo (big overlap), o = others ")
writestart.close()
writexyzstart.close()

