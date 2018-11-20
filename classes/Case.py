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
        if Case.label_column == -1:
            raise Exception("Cannot parse CSV file until properties of file have been chosen")

        # Loop through each comma-separated item in the line, after first truncating the newline from the end
        for idx, item in enumerate(csv_line[0:len(csv_line) - 1].split(",")):
            if idx == Case.label_column:
                self.label = item
            else:
                self.attributes.append(float(item))
                self.attributesAlreadyExamined.append(False)
        self.predicted = None

    # DEBUG:
    def to_string(self):
        return ", ".join(self.attributes) + ", label=" + self.label
