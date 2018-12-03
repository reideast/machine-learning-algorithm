# Decision Tree Machine Learning

A Python GUI program to learn a predictive machine learning model based on CSV input.
Will use a modified C4.5 (Quinlain 1974) decision tree algorithm to generate a model learned on
a training set of the original file. Output will be an image of the generated model that would
allow a human to follow the decision tree, along with predictions on a testing set of the data
using that model.

## Usage

Run `python main.py` to open GUI.

1. Click Load Data File to browse for your CSV data file

   * You may change the filter to choose another file type, but if the file is not formatted with
      commas, the program will not be able to recognise columns

1. [Optional] Customise column titles for your data, and select the column that holds your category labels,
   and then click Update Metadata

   * If the program mis-identifies the label column it will show a warning. Simply choose the radio button
     that corresponds to the correct label column.

1. Click Train on Data Set to generate the model

   * The data will be randomly subdivided in ten different ways, generating ten models from these
     different training sets
    
1. View the different models with the Previous and Next buttons. View the training set & predictions, with
   wrong predictions highlighted. View the Classification Accuracy for each model + training set, along with average CA.

1. Click Save Results to choose a directory to output the generated files.

   * There will be ten CSV files with predictions and ten PNG files with a graph visualisation of the decision tree

   * Files will be uniquely named based on date & time, so you can save multiple trained models to the same folder.

## Prerequisites

### Python 3.6

Source code has been tested with Python version 3.6. (Minimum, since type hinting has been used.)

### Graphviz

Graphviz is a popular graph-creating library with its own markup language. To generate tree visualisations of the models, this package must be installed on the local machine.

Please follow the download instructions at the [Graphviz project](https://graphviz.gitlab.io/). The `dot` executable must be available, or the program will issue a warning and the graphs will be blank

Note: For a Windows installation, the Graphviz `bin` directory must be added to the `PATH` env variable for Python to utilise it.

### pydot

Pydot is an adapter used to create Graphviz objects in Python code.

Install with `pip install pydot`. Full details at [pydot project](https://github.com/pydot/pydot)

## About

By James Quaife (j.quiafe1@nuigalway.ie) and Andrew East (a.east1@nuigalway.ie)
