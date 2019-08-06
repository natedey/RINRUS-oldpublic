"""
This is a program written by Qianyi Cheng
at University of Memphis.
"""

import os, sys

def system_run(cmd):
    print(cmd)
    exit = os.system(cmd)
    if ( exit != 0 ):
        print('failed to run:')
        print(cmd)
        sys.exit()
