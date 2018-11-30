import copy
from random import shuffle

TESTING_RATIO = 3


def clone_spliter(master_data_set):
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
