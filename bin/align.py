#!/usr/bin/env python3
import sys, os
from numpy import *
from rms import *

xyz1 = genfromtxt(sys.argv[1],usecols=(1,2,3))
xyz2 = genfromtxt(sys.argv[2],usecols=(1,2,3))

idx1 = array([0,1,2,3])
idx2 = array([16,17,18,19])

c_trans, U, ref_trans = rms_fit(xyz1[idx1],xyz2[idx2])
new_c2 = dot( xyz2-c_trans, U ) + ref_trans

savetxt(sys.argv[3],new_c2, fmt='%.6f')
