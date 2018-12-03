# Machine Learning Project
# By James Quaife: j.quiafe1@nuigalway.ie, SID: 14100104
# and Andrew East: a.east1@nuigalway.ie, SID: 16280042
# National University of Ireland, Galway
# Computer Science CT475: Machine Learning
# November 2018
# Supervisor: Dr. Michael Madden

# Teamwork Attribution: This file was written by Andrew East

import copy
from random import shuffle
from typing import List

from classes.Case import Case

TESTING_RATIO = 3


def clone_splitter(master_data_set: List[Case]) -> (List[Case], List[Case]):
    """
    Takes a list, clones it so it can be re-used later, and splits it into sets of size (n - 1)/n and 1/n where n = TESTING_RATIO
    :param master_data_set: A list, which will be deep copied to clone it.
                            If python's standard deepcopy does not go deep enough in the list's objects, then override __deepcopy__(self) in the object class
    :return: A tuple of two lists, the first of which is the larger one
    """
    data_set = copy.deepcopy(master_data_set)

    qty_testing = len(data_set) // TESTING_RATIO

    shuffle(data_set)
    return data_set[qty_testing:], data_set[:qty_testing]
