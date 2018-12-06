import re
#from itertools import islice


def lines_generator(placeholder=0):
    with open("tabel.txt", "rt") as f:
        #for line in islice(f,0,6 ):
        for line in f:
            yield(line)



filecontent=[]

mylines = lines_generator()   
mylist =  ['ladu2','ladu3','ladu1']
p = re.compile("|".join(mylist))
matched_item = None

for line in mylines:
    if not (matched_item):
        matched_item = p.search(line)
        continue
    else:
        if not p.search(line):
            line = line.rstrip('\n')
            line += '\t' + matched_item.group(0)
            filecontent.append(line)
        else: 
            matched_item = p.search(line)
            pop_index = mylist.index(matched_item.group(0))
            mylist.pop(pop_index)



