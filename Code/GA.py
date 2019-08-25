from bitarray import bitarray
import copy
from bitarray import bitdiff
import os.path
import os, errno
import time


def greedyadditional(sametestcase_list,coverage_array,numberlist):
    coverage_row_array = []
    detected_mu = ""
    temp_list = copy.deepcopy(sametestcase_list)
    for i in range(len(coverage_array[0])):
        detected_mu += "0"
    detected_mu_init = detected_mu
    addtional_order = []
    for i in range(len(sametestcase_list)):
        count = 0
        max_number = int(0)
        max_order = int(-1)
        for j in range(len(sametestcase_list)):
            if sametestcase_list[j] not in addtional_order:
                temp_index = testsuitlist_old.index(sametestcase_list[j])
                temp_number = bitdiff(bitarray(detected_mu)&bitarray(coverage_array[j]),bitarray(coverage_array[j]))
                if temp_number > max_number and sametestcase_list[j] not in addtional_order:
                    max_order = j
                    max_number = temp_number
            else:
                continue
        if max_order == int(-1):
            detected_mu = detected_mu_init
            for j in range(len(sametestcase_list)):
                if sametestcase_list[j] not in addtional_order:
                    temp_index = testsuitlist_old.index(sametestcase_list[j])
                    temp_number = bitdiff(bitarray(detected_mu)&bitarray(coverage_array[j]),bitarray(coverage_array[j]))
                    if temp_number > max_number and sametestcase_list[j] not in addtional_order:
                        max_order = j
                        max_number = temp_number
                else:
                    continue
        if max_order != int(-1):
            addtional_order.append(sametestcase_list[max_order])
            temp_list.pop(temp_list.index(sametestcase_list[max_order]))
            detected_mu = bitarray.to01(bitarray(detected_mu)|bitarray(coverage_array[max_order]))
            continue
        elif max_order == int(-1):
            for item in temp_list:
                addtional_order.append(item)
            break
    return addtional_order
