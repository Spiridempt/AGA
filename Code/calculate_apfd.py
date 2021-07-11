import os
from bitarray import bitarray
import copy
from bitarray import bitdiff
import time
import sys

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

if __name__ == '__main__':
    subject = sys.argv[1]
    root_path = '../Input_Data/original_input/opensource/'
    result_path = '../Results/agaresults/'
    print (subject + ' is beginning!')
    subject_path = os.path.join(root_path, subject)
    testlist = readFile(os.path.join(subject_path, 'testList'))
    testname_testno_dict = {}
    for i in range(len(testlist)):
        testname_testno_dict[testlist[i]] = i
    mutantkillmatrix = readFile(os.path.join(subject_path, 'mutantKillMatrix'))
    testno_testkill_dict = {}
    for i in range(len(mutantkillmatrix)):
        thisline = mutantkillmatrix[i]
        killlist = []
        for j in range(len(thisline)):
            if thisline[j] == '1':
                killlist.append(j)
        testno_testkill_dict[i] = killlist
    writefile = open(os.path.join(result_path, subject, 'apfd_result.csv'), 'w')
    sequencesfiles = os.listdir(os.path.join(result_path, subject))
    for file in sequencesfiles:
        if 'SequenceGAMethod_' in file:
            thissequence = readFile(os.path.join(result_path, subject, file))
            apfd = 0.0
            is_killed = [] # record whether each mutant has been killed by a test case
            for i in range(len(mutantkillmatrix[0])):
                is_killed.append(False)
            for i in range(len(thissequence)):
                thistestno = testname_testno_dict[thissequence[i]]
                killlist = testno_testkill_dict[thistestno]
                for j in killlist:
                    if is_killed[j] == False:
                        is_killed[j] = True
                        apfd += float(i+1)
            apfd = apfd / float(len(mutantkillmatrix)*len(mutantkillmatrix[0]))
            apfd = 1 - apfd + 1/float(2*len(thissequence))
            writefile.write(file.split('_')[1].split('.txt')[0] + ',' + str(apfd) + '\n')
    writefile.close()
    print (subject + ' is completed!')
