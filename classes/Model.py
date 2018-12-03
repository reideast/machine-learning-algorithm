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
        self.training_set = []
        self.testing_set = []
        self.decision_tree = None
        

# TODO: isinstance(var, Class) == T/F
class Tree:
    NEXT_UNIQUE_ID = 0

    def __init__(self):
        self.unique_id = -1  # Unique identifier needed to make nodes unique in Graphviz node tag strings


class InternalNode(Tree):
    """
    InternalNode: An internal node of a Decision Tree
    Contains information on which attribute to split upon in this node, and what the criteria are to decide which direction to got on that split
    """
    def __init__(self):
        super().__init__()
        self.splitAttribute = None

        self.threshold = None  # TODO: when implementing sub classes, delete this

        self.leftChild = None  # TODO: Support 1 or 2 split points by allowing (2,3) trees
        self.rightChild = None  # TODO: Support categorical attributes by allowing n-ary trees
        # TODO: When implementing subclasses, make this into a List


class ContinuousSplitNode(InternalNode):
    """
    ContinuousSplitNode: An internal node which splits upon a continuous attribute, int or float
    Splits using threshold values to decide where the split should occur
    """
    def __init__(self):
        super().__init__()
        self.thresholds = []  # len should be n - 1, where n = number of children


class CategoricalSplitNode(InternalNode):
    """
    CategoricalSplitNode: An internal node which splits upon a categorical attribute
    Splits by seeing which category a data case's attribute has
    """
    def __init__(self):
        super().__init__()
        self.childCategories = []  # len should be n, where n = number of children AND n = number of ALL categories for this attribute observed across entire train/test data set


class PredictionNode(Tree):
    """
    PredictionNode: A leaf node of a Decision Tree
    """
    def __init__(self):
        super().__init__()
        self.predicted = None
        self.numCases = -1
        self.numCasesMajorityClass = -1


class PredictionNodeConfidence(PredictionNode):
    """
    PredictionNodeConfidence: A leaf node of a Decision Tree, which store the confidence in this decision (as the % of all classes in the data subset for this node the majority class is)
    Stores the data on the majority class as well as all other classes
    """
    pass
    # TODO: store other labels' counts, too
    # TODO: store if this node is using own plurality (terminating case 2|3) or parent's data set (term. case 1)
    # TODO: Maybe this should just be the parent class, no need for subclass? Or should this be a class just for "parent's plurality (terminating case 1)"
