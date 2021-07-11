import os
from bitarray import bitarray
import copy
#import bitarray
from bitarray import bitdiff
import time
import sys

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

def sort_by_count(t):
    return -t[1]

def greedyadditional_new(testlist, coveragelist, total_count, used, has_change, forward_index, inverted_index):
    addtional_order = []
    total_count_backup = copy.deepcopy(total_count)

    pass_count = 0
    intermediate_timelist = [] 
    for i in range(len(testlist)):
        maxvalue = 0
        maxindex = -1
        for j in range(len(total_count)):
            if total_count[j] > maxvalue and used[j] == False:
                maxvalue = total_count[j]
                maxindex = j
        if maxindex == -1:
            pass_count += 1
            with open(os.path.join(resultpath, 'SequenceGAMethod_' + str(pass_count) + '.txt'),'w') as f:
                for item in addtional_order:
                    f.write(item + '\n')
                remaining_list = []
                for j in range(len(total_count_backup)):
                    if used[j] == False:
                        remaining_list.append((testlist[j], total_count_backup[j]))
                remaining_list_sorted = sorted(remaining_list, key = sort_by_count)
                for testtuple in remaining_list_sorted:
                    f.write(testtuple[0] + '\n')
            thistime = time.time()
            intermediate_timelist.append(thistime)
            total_count = copy.deepcopy(total_count_backup)
            for j in range(len(has_change)):
                has_change[j] = False
            maxvalue = 0
            maxindex = -1
            for j in range(len(total_count)):
                if total_count[j] > maxvalue and used[j] == False:
                    maxvalue = total_count[j]
                    maxindex = j

        if maxindex != -1:
            addtional_order.append(testlist[maxindex])
            used[maxindex] = True
            for j in forward_index[maxindex]:
                if has_change[j] == False:
                    has_change[j] = True
                    for k in inverted_index[j]:
                        total_count[k]-=1
        else:
            for j in range(len(total_count)):
                if used[j] == False:
                    addtional_order.append(testlist[j])
            break
    return [addtional_order, intermediate_timelist]


if __name__ == '__main__':

    category = sys.argv[1]
    assert category in ['opensource', 'industry']
    subject = sys.argv[2]

    rootpath_testlist = os.path.join('../Input_Data/original_input', category, subject)
    subjectalias = subject.replace('-', '').replace('_', '')
    rootpath_coverage = os.path.join('../Input_Data/input_adjlist', subjectalias + '_v1')
    resultpath = os.path.join('../Results/agaresults', subject)
    if not os.path.exists(resultpath):
        os.mkdir(resultpath)

    testlist = readFile(os.path.join(rootpath_testlist, 'testList'))
    coveragelist = readFile(os.path.join(rootpath_coverage, subjectalias + '-line.txt'))

    st0 = time.time()
    used = []
    for i in range(len(coveragelist)):
        used.append(False)

    sloc = 0
    forward_index = []
    for i in range(len(coveragelist)):
        newline = coveragelist[i].strip().split()
        if newline == []:
            forward_index.append([])
            continue
        thismax = max([int(iitem) for iitem in newline])
        if thismax > sloc:
            sloc = thismax
        forward_index.append([int(item) for item in newline])
    sloc = sloc + 1
    inverted_index = []
    has_change = []
    for i in range(sloc):
        has_change.append(False)
        inverted_index.append([])
    for i in range(len(coveragelist)):
        splits = coveragelist[i].strip().split()
        for item in splits:
            inverted_index[int(item)].append(i)
    total_count = [len(ll) for ll in forward_index]
    #st0 = time.time()

    st = time.time()
    pre_time = st - st0
    ga = greedyadditional_new(testlist, coveragelist, total_count, used, has_change, forward_index, inverted_index)
    #ga = greedyadditional(testlist,coveragelist,numberlist)
    #ga = greedyadditional(testlist,coveragelist)
    prioritize_time = time.time() - st
    #print len(ga)
    #raw_input('pause...')
    f = open(os.path.join(resultpath, 'SequenceGAMethod_final.txt'), 'w')
    for item in ga[0]:
        f.write(str(item) + '\n')
    f.close()
    f = open(os.path.join(resultpath, 'TimeGAMethod_adjacencylist'), 'w')
    f.write('pre,' + str(st - st0) + '\n')
    index = -1
    for index in range(len(ga[1])):
        f.write(str(index+1) + ',' + str(ga[1][index] - st) + '\n')
    f.write(str(index+2) + ',' + str(prioritize_time) + '\n')
    f.close()
    print (subject + ' is completed!')

