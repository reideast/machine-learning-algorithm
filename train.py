# Machine Learning Project
# By James Quaife: j.quiafe1@nuigalway.ie, SID: 14100104
# and Andrew East: a.east1@nuigalway.ie, SID: 16280042
# National University of Ireland, Galway
# Computer Science CT475: Machine Learning
# November 2018
# Supervisor: Dr. Michael Madden

# Teamwork Attribution: This file was written by James Quiafe, with some planning and pair programming with Andrew East

from math import log
from typing import List, Dict, Union, Tuple

from classes.Case import Case
from classes.Model import Model, Tree as DecisionTree, PredictionNode, CategoricalSplitNode, ContinuousSplitNode

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
        tree.num_cases_majority_class = len(data_cases)  # How many data cases made it to this node?
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
        for idx, case in enumerate(list(count_classes.values())):
            if case > num_in_majority_class:
                num_in_majority_class = case
                majority_class_index = idx
        tree.predicted = list(count_classes.keys())[majority_class_index]
        tree.num_cases_majority_class = num_in_majority_class
        return tree

    # This will not be a leaf node, so determine how this internal node should be split

    # Find information gains
    info_gain_per_attrib: List[float] = []
    thresholds_per_attrib: List[Union[None, List[float]]] = []  # For each attrib, either have None (categorical split) or have a list of thresholds to split on: may be 1, 2, more (continuous split)
    # TODO: Make thresholds_per_attrib a class: SplitMethod maybe, with subclasses CategoricalSplitMethod & ContninuousSplitMethod? Knows that this is a categ/contin attrib and thresholds if needed
    # TODO: Support n-ary nodes with n-1 thresholds OR no threshold and n = number of categorical attribute values to EQUAL
    for attrib in range(len(Case.attributes_names)):  # TODO: get len info from Data
        if Case.attribute_type_is_continuous[attrib]:
            info, thresholds = get_best_info_gain_for_attribute(data_cases, attrib)
            # TODO: Is there a way to return a tuple, then deconstruct it into .append() methods?
            info_gain_per_attrib.append(info)
            thresholds_per_attrib.append(thresholds)
        else:  # Categorical attribute
            # TODO: determine info gain for a categorical attrib
            # also, push None to thresholds_per_attrib
            # This ensures that the info gain and thresholds Lists stay as parallel arrays
            raise NotImplementedError()

    # Find best information gain
    num_in_majority_class = -1.0
    best_attrib_to_split_on = -1
    for idx, case in enumerate(info_gain_per_attrib):
        if case > num_in_majority_class:
            num_in_majority_class = case
            best_attrib_to_split_on = idx

    # Save best information gain
    if Case.attribute_type_is_continuous[best_attrib_to_split_on]:
        tree = ContinuousSplitNode()
        tree.split_attribute = best_attrib_to_split_on
        subsets = [[]]  # Start with one subset, since num children is num thresholds + 1
        multiple_thresholds = thresholds_per_attrib[best_attrib_to_split_on]
        for split_point in multiple_thresholds:
            tree.thresholds.append(split_point)
            subsets.append([])

        # Build subsets of the data set by splitting at those thresholds
        for case in data_cases:
            case.attributes_already_examined[best_attrib_to_split_on] = True
            for idx, threshold in enumerate(multiple_thresholds):
                if case.attributes[best_attrib_to_split_on] < threshold:
                    subsets[idx].append(case)
                    break
            else:  # else clause on the for loop executes when loop doesn't break: Handles if the attrib is greater than the last threshold. Python!
                subsets[-1].append(case)  # Append to lsat item in list
    else:
        tree = CategoricalSplitNode()
        tree.split_attribute = best_attrib_to_split_on
        # TODO: save category to split on
        # TODO: split into lists
        subsets = []
        raise NotImplementedError()

    # Continue to build model recursively in children nodes with subsets of the data set
    # tree.left_child = build_model_tree_recursive(left_list)
    # tree.right_child = build_model_tree_recursive(right_list)
    for subset in subsets:
        tree.children.append(build_model_tree_recursive(subset))

    return tree


