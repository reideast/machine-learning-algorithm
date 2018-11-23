class Model:
   

    def __init__(self):
        self.modelNum = -1
        self.test = []
        self.train = []
        self.treeRoot = None
        

    # DEBUG:
    def to_string(self):
        return ", ".join(self.attributes) + ", label=" + self.label
    
class Tree:
    next_debug_id = -1  # DEBUG
    
    def __init__(self):
        self.isLeaf = False
        self.predicted = None
        self.splitAttribute = None
        self.threshold = None
        self.leftChild = None
        self.rightChild = None
        self.debug_id = -1  # DEBUG
        self.numCases = None
