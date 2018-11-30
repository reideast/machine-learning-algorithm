# Machine Learning Project
# By James Quaife: j.quiafe1@nuigalway.ie, SID: 14100104
# and Andrew East: a.east1@nuigalway.ie, SID: 16280042
# National University of Ireland, Galway
# Computer Science CT475: Machine Learning
# November 2018
# Supervisor: Dr. Michael Madden

# Teamwork Attribution: This file was written by Andrew East

import tkinter as tk
from tkinter import filedialog, messagebox, IntVar, ttk

from datetime import datetime
import os
import logging

from about import get_about_message
from classes.Case import Case, ParseCsvError
from graph_tree import graph_model
from parse_csv import parse_csv, read_one
from split import clone_spliter
from test import test, score
from train import train


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.winfo_toplevel().title("Decision Tree Machine Learning")
        self.pack(fill=tk.BOTH, expand=True)

        self.filename = ""
        self.is_file_prepared = False
        self.trainer = None
        self.master_data_set = None
        self.training_set = []
        self.testing_set = []
        self.model = []
        self.test_score = []
        self.train_score = []
        self.average_test_score = -1.0
        self.graph_photoimage_img_data = []
        self.graph_png_img_data = []
        self.current_results_subframe_shown = -1
        self.can_make_graphs = True

        # ##################   Frame Top: Control Buttons   ################## #
        self.frame_controls = tk.Frame(self)
        self.frame_controls.pack(side=tk.TOP)

        pack_options_button = {"side": tk.LEFT, "padx": 6, "pady": 6, "ipadx": 4, "ipady": 4}

        # DEBUG: Cheater buttons
        self.button_cheat = tk.Button(self.frame_controls)
        self.button_cheat["command"] = self.cheater_shortcut
        self.image_cheat = tk.PhotoImage(file="images/process.png")
        self.button_cheat["image"] = self.image_cheat
        # self.button_cheat.pack({"side": tk.LEFT, "padx": 6, "pady": 6, "ipadx": 5, "ipady": 5})
        self.button_cheat_prev = tk.Button(self.frame_controls)
        self.button_cheat_prev["command"] = lambda: self.show_subframe_columns()
        self.image_cheat_prev = tk.PhotoImage(file="images/previous.png")
        self.button_cheat_prev["image"] = self.image_cheat_prev
        # self.button_cheat_prev.pack({"side": tk.LEFT, "padx": 6, "pady": 6, "ipadx": 5, "ipady": 5})
        self.button_cheat_next = tk.Button(self.frame_controls)
        self.button_cheat_next["command"] = lambda: self.show_subframe_results(0)
        self.image_cheat_next = tk.PhotoImage(file="images/next.png")
        self.button_cheat_next["image"] = self.image_cheat_next
        # self.button_cheat_next.pack({"side": tk.LEFT, "padx": 6, "pady": 6, "ipadx": 5, "ipady": 5})

        self.button_load_file = tk.Button(self.frame_controls)
        self.button_load_file["text"] = "Load Data File"
        self.button_load_file["command"] = self.load_file
        self.image_load_file = tk.PhotoImage(file="images/open.png")
        self.button_load_file["compound"] = tk.LEFT
        self.button_load_file["image"] = self.image_load_file
        self.button_load_file.pack(pack_options_button)

        self.button_train = tk.Button(self.frame_controls)
        self.button_train["text"] = "Train on Data Set"
        self.button_train["state"] = tk.DISABLED
        self.button_train["command"] = self.train_on_data
        self.image_train = tk.PhotoImage(file="images/process.png")
        self.button_train["compound"] = tk.LEFT
        self.button_train["image"] = self.image_train
        self.button_train.pack(pack_options_button)

        self.button_previous = tk.Button(self.frame_controls)
        self.button_previous["text"] = "Previous"
        self.button_previous["state"] = tk.DISABLED
        self.button_previous["command"] = self.show_previous_subframe_results
        self.image_previous = tk.PhotoImage(file="images/previous.png")
        self.button_previous["compound"] = tk.LEFT
        self.button_previous["image"] = self.image_previous
        self.button_previous.pack(pack_options_button)

        self.button_next = tk.Button(self.frame_controls)
        self.button_next["text"] = "Next"
        self.button_next["state"] = tk.DISABLED
        self.button_next["command"] = self.show_next_subframe_results
        self.image_next = tk.PhotoImage(file="images/next.png")
        self.button_next["compound"] = tk.RIGHT
        self.button_next["image"] = self.image_next
        self.button_next.pack(pack_options_button)

        self.button_save = tk.Button(self.frame_controls)
        self.button_save["text"] = "Save Results"
        self.button_save["state"] = tk.DISABLED
        self.button_save["command"] = self.save_results
        self.image_save = tk.PhotoImage(file="images/save.png")
        self.button_save["compound"] = tk.LEFT
        self.button_save["image"] = self.image_save
        self.button_save.pack(pack_options_button)

        self.button_about = tk.Button(self.frame_controls)
        self.button_about["command"] = lambda: messagebox.showinfo("About this Program", get_about_message())
        self.image_about = tk.PhotoImage(file="images/about.png")
        self.button_about["image"] = self.image_about
        self.button_about.pack({"side": tk.LEFT, "padx": 6, "pady": 6, "ipadx": 5, "ipady": 5})

        # ##################   Frame Bottom: Container   ################## #
        # Frame switching code using tkraise() to bring z-order of frame up: Bryan Oakley (26 September 2011) https://stackoverflow.com/a/7557028/5271224
        self.frame_bottom = tk.Frame(self)
        self.frame_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame_bottom.grid_rowconfigure(0, weight=1)
        self.frame_bottom.grid_columnconfigure(0, weight=1)

        # ##################   Frame Bottom: Results   ################## #
        # Subframe to show results of the model; Make ten of them into arrays of GUI elements
        self.subframe_results = []
        self.tree_canvas = []
        self.canvas_img_data = []
        self.label_prediction_score = []
        self.label_training_accuracy = []
        self.label_aggregate_prediction_score = []
        self.scrollframe_table_predictions = []
        self.table_predictions = []
        self.scrollbar_table_prediction = []
        for idx in range(NUM_MODELS):
            self.subframe_results.append(self.make_single_results_frame())

        # ##################   Frame Bottom: Set Input File Options   ################## #
        # Subframe with controls to set the column options
        self.subframe_columns = tk.Frame(self.frame_bottom)
        self.subframe_columns.grid(row=0, column=0, sticky="nsew")

        self.subframe_column_name_inputs_area = tk.LabelFrame(self.subframe_columns, text="Input Column Names and Select Label/Class Column")
        self.subframe_column_name_inputs_area.pack(padx=10, fill=tk.X)

        # Build the subframe which will contain the text input boxes to input column names
        self.subframe_col_options = tk.Frame(self.subframe_column_name_inputs_area)
        self.subframe_col_options.pack()
        self.subframe_col_options_inner = None
        self.cols_labels = None
        self.cols_text_boxes = None
        self.cols_radio_buttons = None
        self.cols_radio_var = None

        self.button_process_csv = tk.Button(self.subframe_column_name_inputs_area)
        self.button_process_csv["text"] = "Load CSV File"
        self.button_process_csv["command"] = self.save_file_attributes
        self.image_process_csv = tk.PhotoImage(file="images/data.png")
        self.button_process_csv["compound"] = tk.LEFT
        self.button_process_csv["image"] = self.image_process_csv
        pack_options_button["side"] = tk.TOP
        self.button_process_csv.pack(pack_options_button)

        self.subframe_inputted_file_area = tk.LabelFrame(self.subframe_columns, text="Data File", padx=5, pady=5)
        self.subframe_inputted_file_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_table_frame = tk.Frame(self.subframe_inputted_file_area, bd=2, relief=tk.SUNKEN)
        self.table_loaded_input = ttk.Treeview(self.input_table_frame, show="headings", columns="message_column")
        self.table_loaded_input.heading("message_column", text="Datafile not loaded yet")
        ttk.Style().layout("Treeview", [])  # Setting the style of all Treeview widgets successfully removes the border to better fit w/ the scrollbar
        self.table_loaded_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.table_scrollbar = tk.Scrollbar(self.input_table_frame)
        self.table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_table_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.table_loaded_input.config(yscrollcommand=self.table_scrollbar.set)
        self.table_scrollbar.config(command=self.table_loaded_input.yview)

        # ##################   Finalise Window Building   ################## #
        self.add_col_options()  # Add default options, no data
        self.show_subframe_columns()

    # ##################   Methods to support switching pages   ################### #

    def show_subframe_columns(self):
        if self.filename is "":
            self.__change_subframe_column_options_input_state(tk.DISABLED)
        else:
            self.__change_subframe_column_options_input_state(tk.NORMAL)
        self.cols_text_boxes[0].focus_set()  # Set focus on first text box so user can immediately start typing
        self.subframe_columns.tkraise()
        self.current_results_subframe_shown = -1

    def disable_subframe_columns(self):
        self.__change_subframe_column_options_input_state(tk.DISABLED)

    def __change_subframe_column_options_input_state(self, state):
        for text in self.cols_text_boxes:
            text["state"] = state
        for radio in self.cols_radio_buttons:
            radio["state"] = state
        self.button_process_csv["state"] = state

    def show_subframe_results(self, idx):
        if self.current_results_subframe_shown < 0:  # Only do the work of disabling input boxes if that frame was already on top
            self.disable_subframe_columns()
        self.subframe_results[idx].tkraise()
        self.current_results_subframe_shown = idx

    def show_previous_subframe_results(self):
        if self.current_results_subframe_shown <= 0:
            self.show_subframe_results(NUM_MODELS - 1)
        else:
            self.show_subframe_results(self.current_results_subframe_shown - 1)

    def show_next_subframe_results(self):
        if self.current_results_subframe_shown >= NUM_MODELS - 1 or self.current_results_subframe_shown < 0:
            self.show_subframe_results(0)
        else:
            self.show_subframe_results(self.current_results_subframe_shown + 1)

    # Add variable number of text/check boxes to input column labels
    def add_col_options(self):
        """
        Generate the text boxes, labels, etc., one for each dataset attribute column
        So that user can input the names for each column
        Destroys existing input boxes within the frame and recreates them
        """
        if self.subframe_col_options_inner is not None:
            self.subframe_col_options_inner.destroy()
        self.subframe_col_options_inner = tk.Frame(self.subframe_col_options)
        self.subframe_col_options_inner.grid()

        if self.filename is not "":
            row = read_one(self.filename)
            num_cols = len(row)
        else:
            num_cols = 4  # generate with four columns by default
            row = [""] * num_cols

        self.cols_labels = []
        self.cols_text_boxes = []
        self.cols_radio_buttons = []
        self.cols_radio_var = IntVar()
        for idx in range(num_cols):
            label = tk.Label(self.subframe_col_options_inner,
                             text="#" + str(idx + 1) + ": " + row[idx])
            label.grid(row=0, column=idx)
            self.cols_labels.append(label)
        for idx in range(num_cols):
            text_box = tk.Entry(self.subframe_col_options_inner, width=(90 // num_cols))
            text_box.grid(row=1, column=idx)
            self.cols_text_boxes.append(text_box)
        for idx in range(num_cols):
            radio = tk.Radiobutton(self.subframe_col_options_inner,
                                   text="Label", variable=self.cols_radio_var, value=idx)
            # TODO: Perhaps add a tooltip (?) here for further explanation
            radio.grid(row=2, column=idx)
            self.cols_radio_buttons.append(radio)
        self.cols_radio_buttons[num_cols - 1].select()  # Select last in list, since many data sets have the final column as the label

        # TODO: Checkbox for each column to mark it as categorical vs. continuous? Will need to rework algorithm s.t. it can handle non-continuous values

        # DEBUG:
        if DEBUG and "owls.csv" in self.filename:  # also guards against filename not being set yet
            for idx, name in enumerate(["body-length", "wing-length", "body-width", "wing-width", "type"]):
                self.cols_text_boxes[idx].insert(0, name)

    def make_single_results_frame(self):
        """
        Generate one of the ten GUI "pages" to hold a graph/table of results
        Appends elements that will be edited later to each of many arrays of GUI elements. (This may be the _least_ pure function I've ever written...)
        """
        subframe_results = tk.Frame(self.frame_bottom)
        subframe_results.grid(row=0, column=0, sticky="nsew")

        canvas_area = tk.LabelFrame(subframe_results, text="Model %d of %d" % (len(self.subframe_results) + 1, NUM_MODELS), padx=5, pady=5)
        canvas_area.pack(padx=10, fill=tk.BOTH, expand=True)

        subframe_tree_canvas = tk.Frame(canvas_area, bd=2, relief=tk.SUNKEN)
        subframe_tree_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        subframe_tree_canvas.grid_rowconfigure(0, weight=1)
        subframe_tree_canvas.grid_columnconfigure(0, weight=1)

        tree_canvas = tk.Canvas(subframe_tree_canvas, bd=0, scrollregion=(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT), background="#FCFEFC")
        self.tree_canvas.append(tree_canvas)
        self.canvas_img_data.append(None)

        scroll_v = tk.Scrollbar(subframe_tree_canvas, orient=tk.VERTICAL)
        scroll_v.grid(row=0, column=1, sticky="ns")
        scroll_v.config(command=tree_canvas.yview)

        scroll_h = tk.Scrollbar(subframe_tree_canvas, orient=tk.HORIZONTAL)
        scroll_h.grid(row=1, column=0, sticky="ew")
        scroll_h.config(command=tree_canvas.xview)

        tree_canvas.config(xscrollcommand=scroll_h.set, yscrollcommand=scroll_v.set)
        tree_canvas.grid(row=0, column=0, sticky="nsew")

        subframe_results_predictions = tk.LabelFrame(subframe_results, text="Predictions %d of %d" % (len(self.subframe_results) + 1, NUM_MODELS), padx=5, pady=5)
        subframe_results_predictions.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)

        subframe_ca_container = tk.Frame(subframe_results_predictions)
        subframe_ca_container.pack(side=tk.LEFT)

        subframe_classification_accuracy = tk.LabelFrame(subframe_ca_container, text="Classification Accuracy", padx=5, pady=5)
        subframe_classification_accuracy.pack(padx=5, pady=5, side=tk.TOP, fill=tk.X)
        label_prediction_score = tk.Label(subframe_classification_accuracy, text="xx.x%", font=("TkDefaultFont", 18), justify=tk.LEFT)
        label_prediction_score.pack()
        self.label_prediction_score.append(label_prediction_score)

        # DEBUG: accuracy of training set
        label_training_accuracy = tk.Label(subframe_classification_accuracy, text="xx.x%", font=("TkDefaultFont", 10), justify=tk.LEFT)
        label_training_accuracy.pack()
        self.label_training_accuracy.append(label_training_accuracy)

        subframe_aggregate_classification_accuracy = tk.LabelFrame(subframe_ca_container, text="Aggregate CA", padx=5, pady=5)
        subframe_aggregate_classification_accuracy.pack(padx=5, pady=5, side=tk.BOTTOM, fill=tk.X)
        label_aggregate_prediction_score = tk.Label(subframe_aggregate_classification_accuracy, text="xx.x%", font=("TkDefaultFont", 14), justify=tk.LEFT)
        label_aggregate_prediction_score.pack()
        self.label_aggregate_prediction_score.append(label_aggregate_prediction_score)

        scrollframe_table_predictions = tk.Frame(subframe_results_predictions, bd=2, relief=tk.SUNKEN)
        table_predictions = ttk.Treeview(scrollframe_table_predictions, height=5, show="headings", columns="message_column")  # Height is number of rows
        table_predictions.heading("message_column", text="Predictions not loaded yet")
        table_predictions.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_table_prediction = tk.Scrollbar(scrollframe_table_predictions)
        scrollbar_table_prediction.pack(side=tk.RIGHT, fill=tk.Y)
        scrollframe_table_predictions.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        table_predictions.config(yscrollcommand=scrollbar_table_prediction.set)
        scrollbar_table_prediction.config(command=table_predictions.yview)
        self.scrollframe_table_predictions.append(scrollframe_table_predictions)
        self.table_predictions.append(table_predictions)
        self.scrollbar_table_prediction.append(scrollbar_table_prediction)

        return subframe_results

    # DEBUG: Load up owls.csv quickly
    def cheater_shortcut(self):
        self.filename = "owls.csv"
        self.add_col_options()
        self.show_subframe_columns()

        self.save_file_attributes()

        self.train_on_data()

    # ##################   Methods called by buttons to do main functionality   ################## #
    def load_file(self):
        chosen_file = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                 title="Choose a data file",
                                                 filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if chosen_file is not "":
            self.filename = chosen_file  # Temp variable used so cancelling the dialog when a file had already been loaded will not prevent proceeding

            self.is_file_prepared = False

            self.table_loaded_input.destroy()
            self.table_loaded_input = ttk.Treeview(self.input_table_frame, show="headings", columns="message_column")
            self.table_loaded_input.heading("message_column", text="Full dataset not yet loaded")
            self.table_loaded_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            # Reconnect scrollbar events to new Treeview object
            self.table_loaded_input.config(yscrollcommand=self.table_scrollbar.set)
            self.table_scrollbar.config(command=self.table_loaded_input.yview)

            Case.label_column = -1
            self.button_train["state"] = tk.DISABLED
            self.button_previous["state"] = tk.DISABLED
            self.button_next["state"] = tk.DISABLED
            self.button_save["state"] = tk.DISABLED
            logging.debug("Preparing to choose attributes for data file: " + self.filename)

            # Recreate column attribute picker GUI elements for user to provide column names
            self.add_col_options()
            self.show_subframe_columns()

    def save_file_attributes(self):
        """
        Gather properties of CSV file from user-inputted GUI elements
        """
        logging.debug("Loading data file: " + self.filename)

        if self.filename is not "":
            Case.attributes_names = []
            Case.label_column = self.cols_radio_var.get()
            for idx, text_box in enumerate(self.cols_text_boxes):
                value = text_box.get()
                if len(value) == 0:
                    value = "column" + str(idx + 1)
                if idx == Case.label_column:
                    Case.label_name = value
                else:
                    Case.attributes_names.append(value)

            # Parse file into list of python objects
            try:
                self.master_data_set = parse_csv(self.filename)
            except ParseCsvError as error:
                tk.messagebox.showerror("Parse CSV Error", "Error while reading file %s\n\nBad line: %s\n\n Item could note be parsed to a float: %s" % (self.filename, error.bad_line, error.bad_item))

            # Show datatable of loaded data
            self.table_loaded_input.destroy()
            col_indices = list(range(len(Case.attributes_names) + 1))  # Make tuple of columns
            self.table_loaded_input = ttk.Treeview(self.input_table_frame, show="headings", columns=col_indices)
            self.table_loaded_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            # Create column headers
            for idx, item in enumerate(Case.attributes_names + [Case.label_name]):  # Label columns
                self.table_loaded_input.column(str(idx), minwidth=5, width=50)
                self.table_loaded_input.heading(str(idx), text=item, anchor="w")

            # Fill table with data from file
            self.table_loaded_input.tag_configure("even", background="#eeeeee")
            for idx, case in enumerate(self.master_data_set):
                self.table_loaded_input.insert("", "end", values=[item for item in case.attributes + [case.label]], tags="even" if idx % 2 == 0 else "")

            # Reconnect scrollbar events to new Treeview object
            self.table_loaded_input.config(yscrollcommand=self.table_scrollbar.set)
            self.table_scrollbar.config(command=self.table_loaded_input.yview)

            # Enable next step in UI flow
            self.button_train["state"] = tk.NORMAL
            self.is_file_prepared = True
        else:
            messagebox.showwarning("No file loaded", "Cannot select file attributes: no data file has been loaded")

    def train_on_data(self):
        if self.master_data_set is not None:
            # TODO: Need to implement some kind of GUI spinner while training is ongoing?

            # Clear previous models before re-training
            self.training_set = []
            self.testing_set = []
            self.model = []
            self.test_score = []
            self.train_score = []
            self.graph_photoimage_img_data = []
            self.graph_png_img_data = []

            # Train, score, and display each model
            col_indices = list(range(len(Case.attributes_names) + 2))  # Make tuple of column names, as defined by user. Same for each loop
            for i in range(NUM_MODELS):
                logging.info("Training model #" + str(i + 1))

                # Get a randomised split of the data set, cloned so the master set remains ready for re-use
                training_set, testing_set = clone_spliter(self.master_data_set)
                self.training_set.append(training_set)
                self.testing_set.append(testing_set)

                # Build that model!
                model = train(training_set)
                self.model.append(model)

                # Test & score on the holdout set, e.g. make predictions
                test(model, testing_set)
                test_score = score(testing_set)
                self.test_score.append(test_score)

                # DEBUG: Also score the training set, which reveals confidence in the algorithm
                test(model, training_set)
                train_score = score(training_set)
                self.train_score.append(train_score)

                if self.can_make_graphs:
                    try:
                        # Make Graph using pydot python objects and return as a tk PhotoImage & PNG
                        graph_photoimage_img_data, graph_png_img_data = graph_model(model)
                        self.graph_photoimage_img_data.append(graph_photoimage_img_data)
                        self.graph_png_img_data.append(graph_png_img_data)

                        # Paint image
                        if self.canvas_img_data[i] is not None:
                            self.tree_canvas[i].delete(self.canvas_img_data[i])  # Remove existing image objects
                        self.canvas_img_data[i] = self.tree_canvas[i].create_image(0, 0, image=graph_photoimage_img_data, anchor=tk.NW)
                        # Reconfigure scrolling area of canvas to the area of the current graph
                        self.tree_canvas[i].config(scrollregion=(0, 0, graph_photoimage_img_data.width(), graph_photoimage_img_data.height()))
                    except OSError as e:
                        if "dot" in e.strerror:
                            logging.error("Graphviz 'dot' executable not found on PATH. No more graphs will be attempted this session")
                            messagebox.showwarning("Graphviz not found", "Graphviz's dot executable was not found.\nPlease install Graphviz, and if on Windows, add the" +
                                                   " Graphviz bin directory to the PATH\n\nNo more graphs will be attempted to be generated during this session, but the" +
                                                   " models can still be tested as normal.")
                            self.can_make_graphs = False
                        else:
                            raise  # This was not the error for "dot not found", so throw it onward

                # Write score
                self.label_prediction_score[i]["text"] = "%.1f%%" % (test_score * 100)
                self.label_training_accuracy[i]["text"] = "Testing Acc: %.1f%%" % (train_score * 100)

                # Put results into datatable
                self.table_predictions[i].destroy()
                self.table_predictions[i] = ttk.Treeview(self.scrollframe_table_predictions[i], height=5, show="headings", columns=col_indices)
                self.table_predictions[i].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                # Create column headers
                for j, item in enumerate(Case.attributes_names):
                    self.table_predictions[i].column(str(j), minwidth=5, width=50)
                    self.table_predictions[i].heading(str(j), text=item, anchor="w")
                for j, item in enumerate([Case.label_name, "Predicted"]):
                    self.table_predictions[i].column(str(j + len(Case.attributes_names)), minwidth=10, width=100)
                    self.table_predictions[i].heading(str(j + len(Case.attributes_names)), text=item, anchor="w")
                # Create table contents
                self.table_predictions[i].tag_configure("even", background="#eeeeee")
                self.table_predictions[i].tag_configure("mismatchEven", background="#eeeeee", foreground="#cc0000")
                self.table_predictions[i].tag_configure("mismatchOdd", foreground="#cc0000")
                for j, case in enumerate(testing_set):
                    self.table_predictions[i].insert("", "end", values=[item for item in case.attributes + [case.label, case.predicted]],
                                                  tags="mismatch" + ("Even" if j % 2 == 0 else "Odd") if case.predicted != case.label else ("even" if j % 2 == 0 else "odd")
                                                  )
                # Reconnect scrollbar events to new Treeview object
                self.table_predictions[i].config(yscrollcommand=self.scrollbar_table_prediction[i].set)
                self.scrollbar_table_prediction[i].config(command=self.table_predictions[i].yview)

            # Calculate aggregate classification accuracy
            total = 0.0
            for test_score in self.test_score:
                total += test_score
            self.average_test_score = total / NUM_MODELS
            for aggregate_result_label in self.label_aggregate_prediction_score:
                aggregate_result_label["text"] = "%.1f%%" % (self.average_test_score * 100)

            # Enable browsing through results and saving all results
            self.button_previous["state"] = tk.NORMAL
            self.button_next["state"] = tk.NORMAL
            self.button_save["state"] = tk.NORMAL

            # Show the first set of results
            self.show_subframe_results(0)
        else:
            messagebox.showwarning("No file loaded", "Cannot train model: no data file has been loaded")

    def save_results(self):
        if len(self.model) != 0:
            # Get now as a datetime string to tag files with
            date_tag = datetime.now().strftime("%y%m%d-%H%M")

            # Make a templating string to build each individual filename later
            filename_template = "results - %s - %%d of %d.%%s" % (date_tag, NUM_MODELS)

            chosen_folder = filedialog.askdirectory(initialdir=os.getcwd(),
                                                    title="Choose directory to save results into, files will be named \"" + filename_template % (0, "csv/png") + "\"")
            if chosen_folder is not "":
                csv_header_row = ",".join(Case.attributes_names + [Case.label_name, "predicted"]) + "\n"
                for idx in range(NUM_MODELS):
                    # Write PNG file out
                    if self.can_make_graphs:  # Don't attempt to write PNGs if Graphviz wasn't installed
                        png_filename = os.path.join(chosen_folder, filename_template % (idx + 1, "png"))
                        with open(png_filename, "wb") as png_file:
                            png_file.write(self.graph_png_img_data[idx])

                    # Write CSV file out
                    csv_filename = os.path.join(chosen_folder, filename_template % (idx + 1, "csv"))
                    with open(csv_filename, "w") as csv_file:
                        csv_file.write(csv_header_row)
                        for case in self.testing_set[idx]:
                            columns = [str(item) for item in case.attributes + [str(case.label), str(case.predicted)]]
                            csv_file.write(",".join(columns) + "\n")
                logging.debug("Files with results and images of models have been saved")
        else:
            messagebox.showwarning("No model trained", "Cannot save model results: no model has been trained")

DEBUG = True
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

NUM_MODELS = 10

root = tk.Tk()
root.minsize(1, 700)  # Must be at least this tall
# root.geometry("1x700")  # DEBUG: weird, very skinny
master_app = Application(master=root)
master_app.mainloop()
