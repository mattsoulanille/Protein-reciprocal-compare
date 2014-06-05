# Fix sorting e values like they are words
import sys, csv
from functools import partial
e_cutoff = 1e-3

def printHelp():
    sys.exit("This is the help text. Helpful, right? :P will change.")

def readArgs():
    file1 = ''
    file2 = ''
    output = ''
    arguments = []
    for each in sys.argv[1:]:
        if each[0] == '-':
            arguments += [each]
        elif file1 == '':
            file1 = each
        elif file2 == '':
            file2 = each
        elif output == '':
            output = each
        else:
            sys.exit("Error: Too many arguments (2 files and 1 output max).")
    return [arguments, file1, file2, output]
            
args = readArgs()

def list_line_sort(data, line):
    data.sort(key=lambda x: x[line])

line = 2
outputMode = 0
prefdict = {"outputMode":0, "sort":2}

def assign(key, value, dictionary):
    dictionary[key] = value
def passign(key, value):
    assign(key, value, prefdict)


flagdict = {"e":partial(passign, "sort", 2), "--sort=e":partial(passign, "sort", 2), "1":partial(passign, "sort", 0), "--sort=file1":partial(passign, "sort", 0), "2":partial(passign, "sort", 1), "--sort=file2":partial(passign, "sort", 1), "--stdout":partial(passign, "outputMode", 1), "s":partial(passign, "outputMode", 1)}

def checkDefined(l, b, e):
    returnlist = []
    for x in range(b, e+1):
        try: l[x]
        except: return False
        if l[x] == '':
            return False
    return True

for arg in args[0]:
    if arg[0] == arg[1] == '-':
        try: flagdict[arg]()
        except: sys.exit("Error: Unknown argument '" + str(arg) + "' Use --help for help.")
    elif arg[0] == '-':
        for letter in arg[1:]:
            try: flagdict[letter]()
            except: sys.exit("Error: Unknown argument '" + str(letter) + "' Use --help for help.")
    else:
        raise Exception("something is very broken D:")
        
        
                

if prefdict["outputMode"] == 0: # Output in file mode
    if checkDefined(args, 1, 3) == False:
        sys.exit("Error: Not enough arguments. Requires two files to compare and a name for an output file.")
elif prefdict["outputMode"] == 1: # Output in stdout mode
    if checkDefined(args, 3, 3) == True:
        sys.exit("Error: Too many arguments. If using stdout as output, no output file name should be given")
    elif checkDefined(args, 1, 2) == False:
        sys.exit("Error: Too few arguments. Two files are required for comparison. No output file when using stdout as output")






def dataToDict(filename):
    d = {}
    e_current = None
    with open(filename, 'r') as csvdata:
        csvreader = csv.reader(csvdata, quotechar="'")
        for row in csvreader:
            if row[0] in d:
                e_current = d[row[0]][1]
            else:
                e_current = None
            if (row[10] < e_cutoff and row[10] < e_current) or e_current == None:
                d[row[0]] = [row[1], row[10]]
    return d

d1 = dataToDict(args[1])
d2 = dataToDict(args[2])
output = []

for iterate in xrange(0, min(len(d1), len(d2))-1):
    seq = d1.keys()[iterate]
    opp = d1[seq][0]
    reciprocal = d2.get(opp, [None])[0]
    if seq == reciprocal:
        outlist = [seq, opp, max(d1[seq][1], d2[opp][1])]
        output.append(outlist)


list_line_sort(output, prefdict["sort"])
if prefdict["outputMode"] == 0:
    with open(args[3], 'w+') as outfile:
        for line in output:
            outfile.write(str(line) + '\n')
elif prefdict["outputMode"] == 1:
    sys.stdout.write(str(output))
