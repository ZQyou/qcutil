import sys
import re
import json
from pprint import pprint

qcout_file = sys.argv[1]
match_option = None
if len(sys.argv) > 2:
    match_option = sys.argv[2]

with open('qckey.json') as keyfile:
    qckeydb = json.load(keyfile)    # this way is not available in Python 3


qckey_strings = qckeydb["Strings"]
del qckeydb["Strings"]

MATCH_LINE = "This line is here to provide a match."

with open(qcout_file) as qcout:

    content = qcout.readlines()
    len_content = len(content)
    num = 0 

    while num < len_content:
        
        line_count = 0
        line = content[num]

        'Loop over section keys'
        for key in list(qckeydb.keys()):
            pattern = qckeydb[key]["Head"]
            if re.search(pattern,line):
                'Parsing a section'
                if not match_option:
                    print num, line.rstrip()
                num = num + 1
                line_count = line_count + 1
                stop_pattern = qckeydb[key]["End"]
                min_lines = qckeydb[key]["Min"]
                line = content[num]
                while not ( re.search(stop_pattern,line) and line_count > min_lines ):
                    if re.search("\d",line):
                        if match_option:
                            print "$"+key+"$"+line.rstrip()
                            print MATCH_LINE
                        else:
                            print num, line.rstrip()
                    num = num + 1
                    line_count = line_count + 1
                    line = content[num]
                if re.search(stop_pattern,line) and qckeydb[key]["PrintEnd"] and not match_option:
                    print num, line.rstrip()
                 
                break

        'Loop over string keys'
        for key in list(qckey_strings.keys()):
            if re.search(key,line) and qckey_strings[key]:
                if match_option:
                    print "$"+qckey_strings[key]+"$"+line.rstrip()
                    print MATCH_LINE
                else:
                    print num, line.rstrip()
                break

        num = num + 1
