# Machine Learning Project
# By James Quaife: j.quiafe1@nuigalway.ie, SID: 14100104
# and Andrew East: a.east1@nuigalway.ie, SID: 16280042
# National University of Ireland, Galway
# Computer Science CT475: Machine Learning
# November 2018
# Supervisor: Dr. Michael Madden

# Teamwork Attribution: This file was written by James Quiafe

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
