from classes.Case import Case


# Read the whole file, creating a list of Cases, one for each row
def parse_csv(filename):
    LABEL_COL = 4 # TODO: This is hard-coded, but there should be functionality to choose the column (GUI)

    cases = []

    file = open(filename)

    # Read the rest of the lines
    for line in file:
        cases.append(Case(line, LABEL_COL))

    file.close()

    for case in cases:
        print(case.to_string())

    return cases


# Read only the first row of the file, returning a list of the column-separated-values for that row
def read_one(filename):
    file = open(filename)
    line = file.readline()
    file.close()
    return line[0:len(line) - 1].split(",")
    # return ["a", "b", "c", "d", "e"]
