from molden_classes import _parse_molden

####################### MULTI OUTPUTFILE  ###########################

class _multioutput(object):

    def __init__(self, jobs=[]):
        self.list_of_jobs=[]
        #self.list_of_content=[]
        for k in jobs:
            self.add(k)

    def add(self,new_job):
        self.list_of_jobs.append(new_job)
        #self.list_of_content.append(new_job.general.jobtype)

    #def remove(self,position=0): #if not specified delete last
    #    del self.list_of_content[position]
    #    del self.list_of_jobs[position]


class _outputfile(object):

    def __init__(self,file_input,silent=False):

        #Check input type
        if type(file_input)==list:
            content = file_input
        else:
            infile = open(file_input, "r")
            content = infile.readlines()

        moldenformat = False

        switch = 0
        for line in content:
            if "MOLDEN_FORMAT".lower() in line.lower():
                moldenformat = True
            if  "Standard Nuclear Orientation" in line:
                break

        if moldenformat:
            self.molden = _parse_molden(content)
            moldenformat = False

