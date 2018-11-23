import copy
from random import shuffle

TESTING_RATIO = 3


def clone_spliter(master_data_set):
    # Clone data set so it can be re-used for other splits later
    data_set = copy.deepcopy(master_data_set)
    # overriding deepcopy mechanism for classes: __deepcopy__(self): https://docs.python.org/2/library/copy.html

    qty_testing = len(data_set) // TESTING_RATIO

    #shuffle(data_set) #DEBUG for testing and preventing randomness!!
    return data_set[qty_testing:], data_set[:qty_testing]
