from classes.Case import Case

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
