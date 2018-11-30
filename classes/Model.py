class Model:
    def __init__(self):
        self.modelNum = -1
        self.test = []
        self.train = []
        self.treeRoot = None
        

class Tree:
    next_unique_id = -1
    
    def __init__(self):
        self.isLeaf = False
        self.predicted = None
        self.splitAttribute = None
        self.threshold = None
        self.leftChild = None
        self.rightChild = None
        self.unique_id = -1  # Unique identifier needed to make nodes unique in Graphviz node tag strings
        self.numCases = None
        self.numCasesMajorityClass = -1
