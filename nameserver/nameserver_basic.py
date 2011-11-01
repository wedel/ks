#nameserver.py

import sys

database = {}

def resolve(name):
    if name in database:
        print database[name]
    else:
        print 0
        
def readin():
    file = open('database.txt', "r")
    for line in file:
        line = line.split()
        if len(line) > 1:
            nr = line[0]
            name = line[1]
            database[name] = nr
            #print name + ": " + nr

# if called via shell return address of first argument
if __name__ == "__main__" :
    readin()
    resolve(sys.argv[1])

