# Machine Learning Project
# By James Quaife: j.quiafe1@nuigalway.ie, SID: 14100104
# and Andrew East: a.east1@nuigalway.ie, SID: 16280042
# National University of Ireland, Galway
# Computer Science CT475: Machine Learning
# November 2018
# Supervisor: Dr. Michael Madden

# Teamwork Attribution: This file was written by Andrew East
from typing import List

from classes.Case import Case
from classes.Model import Tree, InternalNode, PredictionNode, Model


def test(model: Model, testing_cases: List[Case]) -> None:
    """
    Test a model with a set of data cases by applying the model to make predictions
    :param model: Model, an already fully constructed decision tree model
    :param testing_cases: The list of Cases, which will have their predictions filled in
    """
    for case in testing_cases:
        __predict(model.decision_tree, case)


def __predict(node: Tree, case: Case) -> None:
    """
    Recursive helper function to follow the model's decision tree, according to this testing case's attribute, until a leaf is reached
    :param node: Tree, with either an attribute and threshold to test against and follow to its children, or a leaf node w/ prediction to use
    :param case: Case, the data case which is being predicted
    """
    if isinstance(node, PredictionNode):
        case.predicted = node.predicted
        # Note: If leaf node was not 100% one class, this just predicts the majority class. Which is chosen in 50/50 splits (or 33/33/33, etc) is non-deterministic in our algorithm
    elif isinstance(node, InternalNode):
        if case.attributes[node.splitAttribute] < node.threshold:
            __predict(node.leftChild, case)
        else:
            __predict(node.rightChild, case)
    else:
        raise NotImplementedError("Other node types implemented yet")  # TODO


def score(testing_cases: List[Case]) -> float:
    """
    Get the percentage of testing cases that were correct
    :param testing_cases: A list of Cases, which have already been tested and predictions saved
    :return: float, percentage correct [0,1]
    """
    test_correct = 0
    test_total = 0
    for case in testing_cases:
        test_total += 1
        if case.label == case.predicted:
            test_correct += 1

    return test_correct / test_total
