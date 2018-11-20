from classes.Case import Case
from classes.Model import Model,Tree


def train(data_cases):
    model=Model()
    model.train=data_cases
    print("Begin1" +str(len(data_cases)))
    model.treeRoot=recursive(data_cases)
    print("AllDOne" +str(len(data_cases)))
    
def recursive(data_cases):
    print("Begin2" +str(len(data_cases)))
    tree = Tree()
    if len(data_cases)==0:
        tree.isLeaf=True
        tree.predicted="Default" #Todo is this correct???
        return tree
    owls={}
    
    for case in data_cases:
        if case.label in owls:
            owls[case.label]+=1
        else:
            owls[case.label] = 1 
    if len(owls)==1:
        tree.isLeaf=True
        tree.predicted=list(owls.keys())[0] 
        return tree
    
    allExamined=False
    for isExamined in data_cases[0].attributesAlreadyExamined:
        if isExamined == True:
            allExamined = True
            
    if allExamined == False:
        tree.isLeaf = True
        max=-1
        maxIndex=0
        for idx,item in enumerate(list(owls.values())):
            if item > max:
                max=item
                maxIndex=idx
        tree.predicted = list(owls.keys())[maxIndex]
          
        return tree              
    
    #Internal Node still needs split
    infoGained = []
    thresholds = []
    for attrib in range(len(Case.attributes_names)):
        if data_cases[0].attributesAlreadyExamined[attrib]:
            infoGained.append(-1)
            thresholds.append(-1)
        else:
            print(attrib)
            min = data_cases[0].attributes[attrib]
            max = data_cases[0].attributes[attrib]
            for case in data_cases:
                if min > case.attributes[attrib]:
                    min = case.attributes[attrib]  
                if max < case.attributes[attrib]:
                    max = case.attributes[attrib]  # TODO Calculate information Gained
            infoGained.append(-1)
            thresholds.append((min + max) / 2)
            best=attrib
    # TODO actually choose the best one 
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
    
    
    return tree
        
        
        
       
                
