# Machine Learning Project
# By James Quaife: j.quiafe1@nuigalway.ie, SID: 14100104
# and Andrew East: a.east1@nuigalway.ie, SID: 16280042
# National University of Ireland, Galway
# Computer Science CT475: Machine Learning
# November 2018
# Supervisor: Dr. Michael Madden

# Teamwork Attribution: This file was written by Andrew East

from classes.Case import Case


def parse_csv(filename):
    """
    Read the whole file, creating a list of Cases, one for each row
    Depends on Case.parse_csv_line(self) to do the actual comma separating
    :param filename: str, path to the CSV file to read
    :return: A list of Cases, each one representing a line in the file
    """
    cases = []

    file = open(filename)

    # Read the rest of the lines
    for line in file:
        cases.append(Case(line))

    file.close()

    return cases


def read_one(filename):
    """
    Read only the first row of the file, returning a list of the comma separated values for that row
    :param filename: str, path to the CSV file to read
    :return: A list of strings representing each of the values in the first line
    """
    file = open(filename)
    line = file.readline()
    file.close()
    return line[0:len(line) - 1].split(",")
