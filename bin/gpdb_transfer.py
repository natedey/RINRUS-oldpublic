#############################################################################
### Usage: gpdb_transfer.py -i input_dir -o output_dir -r template_dir!"
#############################################################################

import os, sys, re
from glob import glob
from numpy import *
import argparse

#def main():
    ### check how many directories are here ###
    ### 
    ### generate pdbfiles from finished output file ###
    ### transfer file to leviathan ###

def system_run(cmd):
    print(cmd)
    exit = os.system(cmd)
    if ( exit != 0 ):
        print('failed to run:')
        print(cmd)
        sys.exit()
 

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


### Use the current exist pdbfiles and transfer the last pdb file ###
def get_pdb_pdbfiles(dirf):
    c = dirf.split('/')
    if 'irc1' in c[-1] or 'irc2' in c[-1]:
        trans_name = '%s-%s.pdb'%(c[-2],c[-1])
    else:
        trans_name = '%s.pdb'%c[-1]
    pdb_name = []
    for pdbf in glob('%s/pdbfiles/*.pdb'%dirf):
        m = re.search('(\d+).pdb',pdbf.split('/')[-1])
        pdb_name.append( int(m.group(1)) )
    return max(pdb_name)

### Suppose the template pdb file is under the model directory ###
def gen_pdbfiles_indir(dirf,project_dir):
    c = dirf.split('/')
    if 'irc1' in c[-1] or 'irc2' in c[-1]:
        trans_name = '%s-%s.pdb'%(c[-2],c[-1])
        model_pdb_dir = dirf[:-5]
    else:
        trans_name = '%s.pdb'%c[-1]
        model_pdb_dir = dirf
    temp = '%s/template.pdb'%model_pdb_dir
    if temp:
        print(temp)
    else:
        temp = raw_input('Where is the template pdb file: ')
    new_dir = '%s/pdbfiles'%dirf
    if os.path.isdir(new_dir):
        system_run('rm -r %s'%new_dir)
        system_run('mkdir %s'%new_dir)
    else:
        system_run('mkdir %s'%new_dir)
    os.chdir(new_dir)
    system_run('python3 ~/git/RINRUS/bin/gopt_to_pdb.py -p %s -o %s/1.out -f -1'%(temp[0],dirf))
    os.chdir('%s'%project_dir)
    pdb_name = []
    for pdbf in glob('%s/*.pdb'%new_dir):
        m = re.search('(\d+).pdb',pdbf.split('/')[-1])
        pdb_name.append( int(m.group(1)) )
    return max(pdb_name)

### All tmeplate files are under one directory, user needs to provide the full path ###
def gen_pdbfiles(dirf,project_dir,temp_dir):
    c = dirf.split('/')
    if c[-1] == '':
        c = c[:-1]
    if 'irc1' in c[-1] or 'irc2' in c[-1]:
        tpdir = dirf[:-5]
        if 'freq' in c[-2]:
            trans_name = '%s-%s.pdb'%(c[-3],c[-1])
            m = re.search(r'(\d+)',c[-3])
        else:
            trans_name = '%s-%s.pdb'%(c[-2],c[-1])
            m = re.search(r'(\d+)',c[-2])
    else:
        tpdir = dirf
        if 'freq' in c[-1]:
            trans_name = '%s.pdb'%c[-2]
            m = re.search(r'(\d+)',c[-2])
        else:
            trans_name = '%s.pdb'%c[-1]
            m = re.search(r'(\d+)',c[-1])
    if os.path.isfile('%s/template.pdb'%tpdir):
        print(tpdir)
        temp = '%s/template.pdb'%tpdir
    else:
        temp = '%s/final_%d.pdb'%(temp_dir,int(m.group(1)))
    new_dir = '%s/pdbfiles'%dirf
    if os.path.isdir(new_dir):
        system_run('rm -r %s'%new_dir)
        system_run('mkdir %s'%new_dir)
    else:
        system_run('mkdir %s'%new_dir)
    os.chdir(new_dir)
    system_run('python3 ~/git/RINRUS/bin/gopt_to_pdb.py -p %s -o %s/1.out -f -1'%(temp,dirf))
    os.chdir('%s'%project_dir)
    pdb_name = []
    for pdbf in glob('%s/*.pdb'%new_dir):
        m = re.search('(\d+).pdb',pdbf.split('/')[-1])
        pdb_name.append( int(m.group(1)) )
    return max(pdb_name), trans_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transfer pdbfiles from hpc to another machine')
    parser.add_argument('-i', dest='input_dirs',default=None, help='project dir')
    parser.add_argument('-o', dest='output_dir',default=None, help='output dir')
    parser.add_argument('-r', dest='ref_dir',default='template.pdb', help='temp dir')

    args = parser.parse_args()
    if args.input_dirs == None or args.output_dir == None:
        print("Please run: Program -i input_dir -o output_dir -r template_dir!")
        sys.exit()

    project_dir = os.path.abspath(args.input_dirs) 
    name = '%s/list'%project_dir
    if os.path.isfile(name) == False:
        print("Please provide a file name 'list' contains all the directory you want to process under your project directory!")
        sys.exit()
    else:
        print("Project directory is: %s"%project_dir)
        complete,incomple = get_all_files(name)
        if len(incomple) != 0:
            print('%s is not complete'%incomple[0])
            sys.exit()
        leviathan = args.output_dir
        print("Final pdb files will be transferred to leviathan:%s"%leviathan)
        if args.ref_dir != None:
            temp_dir = os.path.abspath(args.ref_dir)
            print("All template pdb files are in directory: %s"%temp_dir)
            temp_dir = args.ref_dir
            for dirf in complete:
                pdb, trans_name = gen_pdbfiles(dirf,project_dir,temp_dir)
                print("Transferring %s"%trans_name)
                cmd = 'scp %s/pdbfiles/%s.pdb 141.225.147.5:%s/%s'%(dirf,pdb,leviathan,trans_name)
                system_run(cmd)
        else:
            for dirf in complete:
                pdb, trans_name = gen_pdbfiles(dirf,project_dir,dirf)
                print("Transferring %s"%trans_name)
                cmd = 'scp %s/pdbfiles/%s.pdb 141.225.147.5:%s/%s'%(dirf,pdb,leviathan,trans_name)
                system_run(cmd)

