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

p = re.compile(r'^.*ladu2.*$')

indexes = []

def lines_generator(placeholder=0):
    with open("tabel.txt", "rt") as f:
        for line in islice(f,0,6 ):
            yield(line)


placeholder=0
mylines = lines_generator()   
print(next(mylines))
