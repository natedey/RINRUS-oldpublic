import os
import argparse
import shutil
import shlex,subprocess
from pathlib import Path


def driver_file_reader(file):
    pdb = ''
    Seed = []
    seed = ''
    RIN_program = ''
  #  Histidine = ''
  #  numberofmodels = ''
    charge = ''
    multi = ''
  #  residues_not_protonated = ''
    Computational_program = ''
    template_path = ''
    basis_set_library = ''
    with open(file,'r') as fp:
        data = fp.readlines()
        for line in data:
            #print(line)
            if '#' in line:
                line
            else:
                if 'PDB' in line:
                    pdb += line.replace('PDB:','').replace('\n','').replace(' ','')
                if 'Seed' in line:
                    if ',' in line:
                        line = line.replace('Seed:','').replace('\n','').replace(' ','')
                        seed+= line
                        line = line.split(',')
                        for i in line:
                            if i=='':
                                pass
                            else:
                                Seed.append(i)
                        
                    else:
                        seed+= line.replace('Seed:','').replace('\n','').replace(' ','')
                        Seed.append(line.replace('Seed:','').replace('\n','').replace(' ',''))
                if 'RIN_program' in line:
                    RIN_program += line.replace('RIN_program:','').replace('\n','').replace(' ','')
                if 'Substrate(s)_charge' in line:
                    charge += line.replace('Substrate(s)_charge:','').replace('\n','').replace(' ','')
                if 'Multiplicity' in line:
                    multi+= line.replace('Multiplicity:','').replace('\n','').replace(' ','')
                if 'Computational_program' in line:
                    Computational_program += line.replace('Computational_program:','').replace('\n','').replace(' ','')
                if 'input_template_path' in line:
                    template_path += line.replace('input_template_path:','').replace('\n','').replace(' ','')
                if 'basisset_library' in line:
                    basis_set_library += line.replace('basisset_library:','')
                    
                    #print(line)
    return pdb,Seed,RIN_program,charge,multi,Computational_program,template_path,basis_set_library,seed
def commands_step1(pdb):
    path = os.path.expanduser('~/git/RINRUS/bin/reduce')
    pdb_2 = pdb.replace('.pdb','')
    os.system('~/git/RINRUS/bin/reduce -NOFLIP '+ str(pdb)+ ' > '+ str(pdb_2)+'_h.pdb')
    shutil.copy(str(pdb_2)+'_h.pdb',str(pdb_2)+'_h_modify.pdb')
    mod_pdb = str(pdb_2)+'_h_modify.pdb' 
    return mod_pdb
def commands_step2(pdb):
    probe = pdb.replace('.pdb','')
    os.system('~/git/RINRUS/bin/probe -unformated -MC -self "all" '+ pdb +' > '+ probe + '.probe')
    probe = probe + '.probe'
    return probe
def commands_step3(probe,seed):
    print(probe)
    path = os.path.expanduser('~/git/RINRUS/bin/probe2rins.py')
    #os.system('python3 ~/git/RINRUS/bin/probe2rins.py -f '+ str(probe)+ ' -s ' + seed)
    args = ['python3',path, '-f',probe,'-s',seed.replace('\n','')]
    print(args)
    result = subprocess.run(args)
    return

def res_atom_count(filename):
    num = 0
    with open(filename,'r') as fp:
        data = fp.readlines()
        num += len(data)
        for i in data:
            if i == '':
                num -= 1
    return num

def commands_step4(seed,pdb,model_num):
    #print(pdb)
    path = os.path.expanduser('~/git/RINRUS/bin/rinrus_trim2_pdb.py')
    args = ['python3',path, '-s',str(seed).replace('\n',''), '-pdb',str(pdb), '-model', str(model_num)]
    result = subprocess.run(args)
    
    
    return

def commands_step5(freeze,model_num):
    path = os.path.expanduser('~/git/RINRUS/bin/pymol_scripts.py')
    name = 'res_' + str(model_num)+'.pdb'
    arg= ['python3',path, '-resids', str(freeze),'-pdbfilename', name]
    print(arg) 
    result = subprocess.run(arg)
    return

def command_step6(template,format,basisinfo,charge,model_num):
    
    path = os.path.expanduser('~/git/RINRUS/bin/write_input.py')
    path_2 =os.path.expanduser(basisinfo.replace('\n','').replace(' ','')) 
    noh =  ' res_'+model_num+'.pdb '
    adh = ' res_'+model_num+'_h.pdb'
    arg= ['python3', path ,'-intmp',str(template),'-format',str(format),'-basisinfo',path_2,'-c','-2','-noh',str(noh).replace(' ',''),'-adh',str(adh).replace(' ','')]
    print(arg)
    result = subprocess.run(arg)
    return


