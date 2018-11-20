from classes.Case import Case


def parse_csv(filename):
    """
    Read the whole file, creating a list of Cases, one for each row
    :param filename: String path to the CSV file to read
    :return: List of Cases
    """
    cases = []

    file = open(filename)

    # Read the rest of the lines
    for line in file:
        cases.append(Case(line))

    file.close()

    #for case in cases:
        #print(case.to_string())

    return cases


def read_one(filename):
    """
    Read only the first row of the file, returning a list of the column-separated-values for that row
    :param filename: String path to the CSV file to read
    :return: List of Strings
    """
    file = open(filename)
    line = file.readline()
    file.close()
    return line[0:len(line) - 1].split(",")
