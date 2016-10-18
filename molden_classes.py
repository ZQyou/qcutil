class _molden_section(object):
    '''
    I don't make comment
    '''
    def __init__(self,title='',list_of_lines=[]):
        self.__title = title.rstrip()
        self.list_of_lines = list_of_lines

    ''' shallow copy problem ??
    def add_line(self,line):
        self.list_of_lines.append(line.rstrip())
    '''

    def lines(self):
        print self.__title
        for line in self.list_of_lines:
            print line

    def title(self):
        print self.__title

class _molden_format(object):
    '''
    Standard molden fomrat
    '''
    def __init__(self,molden_type=''):
        self.__molden_type = molden_type
        self.__molden_sections = []

    def set_type(self,molden_type):
        self.__molden_type = molden_type

    def get_type(self):
        print self.__molden_type

    def add_section(self,molden_section):
        self.__molden_sections.append(molden_section)

    def molden_format(self):
        print "[Molden Format]"
        for sec in self.__molden_sections:
            sec.lines()


class _molden(object):
    '''
    Top manager for molden-format outputs
    '''
    def __init__(self,molden_outputs):
        self.molden_outputs = molden_outputs
        self.num_of_outputs = len(molden_outputs)

    def info(self):
        print self.num_of_outputs,"MOLDEN outputs found"

    def print_molden(self,num=0):
        if (num == 0):
            for output in self.molden_outputs:
                output.molden_format()

        else:
            self.molden_outputs[num-1].molden_format()

def _parse_molden(content):
   
    molden_outputs = [];
    start_of_molden = [];
    end_of_molden = [];
    for i, line in enumerate(content):

        if "MOLECULAR ORBITALS IN MOLDEN FORMAT" in line:
            start_of_molden.append(i)
            continue
        if "END OF MOLDEN-FORMAT MOLECULAR ORBITALS" in line:
            end_of_molden.append(i)
            continue
        if "MOLDEN-FORMATTED INPUT FILE FOLLOWS" in line:
            start_of_molden.append(i)
            continue
        if "END OF MOLDEN-FORMATTED INPUT FILE" in line:
            'break here since this is the final molden output'
            end_of_molden.append(i)
            break

    ''' DEBUG
    for i in xrange(len(start_of_molden)):
        print start_of_molden[i], end_of_molden[i]
    '''

    while (start_of_molden):
        
        switch = 0
        title = ''
        molden_lines = []

        for i in xrange(start_of_molden.pop()+1,end_of_molden.pop()-1): 

            if "[Molden Format]" in content[i]:
                molden_format = _molden_format()
                switch = 0
                continue

            if "[Atoms]" in content[i] or "[GTO]" in content[i] or "[MO]" in content[i] or \
               "[GEOCONV]" in content[i] or "[[GEOMETRIES]" in content:
                if switch == 1:
                    molden_section = _molden_section(title,molden_lines)
                    molden_format.add_section(molden_section)
                    molden_lines = []
                title = content[i].rstrip()
                if "[MO]" in content[i]:
                    molden_format.set_type("MO")
                switch = 1
                continue

            molden_lines.append(content[i].rstrip())

        if len(molden_lines) > 0:
            molden_section = _molden_section(title,molden_lines)
            molden_format.add_section(molden_section)

        molden_outputs.append(molden_format)

    return _molden(molden_outputs)
   
