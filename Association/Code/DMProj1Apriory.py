# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""

import pandas as pd
from itertools import combinations


def Apriori(D, min_sup):
    C1, L = find_frequent_1_itemsets(D, min_sup)
    L1 = scan_count(D, L)
    
    freq_itemsets = {}  
    freq_itemsets.update(L1)
    
    k = 1
    
    while L != []:
        k += 1
        C = apriori_gen(L, k)
        temp_save = []
        temp_remove = []
        temp_freq = scan_count(D, C)
        for key in temp_freq.keys():
            if temp_freq[key] / len(data) >= min_sup:
                temp_save.append(key)
            else:
                temp_remove.append(key)
        for key in temp_remove:
            temp_freq.pop(key)
            
        L = temp_save
        L.sort()
        freq_itemsets.update(temp_freq)
        #print(temp_freq)
        #print(L)
        
    return freq_itemsets
        
def find_frequent_1_itemsets(D, min_sup):
    C1 = {}
    for t in D:
        for item in t:
            if item in C1:
                C1[item] += 1.0
            else:
                C1[item] = 1.0
    L1 = [];
    for key in C1.keys():
        if C1[key] / len(data) >= min_sup:
            L1.append(key)
    L1.sort()
    return C1, L1



def scan_count(D, C):
    result = {}
    for c in C:
        result[c] = 0
    # c is tuple or str; the key of dictionary should be tuple or str
    if C != [] and type(C[0]) == str:
        for t in D:
            for c in C:
                if c in t:
                    result[c] += 1.0

    else:
        for t in D:
            for c in C:
                if check_sublist(list(c), t):
                    result[c] += 1.0
    return result

def check_sublist(sub, sup):
    for element in sub:
        if element not in sup:
            return False
    return True


def apriori_gen(pre_freq_itemsets, k):
    # frquent_2_itemset
    candidates = []
    if k == 2:
        for l1 in pre_freq_itemsets:
            for l2 in pre_freq_itemsets:
                if l1 < l2:
                    c = [l1]
                    c.append(l2)
                    candidates.append(c)

    else:
        pre_freq_itemsets = [list(e) for e in pre_freq_itemsets]
        for l1 in pre_freq_itemsets:
            for l2 in pre_freq_itemsets:
                if l1[:-1] == l2[:-1] and l1[-1] < l2[-1]:
                    temp1 = l1[:]
                    temp2 = l2[:]
                    temp1.append(temp2[-1])
                    c = temp1
                    # prune
                    if has_infrequent_subset(c, pre_freq_itemsets, k-1) == False:
                        candidates.append(c)
                    
    C = [tuple(e) for e in candidates]
    return C

def has_infrequent_subset(c, pre_freq_itemsets, k):
    s = list(combinations(c, k))
    s = [list(l) for l in s]
    for i in s:
        if i not in pre_freq_itemsets:
            return True
    return False
#--------------------------------LOAD DATA------------------------------------#
# load data and data preprocessing
data = pd.read_csv('C:/Users/S.Dejbord/Documents/FALL18/DM/Proj1/associationruletestdata.txt',\
                   header = None, sep = '\t')
#print (data.info())
# change the data to the format as "G0_Up"
for i in range(data.shape[1]-1):
    for j in range(data.shape[0]):
        data[i][j] = 'G%s_'%(i+1)+data[i][j]
data = data.values


#----------------------------------PART-1-------------------------------------#

#print len(data)
min_sup_list = [0.7, 0.6, 0.5, 0.4, 0.3]
for min_sup in min_sup_list:
    freq_itemsets = Apriori(data, min_sup)

    keys = list(freq_itemsets.keys())
    
    max_len = 0
    for a in freq_itemsets.keys():
        if type(a) == str:
            l = 1
        else:
            l = len(a)
        if l > max_len:
            max_len = l
    
    print ('Support is set to be {}:'.format(min_sup))
    
#    if max_len == 1:
#        print ('the max-length of frequent itemsets is 1')
#    else:
#        print ('the max-length of frequent itemsets is {}'.format(max_len))
        
    for l in range(max_len):
        count = 0
        if l+1 == 1:
            for k in keys:
                if type(k) == str:
                    count += 1
            print ('the number of length-1 frequent itemsets: {}'.format(count))
        
        if l+1 > 1:
            for k in keys:
                if type(k) == tuple:
                    if len(k) == l+1:
                        count += 1
            print ('the number of length-{} frequent itemsets: {}'.format(l+1, count))



freq_itemsets = Apriori(data, 0.5)

