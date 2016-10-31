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

    def print_lines(self):
        self.print_title()
        for line in self.list_of_lines:
            print line

    def print_title(self):
        print self.__title

class _molden_format(object):
    '''
    Standard molden fomrat
    '''
    def __init__(self,molden_type=''):
        self.__molden_type = molden_type
        self.__molden_sections = []
        self.__molden_sections.append(_molden_section('[Molden Format]'))

    def set_type(self,molden_type):
        self.__molden_type = molden_type

    def get_type(self):
        print self.__molden_type

    def add_section(self,molden_section):
        self.__molden_sections.append(molden_section)

    def printme(self):
        for sec in self.__molden_sections:
            sec.print_lines()
       

class _molden(object):
    '''
    Top manager for molden-format outputs
    '''
    def __init__(self,molden_formats):
        self.molden_formats = molden_formats

    def info(self):
        print len(self.molden_formats),"MOLDEN outputs found"

    def output(self,num=0):
        if (num > 0):
            return self.molden_formats[num-1]
        else:
            return len(self.molden_formats)

    def final(self):
        return self.molden_formats[-1]

def _parse_molden(content):
   
    molden_formats = [];
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

    if len(start_of_molden) == len(end_of_molden):
        start_of_molden.reverse()
        end_of_molden.reverse()
    else:
        print "The output might be incomplete"
        import sys
        sys.exit(0)

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

        molden_formats.append(molden_format)

    return _molden(molden_formats)
   