def distance(calc_type,hydro,pdb,seed,cut):
    path = os.path.expanduser('~/git/RINRUS/bin/pdb_dist_rank.py')
    if hydro.lower() == "nohydro":
        arg = ['python3', path ,'-pdb',str(pdb),'-s',str(seed),'-cut',cut,'-type',calc_type,'-nohydro']
        result = subprocess.run(arg)
    else:
        arg = ['python3', path ,'-pdb',str(pdb),'-s',str(seed),'-cut',cut,'-type',calc_type]
        result = subprocess.run(arg)
    return

def arpreggio(pdb,seed):
    path = os.path.expanduser('~/git/RINRUS/arpeggio/arpeggio.py')
    arg = ['python3',path,str(pdb)]
    result = subprocess.run(arg)
    path = os.path.expanduser('~/git/RINRUS/bin/arpeggio2rins.py')
    arg = ['python3',path,str(pdb),'-f',str(pdb).replace('pdb','contacts'),'-s',seed]
    result = subprocess.run(arg)
    return

def commands_steparp(seed,pdb,model_num):
    #print(pdb)
    path = os.path.expanduser('~/git/RINRUS/bin/rinrus_trim2_pdb.py')
    args = ['python3',path, '-s',str(seed).replace('\n',''), '-pdb',str(pdb),'-c','contact_count.dat', '-model', str(model_num)]
    result = subprocess.run(args)
    
    
    return
