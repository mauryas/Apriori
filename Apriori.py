# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 14:06:22 2017

@author: ShivamMaurya
"""

#from itertools import chain, combinations
from collections import defaultdict
#from optparse import OptionParser

def fetchData(fileName):
    #Read the file and create bag of records
    dataset = open(fileName, 'r')
    finalData = list()
    for data in dataset:
        data = data.rstrip(',')
        data = data.strip('\n')
        splitData = data.split(',')
        for d in splitData:
            if len(d) == 1:
                d = '00'+d
            elif len(d) == 2:
                d = '0'+d
            finalData.append(d)
        records = set(finalData)
        finalData.clear()
        yield records
    return records

def constructBaseSetAndTransBag(records):
    transactionList = list()
    baseSet = set()
    for data in records:
        transactionList.append(data)
        for item in data:
            baseSet.add(frozenset([item]))
    return baseSet, transactionList

def pruneItemSet(elementSet, transactioList, Smin):
    freqElementSet = set()
    supportCounterSet = defaultdict(int)
    
    for t in transactioList:
        for e in elementSet:
            if e.issubset(t):
                supportCounterSet[e] += 1

    for e in elementSet:
        if supportCounterSet[e]>= Smin:
            freqElementSet.add(e)
            
    return freqElementSet
    
def candidate(candidateSet,k):
        freqElementSet = set()
        for i in candidateSet:
            for j in candidateSet:
                newItemSet = i.union(j)
                if len(newItemSet) == k:
                    freqElementSet.add(newItemSet)
        
        return freqElementSet
    
def printResult(globalSet):
    for itemSet in globalSet:
        for item in globalSet[itemSet]:            
            print(list(item).__str__().replace('[','{').replace(']','}'))
        
def apriori(baseSet, transactioList, Smin):
    singleSet = baseSet
    frequentSet = pruneItemSet(singleSet,
                               transactioList, 
                               Smin)
    
    print('Frequent Item Set with Single Item:',len(frequentSet))
    globalSet = dict()
    candidateSet = frequentSet
    k = 2
    while(frequentSet != set([])):
        globalSet[k - 1] = frequentSet
        candidateSet = candidate(candidateSet,k)
        frequentSet = pruneItemSet(candidateSet,
                                   transactioList,
                                   Smin)
        candidateSet = frequentSet
        k+=1
        print("Size:",k)
        print("CandidateSet:",len(candidateSet))
    
#    print(str(globalSet))    
    printResult(globalSet)
    
def main():
    #get a bag of records
    records = fetchData('data/fimi_accident.csv');
    baseSet, transactionList = constructBaseSetAndTransBag(records)
    Smin = 80000
    print('Support:',Smin)
    print('Base Item Set:',len(baseSet))
    apriori(baseSet, transactionList, Smin)
if __name__ == '__main__':
    main()