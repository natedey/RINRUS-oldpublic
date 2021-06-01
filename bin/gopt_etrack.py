"""
This is a program written by Qianyi Cheng
at University of Memphis.
"""

import sys, re, os
from read_gout import *


if __name__ == '__main__':
    output = sys.argv[1]
    with open(output) as f:
        lines = f.readlines()
    gaussian_eigen(lines)
