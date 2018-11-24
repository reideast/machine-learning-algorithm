from classes.Model import Model, Tree
from classes.Case import Case
from typing import List


# TODO: remove ALL type hints for functions...it's a provisional API, only available in python35
def test(model: Model, testing_cases: List[Case]):
    for case in testing_cases:
        __predict(model.treeRoot, case)


def __predict(node: Tree, case: Case):
    if node.isLeaf:
        case.predicted = node.predicted
        # TODO: How to deal with leaves where the majority class is one type, AKA the TODO in the training algorithm
    else:
        if (case.attributes[node.splitAttribute] < node.threshold):
            __predict(node.leftChild, case)
        else:
            __predict(node.rightChild, case)


def score(testing_cases: List[Case]) -> float:
    test_correct = 0
    test_total = 0
    for case in testing_cases:
        print(case.label + "/" + case.predicted, end=",")  # DEBUG
        test_total += 1
        if case.label in case.predicted:
            test_correct += 1

    print("correct=%d / total=%d, %.1f" % (test_correct, test_total, test_correct / test_total))  # DEBUG
    return test_correct / test_total