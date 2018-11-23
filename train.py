from classes.Case import Case
from classes.Model import Model,Tree


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

    if len(data_cases)==0:
        tree.isLeaf=True
        tree.predicted="Default" #Todo is this correct???
        print("Default")
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
        print("Identify Class")
        return tree
    
    haveFoundAnyNonExamined=False
    for alreadyExamined in data_cases[0].attributesAlreadyExamined:
        if alreadyExamined == False:
            haveFoundAnyNonExamined = True
            
    if haveFoundAnyNonExamined == False:
        tree.isLeaf = True
        max=-1
        maxIndex=0
        for idx,item in enumerate(list(owls.values())):
            if item > max:
                max=item
                maxIndex=idx
        tree.predicted = list(owls.keys())[maxIndex]
        print("No more Attributes")
        return tree              
    
    #Internal Node still needs split
    infoGained = []
    thresholds = []
    for attrib in range(len(Case.attributes_names)):
        if data_cases[0].attributesAlreadyExamined[attrib]:#Look at the logic here! Should be checking it off
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
        
    
    
        
        
        
       
                
