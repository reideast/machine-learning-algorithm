class Case():
    def __init__(self, csv_line, label_column):
        # self.num_attributes = num_attributes
        self.label_column = label_column
        self.attributes = []
        self.parseCsvLine(csv_line)

    def parseCsvLine(self, csv_line):
        for idx, item in enumerate(csv_line[0:len(csv_line) - 1].split(",")):
            if (idx == self.label_column):
                self.label = item
            else:
                self.attributes.append(item)

    def printCase(self):
        for item in self.attributes:
            print(item, end="; ")
        print("label is '" + self.label + "'")


def parseCsv(filename):
    LABEL_COL = 4
    training_cases = []

    file = open(filename)
    count = 0

    # # Parse just first line to detect how many items there are
    # # this consumes the line so the `for line in file` below will not re-use it
    # firstLine = file.readline()
    # count += 1
    # # case = Case(firstLine, LABEL_COL)
    # training_cases.append(Case(firstLine, LABEL_COL))
    # training_cases[0].printCase()
    # # print("Num items per line=" + str(len(case.attributes)))

    # Read the rest of the lines
    for line in file:
        training_cases.append(Case(line, LABEL_COL))
        count += 1

    file.close()

    for case in training_cases:
        case.printCase()
    print("Number of lines=" + str(count))


