#!/usr/bin/env python
__author__     = "Zhi-Qiang You"
__copyright__  = "Copyright 2016, Q-Chem, Inc."
__credits__    = ["Zhi-Qiang You"]
__license__    = "GPL"
__version__    = "0.1"
__maintainer__ = "Zhi-Qiang You"
__email__      = "zqyou@q-chem.com"
__status__     = "Alpha"

import sys
import numpy as np

BOHR_IN_A = 0.5291772108

if len(sys.argv[1:]) < 2:
    print "Usage:",sys.argv[0],"qchem_plot_esp qchem_input"
    sys.exit(2)

file_pltesp = sys.argv[1]
file_qcheminp = sys.argv[2]

pltesp = []
qcheminp = []

try:
    f_pltesp = open(file_pltesp)
    f_qcheminp = open(file_qcheminp)
    pltesp = f_pltesp.readlines()
    qcheminp = f_qcheminp.readlines()
except IOError:
    raise

num = 0
is_readchg = 0
extchg = np.array([])
num_extchg = 0

while num < len(qcheminp):
    line = qcheminp[num]
    if "$external_charges" in line:
        is_readchg = 1
        num += 1
        continue
    if is_readchg:
        if "$end" in line:
            break
        else:
            #print line
            num_extchg += 1
            x = np.array(map(float,line.split()[0:4]),dtype='f')
            extchg = np.concatenate((extchg,x))
    num += 1

extchg = extchg.reshape(num_extchg,4)

num = 0
while num < len(pltesp):
    line = pltesp[num]
    if "Grid point positions" in line:
        for head in pltesp[num:4]:
            print head.rstrip()
        num += 4
        continue
   
    x = np.array(map(float,line.split()[0:4]),dtype='f')
    crd = x[0:3]
    esp = x[3]
    for j in xrange(0,num_extchg):
        extchg_crd = extchg[j,0:3]
        d = np.subtract(crd,extchg_crd)
        dist = np.linalg.norm(d) / BOHR_IN_A 
        esp += extchg[j,3]/dist

    print " %16.8E %16.8E %16.8E %16.8E" % (crd[0], crd[1], crd[2], esp)
    num += 1
