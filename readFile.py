class Case:
    def __init__(self, csv_line, label_column):
        self.label_column = label_column  # integer, index of label in the CSV file
        self.label = None  # string, the actual class of this data case
        self.predicted = None  # string, the predicted class, if this case is used for testing
        self.attributes = []  # list of strings, all columns but label
        self.attributesAlreadyExamined = []  # list of booleans, same length as self.attributes

        self.__parse_csv_line(csv_line)

    def __parse_csv_line(self, csv_line):
        # Loop through each comma-separated item in the line, after first truncating the newline from the end
        for idx, item in enumerate(csv_line[0:len(csv_line) - 1].split(",")):
            if idx == self.label_column:
                self.label = item
            else:
                self.attributes.append(item)
                self.attributesAlreadyExamined.append(False)
        self.predicted = None

    def to_string(self):
        return ",".join(self.attributes) + ", label=" + self.label


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
