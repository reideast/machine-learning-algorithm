from classes.Case import Case
from classes.Model import Model,Tree
from math import log


def train(data_cases):
    model=Model()
    model.train=data_cases
    print("Begin1" +str(len(data_cases)))
    model.treeRoot=recursive(data_cases)
    print("AllDOne" +str(len(data_cases)))
    print("Print Tree")
    printTree(model.treeRoot)

    return model
    
def recursive(data_cases):
    print("Begin2" +str(len(data_cases)))
    tree = Tree()

    Tree.next_debug_id += 1
    tree.debug_id = Tree.next_debug_id

    #Terminating case 1
    if len(data_cases)==0: 
        tree.isLeaf=True
        tree.predicted="Default" #Todo is this correct???
        print("Default")
        return tree
    
    countClasses=countClassesInSet(data_cases)       
    #Terminating case 2    
    if len(countClasses)==1:
        tree.isLeaf=True
        tree.predicted=list(countClasses.keys())[0] 
        print("Identify Class")
        return tree
    
    #Terminating Case 3  
    haveFoundAnyNonExamined=False
      
    for alreadyExamined in data_cases[0].attributesAlreadyExamined:
        if alreadyExamined == False:
            haveFoundAnyNonExamined = True
        
    if haveFoundAnyNonExamined == False:
        tree.isLeaf = True
        max=-1
        maxIndex=0
        for idx,item in enumerate(list(countClasses.values())):
            if item > max:
                max=item
                maxIndex=idx
        tree.predicted = list(countClasses.keys())[maxIndex]+"*****Todo*****"
        print("No more Attributes")
        return tree              
    
    #Internal Node still needs split
    infoGained = []
    thresholds = []
    for attrib in range(len(Case.attributes_names)):
        info,threshold=getBestInfoGain(data_cases,attrib)
        infoGained.append(info)
        thresholds.append(threshold)
        
    #Choose Best One
    max=-1.0
    best=-1
    for idx,item in enumerate(infoGained):
        if item > max:
            max=item
            best=idx
    tree.splitAttribute=best 
    tree.threshold=thresholds[best]
    leftList=[]
    rightList=[]
    for item in data_cases:
        item.attributesAlreadyExamined[best]=True
        if item.attributes[best] < thresholds[best]:
            leftList.append(item)
        else:
            rightList.append(item)
    tree.leftChild=recursive(leftList)
    tree.rightChild=recursive(rightList)            
    
    print("Inner Node Complete")
    return tree

def printTree(root):#this is for testing purposes
    open=[root]
    while len(open)!=0:
        current = open.pop()
        if current.isLeaf:
            print(current.predicted)
        else:
            print("Internal"+str(current.splitAttribute)+" "+str(current.threshold))
            open.append(current.leftChild)
            open.append(current.rightChild)
            
            
def getBestInfoGain(data_cases,attrib):
    
    if data_cases[0].attributesAlreadyExamined[attrib]:
            
        return -1, -1
    else:
        print(attrib)
#         allAttributeValues=[]
#         for item in data_cases:
#             allAttributeValues.append(item.attributes[attrib])
#             
#         allAttributeValues.sort()
#         pInfoGain=[]
#         pThresholds=[]
#         
#         for idx in range(len(allAttributeValues)-1):
#             midValue=(allAttributeValues[idx] + allAttributeValues[idx+1]) / 2
#             gain=infoGain(data_cases, attrib, midValue)
#             pInfoGain.append(gain)
#             pThresholds.append(midValue)
        min = data_cases[0].attributes[attrib]
        max = data_cases[0].attributes[attrib]
        for case in data_cases:
            if min > case.attributes[attrib]:
                min = case.attributes[attrib]  
            if max < case.attributes[attrib]:
                max = case.attributes[attrib]
                
        pInfoGain=[]
        pThresholds=[]
        
        step = (max-min)/100
        current = min
         
        for idx in range(99):
            current+=step
            midValue=current
            gain=infoGain(data_cases, attrib, midValue)
            pInfoGain.append(gain)
            pThresholds.append(midValue)# TODO Calculate information Gained
            
        max=-1.0
        best=-1
        for idx,item in enumerate(pInfoGain):
            if item > max:
                max = item
                best = idx
        
        
       
        return pInfoGain[best],pThresholds[best]
        
def countClassesInSet(data_cases):
    
    countClasses={}
    
    for case in data_cases:
        if case.label in countClasses:
            countClasses[case.label]+=1
        else:
            countClasses[case.label] = 1
    return countClasses

def entropy(countClasses,totalCount):
    sum = 0.0
    for item in list(countClasses.values()):
        p = item / totalCount
        sum -= p*log(p,2)
    return sum

def infoGain(data_cases,attrib,threshold):
    countClasses = countClassesInSet(data_cases)
    totalEntropy = entropy(countClasses,len(data_cases))
    
    leftList=[]
    rightList=[]
    for item in data_cases:
        if item.attributes[attrib] < threshold:
            leftList.append(item)
        else:
            rightList.append(item)
    leftEntropy=entropy(countClassesInSet(leftList),len(leftList))
    rightEntropy=entropy(countClassesInSet(rightList),len(rightList))
    
    return totalEntropy - leftEntropy*(len(leftList)/len(data_cases))-rightEntropy*(len(rightList)/len(data_cases))

    
    
    
    
            
               
                