def main(file,nor):
    print(nor)
    driver_input_file = file
    pdb,Seed,RIN_program,charge,multi,Computational_program,template_path,basis_set_library,seed= driver_file_reader(file)
    RIN_program = RIN_program.lower()
    amountofseed = len(Seed)
    print(amountofseed)
    #pdb = input('What is pdb name? ')
    #seed = input('What is the seeds name? ')
    mod_pdb = pdb
    if nor == 'False':
        mod_pdb = commands_step1(pdb)
    
    
        if RIN_program.lower()== 'probe':
            probe = commands_step2(mod_pdb)
            commands_step3(probe,seed)
            num_lines = res_atom_count('res_atoms.dat')
            option = list(range(amountofseed+1,num_lines+1))
            option.append('all')
            print('Insert '+ str(num_lines)+ ' for the largest model')
            print('Other options are listed below')
            print(option)
            model_num = input('What model number would you like? (type "all" if you want all of the models ) ')
            freeze = input("What residues do you not want PyMol to protinate? (Typically, this is the seed) ")
            if model_num=='all':
                num_lines = res_atom_count('res_atoms.dat')
                tot = []
                for num in range(amountofseed+1,num_lines+1):
                    print(num)
                    tot.append(num)
                    commands_step4(seed,mod_pdb,num)
                    commands_step5(freeze,num)
                    command_step6(template_path,Computational_program,basis_set_library,charge,str(num))
                    shutil.copy('1.inp',str(num)+'.inp')
                    shutil.copy('template.pdb','template_'+str(num)+'_.pdb')
            else:
                commands_step4(seed,mod_pdb,model_num)
                commands_step5(freeze,model_num)
                command_step6(template_path,Computational_program,basis_set_library,charge,model_num)

        if RIN_program.lower() == 'arpeggio':
            arpreggio(pdb,seed)
            model_num = input('What model number would you like? (type "all" if you want all of the models ) ')
            commands_steparp(seed,pdb,model_num)
            if model_num=='all':
                num_lines = res_atom_count('contact_counts.dat')
                tot = []
                for num in range(amountofseed+1,num_lines+1):
                    print(num)
                    tot.append(num)
                    commands_steparp(seed,pdb,model_num)
                    commands_step5(freeze,num)
                    command_step6(template_path,Computational_program,basis_set_library,charge,str(num))
                    shutil.copy('1.inp',str(num)+'.inp')
                    shutil.copy('template.pdb','template_'+str(num)+'_.pdb')
            else:
                commands_steparp(seed,pdb,model_num)
                commands_step5(freeze,model_num)
                command_step6(template_path,Computational_program,basis_set_library,charge,model_num)
        if RIN_program.lower() == 'manual':
            num_lines = res_atom_count('res_atoms.dat')
            option = list(range(amountofseed+1,num_lines+1))
            option.append('all')
            print('Insert '+ str(num_lines)+ ' for the largest model')
            print('Other options are listed below')
            print(option)
            model_num = input('What model number would you like? (type "all" if you want all of the models ) ')
            freeze = input("What residues do you not want PyMol to protinate? (Typically, this is the seed) ")
            if model_num=='all':
                num_lines = res_atom_count()
                tot = []
                for num in range(amountofseed+1,num_lines+1):
                    print(num)
                    tot.append(num)
                    commands_step4(seed,mod_pdb,num)
                    commands_step5(freeze,num)
                    command_step6(template_path,Computational_program,basis_set_library,charge,str(num))
                    shutil.copy('1.inp',str(num)+'.inp')
                    shutil.copy('template.pdb','template_'+str(num)+'_.pdb')
            else:
                commands_step4(seed,mod_pdb,model_num)
                commands_step5(freeze,model_num)
                command_step6(template_path,Computational_program,basis_set_library,charge,model_num)
            print("Program assumes user has already created there own res_atom.dat file")
            
        if RIN_program.lower() == 'distance':
            calc_type = input("Do you want distance based calc to be average or center of mass of the seed? (avg or mass): ")
            hydro = input("Do you want (hydro or nohydro) ")
            cut = input("What is the cutoff distance in angstroms? ")
            distance(calc_type,hydro,pdb,seed,cut)
            print('For cluster model creation, change create your own res_atoms and change RIN program to manual. This program does not run center of mass or avg on center_atoms')
    if nor == 'True':
        mod_pdb=pdb
        if RIN_program.lower()== 'probe':
            probe = commands_step2(mod_pdb)
            commands_step3(probe,seed)
            num_lines = res_atom_count()
            option = list(range(amountofseed+1,num_lines+1))
            option.append('all')
            print('Insert '+ str(num_lines)+ ' for the largest model')
            print('Other options are listed below')
            print(option)
            model_num = input('What model number would you like? (type "all" if you want all of the models ) ')
            freeze = input("What residues do you not want PyMol to protinate? (Typically, this is the seed) ")
            if model_num=='all':
                num_lines = res_atom_count()
                tot = []
                for num in range(amountofseed+1,num_lines+1):
                    print(num)
                    tot.append(num)
                    commands_step4(seed,mod_pdb,num)
                    commands_step5(freeze,num)
                    command_step6(template_path,Computational_program,basis_set_library,charge,str(num))
                    shutil.copy('1.inp',str(num)+'.inp')
                    shutil.copy('template.pdb','template_'+str(num)+'_.pdb')
            else:
                commands_step4(seed,mod_pdb,model_num)
                commands_step5(freeze,model_num)
                command_step6(template_path,Computational_program,basis_set_library,charge,model_num)

        if RIN_program.lower() == 'arpeggio':
            arpreggio(pdb,seed)
            model_num = input('What model number would you like? (type "all" if you want all of the models ) ')
            commands_steparp(seed,pdb,model_num)
            if model_num=='all':
                num_lines = res_atom_count('contact_counts.dat')
                tot = []
                for num in range(amountofseed+1,num_lines+1):
                    print(num)
                    tot.append(num)
                    commands_steparp(seed,pdb,model_num)
                    commands_step5(freeze,num)
                    command_step6(template_path,Computational_program,basis_set_library,charge,str(num))
                    shutil.copy('1.inp',str(num)+'.inp')
                    shutil.copy('template.pdb','template_'+str(num)+'_.pdb')
            else:
                commands_steparp(seed,pdb,model_num)
                commands_step5(freeze,model_num)
                command_step6(template_path,Computational_program,basis_set_library,charge,model_num)
        if RIN_program.lower() == 'manual':
            num_lines = res_atom_count()
            option = list(range(amountofseed+1,num_lines+1))
            option.append('all')
            print('Insert '+ str(num_lines)+ ' for the largest model')
            print('Other options are listed below')
            print(option)
            model_num = input('What model number would you like? (type "all" if you want all of the models ) ')
            freeze = input("What residues do you not want PyMol to protinate? (Typically, this is the seed) ")
            if model_num=='all':
                num_lines = res_atom_count()
                tot = []
                for num in range(amountofseed+1,num_lines+1):
                    print(num)
                    tot.append(num)
                    commands_step4(seed,mod_pdb,num)
                    commands_step5(freeze,num)
                    command_step6(template_path,Computational_program,basis_set_library,charge,str(num))
                    shutil.copy('1.inp',str(num)+'.inp')
                    shutil.copy('template.pdb','template_'+str(num)+'_.pdb')
            else:
                commands_step4(seed,mod_pdb,model_num)
                commands_step5(freeze,model_num)
                command_step6(template_path,Computational_program,basis_set_library,charge,model_num)
            print("Program assumes user has already created there own res_atom.dat file")
        if RIN_program.lower() == 'distance':
            calc_type = input("Do you want distance based calc to be average or center of mass of the seed? (avg or mass): ")
            hydro = input("Do you want (hydro or nohydro) ")
            cut = input("What is the cutoff distance in angstroms? ")
            distance(calc_type,hydro,pdb,seed,cut)
            print('For cluster model creation, change create your own res_atoms and change RIN program to manual. This program does not run center of mass or avg on center_atoms')
        
        
         
    return

if __name__ == '__main__':
    """ Usage: input_processing.py -i driver_input """
    parser = argparse.ArgumentParser(description='generate output containing script lines from driver_input')
    parser.add_argument('-i',
                        dest='driver_input',
                        default='driver_input',
                        help=' This is the driver_input file')
    parser.add_argument('-nor',
                        dest='NOR',
                        default='False',
                        help='If true the the pdb will not be protonated')

args = parser.parse_args()
nor = args.NOR

main(args.driver_input,nor)