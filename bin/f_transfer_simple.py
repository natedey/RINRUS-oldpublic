import os, sys, re
from glob import glob
from numpy import *


def system_run(cmd):
    print(cmd)
    exit = os.system(cmd)
    if ( exit != 0 ):
        print('failed to run:')
        print(cmd)
        sys.exit()

def get_pdb_pdbfiles(dirf):
    c = dirf.split('/')
    if 'irc1' in c[-1] or 'irc2' in c[-1]:
        trans_name = '%s-%s.pdb'%(c[-2],c[-1])
    else:
        trans_name = '%s.pdb'%(c[-1])
    pdb_name = []
    for pdbf in glob('%s/pdbfiles/*.pdb'%dirf):
        m = re.search('(\d+).pdb',pdbf.split('/')[-1])
        pdb_name.append( int(m.group(1)) )
    return max(pdb_name), trans_name


### If the full family path is provides ###
def get_all_files(project_dirsf):
    with open(project_dirsf) as f:
        lines = f.readlines()
    complete = []
    incomple = []
    for i in lines:
        i = i.strip()
        if os.path.isfile('%s/1.out'%i):
            with open('%s/1.out'%i) as outf:
                outfl = outf.readlines()
                if "Normal termination" in outfl[-1]:
                    complete.append('%s'%i)
                else:
                    incomple.append('%s'%i)
        else:
            print("Either the 1.out file does not exist or the directory name %s is wrong, please check!"%i.strip())
    return complete, incomple


if __name__ == '__main__':
    ###########################################################################
    ### python3 ~/git/RINRUS/bin/f_transfer_simple.py hpc_dir leviathan_dir ###
    ###########################################################################
    project_dir = sys.argv[1]
    os.chdir(project_dir)
    cwd = os.getcwd()
    name = '%s/list'%project_dir
    leviathan = sys.argv[2]
    complete,incomple = get_all_files(name)
    for dirf in complete:
        pdb, trans_name = get_pdb_pdbfiles(dirf)
        cmd = 'scp %s/pdbfiles/%s.pdb leviathan:%s/%s'%(dirf,pdb,sys.argv[2],trans_name)
        system_run(cmd)
