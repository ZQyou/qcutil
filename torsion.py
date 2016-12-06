#!/usr/bin/env python

''
'refer to http://chemistry.stackexchange.com/questions/40181/when-calculating-a-dihedral-angle-for-a-chemical-bond-how-is-the-direction-defi'
''
'In a Newman projection the torsion angle is the angle (having an absolute value between 0 and 180 degrees) between bonds to two specified (fiducial) groups, one from the atom nearer (proximal) to the observer and the other from the further (distal) atom. The torsion angle between groups A and D is then considered to be positive if the bond A-B is rotated in a clockwise direction through less than 180 degrees in order that it may eclipse the bond C-D: a negative torsion angle requires rotation in the opposite sense.'
'A-B(proximal)-C-D: A-B to C-D is clockwise rotation (< 180 degrees) then positive'
'A-B(proximal)-C-D: A-B to C-D is counter-clockwise rotation (< 180 degrees) then negative'
''
''


import sys
import numpy as np

if len(sys.argv) == 1:
    print "Usage:",sys.argv[0]," qc.xyz [ index of atom list ]"
    sys.exit(2)

radtod = 180.0/np.pi

xyzfile = sys.argv[1]
atom_list = sys.argv[2:]
atom_list = map(int, atom_list)

atom_crds = np.array([])
content = []
with open(xyzfile,'r') as qcxyz:
    content = qcxyz.readlines()[2:]
    qcxyz.close()

if content and len(atom_list) == 4:
    for i in atom_list:
        x = np.array(content[i-1].split()[1:],dtype='f')
#       print x
        atom_crds = np.concatenate((atom_crds,x))
        
atom_crds = atom_crds.reshape((4,3))
# vector order A-->B-->C-->D  left-han rule?
#               b1  b2  b3
b1 = np.subtract(atom_crds[1,:],atom_crds[0,:])
b2 = np.subtract(atom_crds[2,:],atom_crds[1,:])
b3 = np.subtract(atom_crds[3,:],atom_crds[2,:])

#b1 = -1*b1
#b2 = -1*b2
#b3 = -1*b3

# this calculate A-B-C-D
print "A-B-C-D: ",np.arctan2(np.dot(np.cross(np.cross(b1,b2),np.cross(b2,b3)),b2/np.linalg.norm(b2)),
                 np.dot(np.cross(b1,b2),np.cross(b2,b3)))*radtod

# this actully calculate A-C-B-D
n1 = np.cross(b1,b2)
n1 = n1/np.linalg.norm(n1)
n2 = np.cross(b2,b3)
n2 = n2/np.linalg.norm(n2)

b2 = b2/np.linalg.norm(b2)
m1 = np.cross(n1,b2)

x = np.dot(n1,n2)
y = np.dot(m1,n2)

print "dot(b2,n2) = ", np.dot(b2,n2)
print "x = ", x
print "y = ", y
print "A-C-B-D: ", np.arctan2(y,x)*radtod 

