import os
#path = '/home/tjsntlci/chem/chorismate_sapt/WAT249_added/nohopt_FSAPT'
path = input('What is the path ')
os.chdir(path)
os.system('python3 ~/git/RINRUS/bin/FSAPT/gen-FG-atomIDs.py -p template.pdb -s A:203')
os.chdir('fsapt')
os.system('python3 ~/git/RINRUS/bin/FSAPT/analyze-FG-SAPT.py -path /home/ndyonker/git/psi4/objdir/stage/share/psi4/fsapt/')


