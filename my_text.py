import re
from itertools import islice
"""
Read the text file to a list mylist where eache item is a row.

1. Find the start index and end index where lines must be extracted.
2. 
    [index1, index2,.. indexn]

    new_list_1:  mylist[:index1]
    new_list_2: mylist[index1:index2]
    ...
    new_list_3: mylist[indexn:]
"""


def lines_generator(placeholder=0):
    with open("tabel.txt", "rt") as f:
        for line in islice(f,0,6 ):
            yield(line)


placeholder=0
mylines = lines_generator()   

filecontent=[]



def myfunc(mylist):



    for line in mylines:
        if not p.search(line):
            line = line.rstrip('\n')
            line += '\tladu2'
            filecontent.append(line)
        else: 
            pop_index = mylist.index(p.search(line).group(0))
            mylist.pop(pop_index)    
#############################################################################

mylist =  ['ladu2','ladu3','ladu1']
p = re.compile("|".join(mylist))


stock = 'ladu2'

for line in mylines:
    if not p.search(line):
         line = line.rstrip('\n')
         line += '\t' + p.search(line).group(0)
         filecontent.append(line)
    else: 
        pop_index = mylist.index(p.search(line).group(0))
        mylist.pop(pop_index)


print('koik')

