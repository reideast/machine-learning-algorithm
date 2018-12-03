# Machine Learning Project
# By James Quaife: j.quiafe1@nuigalway.ie, SID: 14100104
# and Andrew East: a.east1@nuigalway.ie, SID: 16280042
# National University of Ireland, Galway
# Computer Science CT475: Machine Learning
# November 2018
# Supervisor: Dr. Michael Madden

# Teamwork Attribution: This file was written by James Quiafe, with some planning and pair programming with Andrew East

from math import log
from typing import List, Dict

from classes.Case import Case
from classes.Model import Model, Tree as DecisionTree, PredictionNode, InternalNode

FLOATING_POINT_EPSILON = 1.0E-13


def train(data_cases: List[Case]) -> Model:
    model = Model()
    model.training_set = data_cases
    model.decision_tree = build_model_tree_recursive(data_cases)
    return model


def build_model_tree_recursive(data_cases: List[Case]) -> DecisionTree:
    """
    Build a model recursively, returning a Tree node each time
    :param data_cases: List of data cases to train this node on (reduced from total training set by ancestors)
    :return: A Tree node
    """
    # tree = DecisionTree()
    # tree.num_cases = len(data_cases)

    # Terminating case 1: No data cases remain
    # TODO: Rework recursive method s.t. parent metadata is passed down, and a tree.predicted + tree.num_cases_majority_class pair can be stored FOR THE PARENT's plurality
    if len(data_cases) == 0:
        tree = PredictionNode(len(data_cases))
        tree.predicted = "Default"
        return tree

    count_classes = count_classes_in_dataset(data_cases)

    # Terminating case 2    
    if len(count_classes) == 1:
        tree = PredictionNode(len(data_cases))
        tree.predicted = list(count_classes.keys())[0]
        return tree

    # Terminating Case 3  
    have_found_any_non_examined = False

    for already_examined in data_cases[0].attributes_already_examined:
        if not already_examined:
            have_found_any_non_examined = True

    if not have_found_any_non_examined:
        tree = PredictionNode(len(data_cases))
        num_in_majority_class = -1
        majority_class_index = 0
        for idx, num_counted in enumerate(list(count_classes.values())):
            if num_counted > num_in_majority_class:
                num_in_majority_class = num_counted
                majority_class_index = idx
        tree.predicted = list(count_classes.keys())[majority_class_index]
        tree.num_cases_majority_class = num_in_majority_class
        return tree

    # This will not be a leaf node, so determine how this internal node should be split
    tree = InternalNode()

    # Find information gains
    info_gains = []
    thresholds = []  # TODO: Support n-ary nodes with n-1 thresholds OR no threshold and n = number of categorical attribute values to EQUAL
    for attrib in range(len(Case.attributes_names)):  # TODO: get len info from Data
        info, threshold = get_best_info_gain_for_attribute(data_cases, attrib)
        # TODO: Is there a way to return a tuple, then deconstruct it into .append() methods?
        info_gains.append(info)
        thresholds.append(threshold)

    # Choose best information gain
    num_in_majority_class = -1.0
    best = -1
    for idx, num_counted in enumerate(info_gains):
        if num_counted > num_in_majority_class:
            num_in_majority_class = num_counted
            best = idx
    tree.split_attribute = best
    tree.threshold = thresholds[best]

    # Build subsets of the data set by splitting at that threshold
    left_list = []
    right_list = []
    for num_counted in data_cases:
        num_counted.attributes_already_examined[best] = True
        if num_counted.attributes[best] < thresholds[best]:
            left_list.append(num_counted)
        else:
            right_list.append(num_counted)
    tree.left_child = build_model_tree_recursive(left_list)
    tree.right_child = build_model_tree_recursive(right_list)

    return tree


