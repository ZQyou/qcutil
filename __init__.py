
######################### STANDARD MODULES ##########################

from copy import deepcopy

############################ CONSTANTS ##############################

import constants

############################# MODULES ###############################

# Then we add some hidden outputfile classes...
from output_classes import _outputfile
from output_classes import _multioutput

########################### FILEHANDLING ############################
        
# This is the main filereading method. It reads all types of supported
# files. All other reading methods are hidden from the user. 

def read(filename,silent=False):
    """
    This method reads Q-Chem input files, output files, and coordinate files (xyz,zmat,txyz). 
    """

    extension = (filename.split("."))[-1]

    # Do we have a Q-Chem outputfile?
    if extension.lower() in ("out", "qcout", "qchem"):

        seperator = []
        with open(filename) as infile:
            for num, line in enumerate(infile):
                if "Welcome to Q-Chem" in line:
                    seperator.append(num)

        N_jobs = len(seperator)

        # Always process the file as it containing multiple jobs
        if N_jobs>0:
            if not silent:
                print "Batch-Outputfile detected."
            infile = open(filename,"r")
            content = infile.readlines()
            seperator.append(len(content))
    
            # Create batch jobfile object
            re_file = _multioutput()
    
            # Populate it with jobs
            for k in range(N_jobs):
                start=seperator[k]+1
                end=seperator[k+1]
                dummylines = content[start:end]
                dummy = _outputfile(dummylines,silent)
                re_file.add(dummy)
            return re_file
    
        # No, it's a single job file    
        #else:
        #    if not silent:
        #        print "Outputfile detected."
        #    return _outputfile(filename,silent)

if __name__ == "__main__":
    print "This file is supposed to be loaded as a module, not as main."
   
   