def get_best_info_gain_for_attribute(data_cases: List[Case], attrib: int) -> Tuple[float, List[float]]:
    """
    Determine the best threshold points to split this attribute on, as well as the corresponding information gain
    :param data_cases: Dataset remaining for this node
    :param attrib: Index of the attribute column to attempt to split on
    :return: Tuple: best information gain possible by splitting on this attribute, List of thresholds to split on (1+)
    """
    if data_cases[0].attributes_already_examined[attrib]:
        return -1, [-1]  # This indicates this attribute has actually already been utilised in an ancestor node. -1 will never the largest data gain
    else:
        # Duplicate all values for this attribute in this data subset (so that they can be sorted)
        # TODO: Optimisation: Is there any reason why the whole data_cases List couldn't be sorted and used here?? it's already a duplicated list, only to be used for this node
        all_attribute_values = []
        for data_case in data_cases:
            all_attribute_values.append(data_case.attributes[attrib])
        all_attribute_values.sort()

        # n = num attributes, indices 0..n-1
        # thresholds, i.e. halfway between the nums, are  t
        # a is first_threshold, b is second_threshold for those i,j
        #                                                              n=8
        #   --------------------------------------------------------------
        #   |  0 |t|  1  |t|  2  |t|  3  |t|  4  |t|  5  |t|  6  |t|  7  |
        #   --------------------------------------------------------------
        #     i=0 a j=1  b                                                  first inner loop for i=0
        #     i=0 a                                          j=6  b          last inner loop for i=0
        #                                    i=4 a  j=5  b                  first inner loop for i=4
        #                                    i=4 a           j=6  b          last inner loop for i=4
        #                                           i=5 a    j=6  b         first inner loop for i=5 (and only)

        # for i in range(len(all_attribute_values) - 2):
        #     first_threshold = -all_attribute_values[i] + all_attribute_values[i + 1]
        #     for j in range(i + 1, len(all_attribute_values) - 1):
        #         second_threshold = -all_attribute_values[j] + all_attribute_values[j + 1]
        # ...maybe let's not do it this way

        all_thresholds = []
        for idx in range(len(all_attribute_values) - 1):
            if all_attribute_values[idx + 1] - all_attribute_values[idx] > FLOATING_POINT_EPSILON:  # This prevents Threshold equalling a data point if data point is duplicate
                all_thresholds.append((all_attribute_values[idx] + all_attribute_values[idx + 1]) / 2)

        if len(all_thresholds) == 0:
            # When ALL the data_cases have an identical value for attrib, the above guard against duplicates means that there are NO thresholds to try
            # So, just choose the first date case's attrib as threshold
            gain = get_info_gain(data_cases, attrib, all_attribute_values[0])
            return gain, [all_attribute_values[0]]
        elif len(all_thresholds) == 1:  # Only one threshold, the smallest possible (since this function will only be called when n >= 2)
            gain = get_info_gain(data_cases, attrib, all_thresholds[0])
            return gain, [all_thresholds[0]]
        else:  # At least two thresholds
            # print("Slices:")  # DEBUG
            # print(all_thresholds)
            # print(all_thresholds[:-1])
            # print(all_thresholds[1:]) # replace 1 with i
            potential_info_gains = []
            potential_thresholds = []

            # # DEBUG:
            # print("All thresholds, then first, then last")
            # print(all_thresholds)
            # print(all_thresholds[0:1])
            # print(all_thresholds[0])
            # print(all_thresholds[-1:])
            # print(all_thresholds[-1])

            # One threshold: first
            gain = get_info_gain_multi_thresholds(data_cases, attrib, all_thresholds[0:1])
            potential_info_gains.append(gain)
            potential_thresholds.append([all_thresholds[0]])

            # One threshold: first
            gain = get_info_gain_multi_thresholds(data_cases, attrib, all_thresholds[-1:])
            potential_info_gains.append(gain)
            potential_thresholds.append([all_thresholds[-1]])

            # Two Thresholds, all combinations in between
            for i, first_threshold in enumerate(all_thresholds[:-1]):
                for second_threshold in all_thresholds[i + 1:]:
                    gain = get_info_gain_multi_thresholds(data_cases, attrib, [first_threshold, second_threshold])
                    potential_info_gains.append(gain)
                    potential_thresholds.append([first_threshold, second_threshold])

            best_info_gain = -1.0
            best_idx = -1
            for idx, potential_info_gain in enumerate(potential_info_gains):
                if potential_info_gain > best_info_gain:
                    best_info_gain = potential_info_gain
                    best_idx = idx

            return potential_info_gains[best_idx], potential_thresholds[best_idx]


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


def get_info_gain_multi_thresholds(data_cases: List[Case], attrib: int, multiple_thresholds: List[float]) -> float:
    # TODO: Optimisation: Should be able to (verify this) move count_classes and total_entropy out to parent function. These are repeated for EACH potential_threshold
    classes_counts = count_classes_in_dataset(data_cases)
    total_entropy = get_entropy(classes_counts, len(data_cases))

    # TODO: option A:
    split_lists = [[]]
    for split_point in multiple_thresholds:
        split_lists.append([])
    # TODO B:
    # split_lists = [[] * (len(multiple_thresholds) + 1)]  # Number of split lists is num thresholds + 1
    # TODO C:
    # split_lists = [[] for x in range(len(multiple_thresholds) + 1)]  # Number of split lists is num thresholds + 1
    # print("should be " + str(len(multiple_thresholds) + 1) + " lists inside a list")
    # print(split_lists)
    for case in data_cases:
        for idx, threshold in enumerate(multiple_thresholds):
            if case.attributes[attrib] < threshold:
                split_lists[idx].append(case)
                break
        else:  # else clause on the for loop executes when loop doesn't break: Handles if the attrib is greater than the last threshold. Python!
            split_lists[-1].append(case)

    # Information gain is total entropy for all data points, minus the entropy each split_list gains
    info_gain = total_entropy
    for split_list in split_lists:
        split_entropy = get_entropy(count_classes_in_dataset(split_list), len(split_list))
        info_gain -= split_entropy * (len(split_list) / len(data_cases))

    return info_gain