def get_best_info_gain_for_attribute(data_cases: List[Case], attrib: int) -> (float, float):
    """
    Determine the best threshold to split this attribute on, as well as the corresponding information gain
    :param data_cases: Dataset remaining for this node
    :param attrib: Index of the attribute column to attempt to split on
    :return: Tuple: Best threshold, best information gain (for that threshold)
    """
    if data_cases[0].attributes_already_examined[attrib]:
        return -1, -1  # This indicates this attribute has actually already been utilised in an ancestor node. -1 will never the largest data gain
    else:
        # Duplicate all values for this attribute in this data subset (so that they can be sorted)
        # TODO: Optimisation: Is there any reason why the whole data_cases List couldn't be sorted?? it's already a duplicated list, only to be used for this node
        all_attribute_values = []
        for data_case in data_cases:
            all_attribute_values.append(data_case.attributes[attrib])
        all_attribute_values.sort()

        potential_info_gains = []
        potential_thresholds = []
        for idx in range(len(all_attribute_values) - 1):
            if all_attribute_values[idx + 1] - all_attribute_values[idx] > FLOATING_POINT_EPSILON:  # This prevents Threshold equalling a data point if data point is duplicate
                mid_value = (all_attribute_values[idx] + all_attribute_values[idx + 1]) / 2
                gain = get_info_gain(data_cases, attrib, mid_value)
                potential_info_gains.append(gain)
                potential_thresholds.append(mid_value)

        if len(potential_info_gains) == 0:
            # When ALL the data_cases have an identical value for attrib, the above guard against duplicates means that there will be NO thresholds returned
            # To prevent breaking the algorithm, make sure to return at least one data point, threshold chosen as the first data case's attrib
            mid_value = all_attribute_values[0]
            gain = get_info_gain(data_cases, attrib, mid_value)
            potential_info_gains.append(gain)
            potential_thresholds.append(mid_value)

        best_info_gain = -1.0
        best = -1
        for idx, potential_info_gain in enumerate(potential_info_gains):
            if potential_info_gain > best_info_gain:
                best_info_gain = potential_info_gain
                best = idx

        return potential_info_gains[best], potential_thresholds[best]  # TODO: swap these


def count_classes_in_dataset(data_cases: List[Case]) -> Dict[str, int]:
    """
    For a dataset, go through each data case and tally their classes
    :param data_cases: List of data cases
    :return: dictionary of label -> count
    """
    classes_counts = {}

    for case in data_cases:
        if case.label in classes_counts:
            classes_counts[case.label] += 1
        else:
            classes_counts[case.label] = 1
    return classes_counts


def get_entropy(classes_counts: Dict[str, int], total_of_all_counts: int) -> float:
    """
    Calculate entropy based on counts of each labelled class and total number of items
    :param classes_counts: Labels and their pre-counted totals. Sum totals = total_of_all_counts
    :param total_of_all_counts: Total data cases. (Note: could be calculated here from sum(each(classes_counts.values())), but it is already known in calling context)
    :return: entropy, [0, 1], where lower means this data set is more homogeneous
    """
    entropy = 0.0
    for item in list(classes_counts.values()):
        p = item / total_of_all_counts
        entropy -= p * log(p, 2)
    return entropy


def get_info_gain(data_cases: List[Case], attrib: int, threshold: float) -> float:
    """
    Calculate the information gained by splitting these data cases into subsets, split upon this attribute at threshold
    :param data_cases: Data set
    :param attrib: Index of the attribute to split on
    :param threshold: Value of this attribute, below which will go to the lft tree
    :return:
    """
    # TODO: Optimisation: Should be able to (verify this) move count_classes and total_entropy out to parent function. These are repeated for EACH potential_threshold
    classes_counts = count_classes_in_dataset(data_cases)
    total_entropy = get_entropy(classes_counts, len(data_cases))

    left_list = []
    right_list = []
    for item in data_cases:
        if item.attributes[attrib] < threshold:
            left_list.append(item)
        else:
            right_list.append(item)
    left_entropy = get_entropy(count_classes_in_dataset(left_list), len(left_list))
    right_entropy = get_entropy(count_classes_in_dataset(right_list), len(right_list))

    return total_entropy - left_entropy * (len(left_list) / len(data_cases)) - right_entropy * (len(right_list) / len(data_cases))
