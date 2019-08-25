from bitarray import bitarray
import copy
from bitarray import bitdiff
import os.path
import os, errno
import time


def sort_by_count(t):
    return -t[1]


def accelerated_greedyadditional(testlist, coveragelist, total_count, used, has_change, forward_index, inverted_index, subject_path):

    addtional_order = []
    total_count_backup = copy.deepcopy(total_count)

    pass_count = 0 # record it has been what times that the matrix were all set to 0 and recover original matrix

    for i in range(len(testlist)):
        maxvalue = 0
        maxindex = -1
        for j in range(len(total_count)):
            if total_count[j] > maxvalue and used[j] == False:
                maxvalue = total_count[j]
                maxindex = j
        if maxindex == -1:
            pass_count += 1
            if pass_count >= 10:
                remaining_list = []
                for j in range(len(total_count_backup)):
                    if used[j] == False:
                        remaining_list.append((testlist[j], total_count_backup[j]))
                remaining_list_sorted = sorted(remaining_list, key = sort_by_count)
                for testtuple in remaining_list_sorted:
                    addtional_order.append(testtuple[0])
                return addtional_order

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

    return addtional_order

