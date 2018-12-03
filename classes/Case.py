# Machine Learning Project
# By James Quaife: j.quiafe1@nuigalway.ie, SID: 14100104
# and Andrew East: a.east1@nuigalway.ie, SID: 16280042
# National University of Ireland, Galway
# Computer Science CT475: Machine Learning
# November 2018
# Supervisor: Dr. Michael Madden

# Teamwork Attribution: This file was written by Andrew East

import logging

from typing import List, Any, ClassVar, Union


# TODO: Maybe this could be two classes:
#       Dataset, which holds information on whole dataset: num attributes, names of columns, (maybe List of Cases)
#       Case, which is an individual case. It might be a sub class of Dataset or maybe just stored as List of Cases in Dataset

class Case:
    # These are class-level variables, a Python idiom similar to "static"
    label_column: ClassVar[int] = -1  # integer, index of label in the CSV file
    attributes_names: ClassVar[List[str]] = []  # list of strings, the user-defined names for each column, all columns but label
    attribute_type_is_continuous: ClassVar[List[bool]] = []  # True if continuous, False if categorical. User defined. All columns but label
    # TODO: For categorical attributes, count and store list of observed categories during file parse
    label_name: ClassVar[str] = None  # string, the user-defined name for the label column

    # TODO: In order to store confidence in all classes, even those not observed, store list of all observed labels during file parse

    def __init__(self, csv_line):
        self.label: str = None  # string, the actual class of this data case
        self.predicted: str = None  # string, the predicted class, if this case is used for testing
        self.attributes: List[Union[float, str]] = []  # list of strings, all columns but label
        self.attributes_already_examined: List[bool] = []  # list of booleans, same length as self.attributes

        self.__parse_csv_line(csv_line)

    def __parse_csv_line(self, csv_line: str) -> None:
        """
        Use data within csv_line to build up this Case's attributes and label
        :param csv_line: str, should be a line read from a CSV file (and still has the newline character at the end)
        """
        assert Case.label_column != -1, "Cannot parse CSV file until properties of file have been specified to the Case class"

        # Loop through each comma-separated item in the line, after first truncating the newline from the end
        for idx, item in enumerate(csv_line[0:len(csv_line) - 1].split(",")):
            if idx == Case.label_column:
                self.label = item  # Save column tagged as label as a string
            else:
                try:
                    if Case.attribute_type_is_continuous[idx if idx < Case.label_column else (idx - 1)]:  # Extra index processing is since this idx (0..columns in CSV) is NOT the same idx as for attributes (0...# col - one for the label col)
                        self.attributes.append(float(item))
                    else:
                        self.attributes.append(item)
                except ValueError:
                    logging.error("Cannot parse attribute \"%s\" into a floating-point number" % item)
                    raise ParseCsvError(item, csv_line)
                self.attributes_already_examined.append(False)
        self.predicted = None


class ParseCsvError(Exception):
    def __init__(self, bad_item: Any, bad_line: str):
        self.bad_item = bad_item
        self.bad_line = bad_line

    def __str__(self):
        return "Error parsing CSV file on line '%s' and item '%s" % (self.bad_line, self.bad_item)
