import sys, csv
e_cutoff = 1e-3

def printHelp():
    print("This is the help text. Helpful, right? :P will change.")


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
            raise Exception("Too many arguments (2 files and 1 output max).")
    return [arguments, file1, file2, output]
            
args = readArgs()


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

def list_line_sort(data, line):
    data.sort(key=lambda x: x[line])
def e_value_sort(data):
    return list_line_sort(data, 2)
def second_file_sort(data):
    return list_line_sort(data, 1)
def first_file_sort(data):
    return list_line_sort(data, 0)

# This flag checking needs to be moved to a place where it will warn the user before doing all the long calculations.
for flag in args[0]:
    if args[0] == []:
        e_value_sort(output)
        break
    if flag[0] == flag[1] == '-':
        if flag == '--help':
            printHelp()
        elif flag == '--sort=e':
            e_value_sort(output)
        elif flag == '--sort=file1':
            first_file_sort(output)
        elif flag == '--sort=file2':
            second_file_sort(output)
        else:
            raise Exception("Unrecognized argument: " + flag + "for help, run with --help")
        break
    elif 'e' in flag:
        e_value_sort(output)
    elif '1' in flag:
        first_file_sort(output)
    elif '2' in flag:
        second_flag_sort(output)
    else:
        raise Exception("Unrecognized argument: " + flag + "for help, run with --help")

        

with open(args[3], 'w+') as outfile:
    for line in output:
        outfile.write(str(line) + '\n')