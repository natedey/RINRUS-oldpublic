import pandas as pd
import argparse

class PDB:
    def __init__(self,xcoord,ycoord,zcoord,resi_type):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.zcoord = zcoord
        self.resi_type = resi_type


class atom(object):
    def __init__(self,index,atom_serial_number,residue,residue_number,chain_id,xcoord,ycoord,zcoord,frozen,atom_let,atom_type):
        self.index = index
        self.atom_serial_number = atom_serial_number
        self.residue = residue
        self.residue_number = residue_number
        self.chain_id = chain_id
        self.xcoord = float(xcoord)
        self.ycoord = float(ycoord)
        self.zcoord = float(zcoord)
        self.frozen = str(frozen.strip())
        self.atom_let = str(atom_let)
        self.atom_type = str(atom_type)
def atom_creator(file_1):
    """
    makes atoms objects for a pdb files
    """
    value_1 = []
    with open(file_1,'r') as fp:
        data = fp.readlines()

        for line in data:
            if 'ATOM' in line or 'HETATM' in line:
            
                print(line)
                index_number = line[5:11].strip()
                atom_serial_number = line[12:17].strip()
                residue = line[17:21].strip()
                residue_number = line[22:27].strip()
                chain_id = line[21]
                xcoord = line[30:39].strip()
                ycoord = line[38:47].strip()
                zcoord = line[46:55].strip()
                frozen = line[83:].strip()
                atom_let = line[73:83].strip()
                atom_let = atom_let[0:2].replace('0','').replace('1','')
                atom_type = line[11:17].strip()
                # print(atom_type)
                value_1.append(atom(index_number,atom_serial_number,residue,residue_number,chain_id,xcoord,ycoord,zcoord,frozen,atom_let,atom_type).__dict__)
    return value_1
def frozen_atoms(df,freezer):
    for index,row in df.iterrows():
        #print(df[i]['frozen'])
        if row['frozen'] == '-1':
            if freezer == True:
                tot = str(row['index']) + ' XYZ'
                #print(tot)

                '''
                row['atom_let']
                row['xcoord']
                row['ycoord']
                row['zcoord']
                '''
    return
def chain_selector(df):
    main_chain ={}
    for index,row in df.iterrows():
        if row['residue'] == 'WAT' or row['residue'] == 'WT1':
            pass
        else: 
            if row['atom_type'] == 'H' or row['atom_type'] == 'C' or row['atom_type'] == 'O' or row['atom_type'] == 'N':
                main_chain[row['residue']+':'+row['residue_number']+':'+row['chain_id']]=row
            else:
                row
    print(main_chain)
    return 

def distance(df):
    distance = []
    distance = ((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)**0.5
    return
def df_to_dict(df):
    abc = {}
    for index,row in df.iterrows():
        abc[row['atom_serial_number']+':'+row['residue_number']+':'+row['chain_id']]=[row['atom_let'],row['frozen'],row['xcoord'],row['ycoord'],row['zcoord']]
    for i in abc.keys():
        print(i)
        

    return


def xyz_grabber(df):

    return


def main(args):
    print(args.pdb)
    pdb = atom_creator(args.pdb)
    df = pd.DataFrame(pdb)
    h_added = args.pdb.replace('.pdb','_h.pdb')
    pdb_h = atom_creator(h_added)
    df_2 = pd.DataFrame(pdb_h)
    
    #frozen_atoms(df,freezer=True)
    chain_selector(df)
    df.to_csv('test.csv',index=False)
    print(df)
    print(h_added)
    print(df_2)
    noh_dict = df_to_dict(df)
    h_dict = df_to_dict(df_2)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = '',
        description=''
    )
    parser.add_argument('-noh', dest='pdb', default='filename', type=str,
            help = 'pdb file with frozen coordinates') 
    args = parser.parse_args()
    main(args)


