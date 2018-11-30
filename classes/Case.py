# Machine Learning Project
# By James Quaife: j.quiafe1@nuigalway.ie, SID: 14100104
# and Andrew East: a.east1@nuigalway.ie, SID: 16280042
# National University of Ireland, Galway
# Computer Science CT475: Machine Learning
# November 2018
# Supervisor: Dr. Michael Madden

# Teamwork Attribution: This file was written by Andrew East

import logging


class Case:
    # These are class-level variables, a Python idiom similar to "static"
    label_column = -1  # integer, index of label in the CSV file
    attributes_names = []  # list of strings, the user-defined names for each column, all columns but label
    label_name = None  # string, the user-defined name for the label column

    def __init__(self, csv_line):
        self.label = None  # string, the actual class of this data case
        self.predicted = None  # string, the predicted class, if this case is used for testing
        self.attributes = []  # list of strings, all columns but label
        self.attributesAlreadyExamined = []  # list of booleans, same length as self.attributes

        self.__parse_csv_line(csv_line)

    def __parse_csv_line(self, csv_line):
        """
        Use data within csv_line to build up this Case's attributes and label
        :param csv_line: str, should be a line read from a CSV file (and still has the newline character at the end)
        """
        if Case.label_column == -1:
            raise Exception("Cannot parse CSV file until properties of file have been specified to the Case class")

        # Loop through each comma-separated item in the line, after first truncating the newline from the end
        for idx, item in enumerate(csv_line[0:len(csv_line) - 1].split(",")):
            if idx == Case.label_column:
                self.label = item  # Save column tagged as label as a string
            else:
                try:
                    self.attributes.append(float(item))  # Parse each column tagged as an attribute as a float
                except ValueError:
                    logging.error("Cannot parse attribute \"%s\" into a floating-point number" % item)
                    raise ParseCsvError(item, csv_line)
                self.attributesAlreadyExamined.append(False)
        self.predicted = None


class ParseCsvError(Exception):
    def __init__(self, bad_item, bad_line):
        self.bad_item = bad_item
        self.bad_line = bad_line

    def __str__(self):
        return "Error parsing CSV file on line '%s' and item '%s" % (self.bad_line, self.bad_item)
