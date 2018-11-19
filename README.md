# Decision Tree Machine Learning

A Python GUI program to learn a predictive machine learning model based on CSV input.
Will use a modified ID3 (Quinlain 1974) decision tree algorithm to generate a model learned on
a training set of the original file. Output will be an image of the generated model, along
with predictions on a testing set of the data using that model.

# Usage

Run `python main.py` to open GUI.

1. Click Load to browser for your CSV data file

1. Fill in column titles for your data, and select the column that holds your category labels

1. Click Read CSV to process the entire file

1. Click Train to generate the model

    * The data will be randomly subdivided in ten different ways, generating ten models from different training sets
    
1. View the different models with the Previous and Next buttons

1. Click Save to choose a directory to output the generated files. Files will be uniquely named based on date & time.

## Prerequisites

## Python 3

Source code has been tested with Python version 3.6

### graphviz

Graphviz is a popular graph-creating library with its own markup language. To generate tree visualisations of the models, this package must be installed on the local machine.

Please follow the download instructions at [graphviz project](https://graphviz.gitlab.io/). The `dot` executable must be available, or graphs will be blank

Note: For a Windows installation, the graphviz `bin` directory must be added to the `PATH` env variable for Python to utilise it.

### pydot

Pydot is an interface used to create graphviz objects in Python code.

Install with `pip install pydot`. Full details at [pydot project](https://github.com/pydot/pydot)
