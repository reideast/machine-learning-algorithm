from classes.Case import Case
from classes.Model import Model, Tree
from math import log


def train(data_cases):
    model = Model()
    model.train = data_cases
    model.treeRoot = buildModelTreeRecursive(data_cases)
    return model

    
def buildModelTreeRecursive(data_cases):
    tree = Tree()
    tree.numCases = len(data_cases)

    Tree.next_debug_id += 1
    tree.debug_id = Tree.next_debug_id

    # Terminating case 1
    if len(data_cases) == 0: 
        tree.isLeaf = True
        tree.predicted = "Default" 
        return tree
    
    countClasses = countClassesInSet(data_cases)       
    # Terminating case 2    
    if len(countClasses) == 1:
        tree.isLeaf = True
        tree.predicted = list(countClasses.keys())[0] 
        return tree
    
    # Terminating Case 3  
    haveFoundAnyNonExamined = False
      
    for alreadyExamined in data_cases[0].attributesAlreadyExamined:
        if alreadyExamined == False:
            haveFoundAnyNonExamined = True
        
    if haveFoundAnyNonExamined == False:
        tree.isLeaf = True
        max = -1
        maxIndex = 0
        for idx, item in enumerate(list(countClasses.values())):
            if item > max:
                max = item
                maxIndex = idx
        tree.predicted = list(countClasses.keys())[maxIndex]
        tree.numCasesMajorityClass = max
        return tree              
    
    # Internal Node still needs split
    infoGained = []
    thresholds = []
    for attrib in range(len(Case.attributes_names)):
        info, threshold = getBestInfoGain(data_cases, attrib)
        infoGained.append(info)
        thresholds.append(threshold)
        
    # Choose Best One
    max = -1.0
    best = -1
    for idx, item in enumerate(infoGained):
        if item > max:
            max = item
            best = idx
    tree.splitAttribute = best 
    tree.threshold = thresholds[best]
    leftList = []
    rightList = []
    for item in data_cases:
        item.attributesAlreadyExamined[best] = True
        if item.attributes[best] < thresholds[best]:
            leftList.append(item)
        else:
            rightList.append(item)
    tree.leftChild = buildModelTreeRecursive(leftList)
    tree.rightChild = buildModelTreeRecursive(rightList)            
    
    return tree

   
def getBestInfoGain(data_cases, attrib):
    
    if data_cases[0].attributesAlreadyExamined[attrib]:
            
        return -1, -1  # This is a check to see if attributes have been examined or not for these data cases
    else:
        allAttributeValues = []
        for item in data_cases:
            allAttributeValues.append(item.attributes[attrib])
            
        allAttributeValues.sort()
        pInfoGain = []
        pThresholds = []
        
        for idx in range(len(allAttributeValues) - 1):
            if allAttributeValues[idx + 1] - allAttributeValues[idx] > 0.0001:  # This prevents Threshold equalling a data point if data point is duplicate
                midValue = (allAttributeValues[idx] + allAttributeValues[idx + 1]) / 2
                gain = getInfoGain(data_cases, attrib, midValue)
                pInfoGain.append(gain)
                pThresholds.append(midValue)
            
        max = -1.0
        best = -1
        for idx, item in enumerate(pInfoGain):
            if item > max:
                max = item
                best = idx
       
        return pInfoGain[best], pThresholds[best]

        
def countClassesInSet(data_cases):
    
    countClasses = {}
    
    for case in data_cases:
        if case.label in countClasses:
            countClasses[case.label] += 1
        else:
            countClasses[case.label] = 1
    return countClasses


def getEntropy(countClasses, totalCount):
    sum = 0.0
    for item in list(countClasses.values()):
        p = item / totalCount
        sum -= p * log(p, 2)
    return sum


def getInfoGain(data_cases, attrib, threshold):
    countClasses = countClassesInSet(data_cases)
    totalEntropy = getEntropy(countClasses, len(data_cases))
    
    leftList = []
    rightList = []
    for item in data_cases:
        if item.attributes[attrib] < threshold:
            leftList.append(item)
        else:
            rightList.append(item)
    leftEntropy = getEntropy(countClassesInSet(leftList), len(leftList))
    rightEntropy = getEntropy(countClassesInSet(rightList), len(rightList))
    
    return totalEntropy - leftEntropy * (len(leftList) / len(data_cases)) - rightEntropy * (len(rightList) / len(data_cases))
                
