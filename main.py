from parse_csv import parse_csv, read_one
from classes.Case import Case
from about import get_about_message
from split import clone_spliter
from train import train
from graph_tree import graph_model

import tkinter as tk
from tkinter import filedialog, messagebox, IntVar, ttk

import logging
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.winfo_toplevel().title("Decision Tree Machine Learning")
        self.pack(fill=tk.BOTH, expand=True)

        self.filename = ""
        self.is_file_prepared = False
        self.trainer = None
        self.master_data_set = None
        self.training_set = None
        self.testing_set = None
        self.model = None

        # ##################   Frame Top: Control Buttons   ################## #
        self.frame_controls = tk.Frame(self)
        self.frame_controls.pack(side=tk.TOP)

        pack_options_button = {"side": tk.LEFT, "padx": 6, "pady": 6, "ipadx": 4, "ipady": 4}

        # DEBUG: Cheater buttons
        self.button_cheat = tk.Button(self.frame_controls)
        self.button_cheat["command"] = self.cheater_shortcut
        self.image_cheat = tk.PhotoImage(file="images/process.png")
        self.button_cheat["image"] = self.image_cheat
        self.button_cheat.pack({"side": tk.LEFT, "padx": 6, "pady": 6, "ipadx": 5, "ipady": 5})
        self.button_cheat_graph = tk.Button(self.frame_controls)
        self.button_cheat_graph["command"] = self.cheater_shortcut_graph
        self.image_cheat_graph = tk.PhotoImage(file="images/data.png")
        self.button_cheat_graph["image"] = self.image_cheat_graph
        self.button_cheat_graph.pack({"side": tk.LEFT, "padx": 6, "pady": 6, "ipadx": 5, "ipady": 5})
        self.button_cheat_both = tk.Button(self.frame_controls)
        self.button_cheat_both["command"] = self.cheater_shortcut_both
        self.image_cheat_both = tk.PhotoImage(file="images/next.png")
        self.button_cheat_both["image"] = self.image_cheat_both
        self.button_cheat_both.pack({"side": tk.LEFT, "padx": 6, "pady": 6, "ipadx": 5, "ipady": 5})

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
        self.button_previous["command"] = lambda: messagebox.showinfo("Previous", "Previous")
        self.image_previous = tk.PhotoImage(file="images/previous.png")
        self.button_previous["compound"] = tk.LEFT
        self.button_previous["image"] = self.image_previous
        self.button_previous.pack(pack_options_button)

        self.button_next = tk.Button(self.frame_controls)
        # self.button_next["text"] = "Next"
        # self.button_next["state"] = tk.DISABLED
        # self.button_next["command"] = lambda: messagebox.showinfo("Next", "Next")
        self.button_next["text"] = "flip page"  # DEBUG
        self.button_next["command"] = lambda: self.show_subframe_columns()  # DEBUG
        self.image_next = tk.PhotoImage(file="images/next.png")
        self.button_next["compound"] = tk.RIGHT
        self.button_next["image"] = self.image_next
        self.button_next.pack(pack_options_button)

        self.button_save = tk.Button(self.frame_controls)
        # self.button_save["text"] = "Save Results"
        # self.button_save["state"] = tk.DISABLED
        # self.button_save["command"] = lambda: messagebox.showinfo("Save", "Save")
        self.button_save["text"] = "flip page 2"  # DEBUG
        self.button_save["command"] = lambda: self.show_subframe_results()  # DEBUG
        self.image_save = tk.PhotoImage(file="images/save.png")
        self.button_save["compound"] = tk.LEFT
        self.button_save["image"] = self.image_save
        self.button_save.pack(pack_options_button)

        self.button_about = tk.Button(self.frame_controls)
        self.button_about["command"] = lambda: messagebox.showinfo("About this Program", get_about_message())
        self.image_about = tk.PhotoImage(file="images/about.png")
        self.button_about["image"] = self.image_about
        self.button_about.pack({"side": tk.LEFT, "padx": 6, "pady": 6, "ipadx": 5, "ipady": 5})

        # ##################   Frame Bottom: Results   ################## #
        # Frame switching code using tkraise() to bring z-order of frame up: Bryan Oakley (26 September 2011) https://stackoverflow.com/a/7557028/5271224
        self.frame_bottom = tk.Frame(self)
        self.frame_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame_bottom.grid_rowconfigure(0, weight=1)
        self.frame_bottom.grid_columnconfigure(0, weight=1)

        # Subframe to show results of the model
        self.subframe_results = tk.Frame(self.frame_bottom)
        self.subframe_results.grid(row=0, column=0, sticky="nsew")

        self.canvas_area = tk.LabelFrame(self.subframe_results, text="Model", padx=5, pady=5)
        self.canvas_area.pack(padx=10, fill=tk.BOTH, expand=True)

        self.subframe_tree_canvas = tk.Frame(self.canvas_area, bd=2, relief=tk.SUNKEN)
        self.subframe_tree_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.subframe_tree_canvas.grid_rowconfigure(0, weight=1)
        self.subframe_tree_canvas.grid_columnconfigure(0, weight=1)

        self.tree_canvas = tk.Canvas(self.subframe_tree_canvas, bd=0, scrollregion=(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))

        self.scroll_h = tk.Scrollbar(self.subframe_tree_canvas, orient=tk.HORIZONTAL)
        self.scroll_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_h.config(command=self.tree_canvas.xview)

        self.scroll_v = tk.Scrollbar(self.subframe_tree_canvas, orient=tk.VERTICAL)
        self.scroll_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_v.config(command=self.tree_canvas.yview)

        self.tree_canvas.config(xscrollcommand=self.scroll_h.set, yscrollcommand=self.scroll_v.set)
        self.tree_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.subframe_results_predictions = tk.LabelFrame(self.subframe_results, text="Predictions", padx=5, pady=5)
        self.subframe_results_predictions.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)
        # DEBUG: Might this need expand=True, like the file table has -> self.subframe_inputted_file_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.scrollframe_table_predictions = tk.Frame(self.subframe_results_predictions, bd=2, relief=tk.SUNKEN)
        self.table_predictions = ttk.Treeview(self.scrollframe_table_predictions, height=5, show="headings", columns="message_column")  # Height is number of rows
        self.table_predictions.heading("message_column", text="Predictions not loaded yet")
        self.table_predictions.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_table_prediction = tk.Scrollbar(self.scrollframe_table_predictions)
        self.scrollbar_table_prediction.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollframe_table_predictions.pack(fill=tk.BOTH, expand=True)
        self.table_predictions.config(yscrollcommand=self.scrollbar_table_prediction.set)
        self.scrollbar_table_prediction.config(command=self.table_predictions.yview)

        # ##################   Frame Bottom: Set Input File Options   ################## #
        # Subframe with controls to set the column options
        self.subframe_columns = tk.Frame(self.frame_bottom)
        self.subframe_columns.grid(row=0, column=0, sticky="nsew")

        self.subframe_column_name_inputs_area = tk.LabelFrame(self.subframe_columns, text="Choose Column Names and Predicted Class")
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
        self.hide_subframe_tree()
        if self.filename is "":
            self.disable_subframe_columns()
        else:
            self.enable_subframe_column_options()
        self.cols_text_boxes[0].focus_set()
        self.subframe_columns.tkraise()

    def disable_subframe_columns(self):
        for text in self.cols_text_boxes:
            text["state"] = tk.DISABLED
        for radio in self.cols_radio_buttons:
            radio["state"] = tk.DISABLED
        self.button_process_csv["state"] = tk.DISABLED

    def enable_subframe_column_options(self):
        for text in self.cols_text_boxes:
            text["state"] = tk.NORMAL
        for radio in self.cols_radio_buttons:
            radio["state"] = tk.NORMAL
        self.button_process_csv["state"] = tk.NORMAL

    def show_subframe_results(self):
        self.disable_subframe_columns()
        self.subframe_results.tkraise()

    def hide_subframe_tree(self):
        pass  # todo: need to disable anything for the tree canvas page?

    # Add variable number of text/check boxes to input column labels
    def add_col_options(self):
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
            text_box = tk.Entry(self.subframe_col_options_inner, width=15)
            text_box.grid(row=1, column=idx)
            self.cols_text_boxes.append(text_box)
        for idx in range(num_cols):
            radio = tk.Radiobutton(self.subframe_col_options_inner,
                                   text="Label", variable=self.cols_radio_var, value=idx)  # TODO: Rework/rename this so it's more obvious as to purpose. Perhaps a tooltip (?)
            radio.grid(row=2, column=idx)
            self.cols_radio_buttons.append(radio)
        self.cols_radio_buttons[num_cols - 1].select()  # Select last in list, since many data sets have the final column as the label

        # TODO: Checkbox for each column to mark it as categorical vs. continuous? Will need to rework algorithm s.t. it can handle non-continuous values

        # DEBUG:
        if DEBUG and "owls.csv" in self.filename:  # also guards against filename not being set yet
            for idx, name in enumerate(["body-length", "wing-length", "body-width", "wing-width", "type"]):
                self.cols_text_boxes[idx].insert(0, name)

    # DEBUG: Load up owls.csv quickly
    def cheater_shortcut(self):
        self.filename = "owls.csv"
        self.add_col_options()
        self.show_subframe_columns()

        self.save_file_attributes()

        self.train_on_data()

    # DEBUG: show graph based on trained data
    def cheater_shortcut_graph(self):
        if self.model is None:
            logging.error("No model yet!")
        else:
            # DEBUG: Show a graph

            # Made Graph using pydot python objects and return as a tk PhotoImage
            self.photoimage_img_data, self.png_img_data = graph_model(self.model)

            # Show graph pane and paint image
            self.show_subframe_results()
            self.tree_canvas.create_image(0, 0, image=self.photoimage_img_data, anchor=tk.NW)

            # Reconfigure scrolling area of canvas to the area of the current graph
            self.tree_canvas.config(scrollregion=(0, 0, self.photoimage_img_data.width(), self.photoimage_img_data.height()))

            # Write PNG file out
            open("graph.png", "wb").write(self.png_img_data)

    def cheater_shortcut_both(self):
        self.cheater_shortcut()
        self.cheater_shortcut_graph()

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
            logging.debug("Preparing to choose attributes for data file: " + self.filename)

            # Recreate column attribute picker GUI elements for user to provide column names
            self.add_col_options()
            self.show_subframe_columns()

    # Gather properties of CSV file from user-inputted GUI elements
    def save_file_attributes(self):
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
            self.master_data_set = parse_csv(self.filename)

            # Show datatable of loaded data
            self.table_loaded_input.destroy()
            col_indices = list(range(len(Case.attributes_names) + 1))  # Make tuple of columns
            self.table_loaded_input = ttk.Treeview(self.input_table_frame, show="headings", columns=col_indices)
            self.table_loaded_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            # Create column headers
            for idx, item in enumerate(Case.attributes_names + [Case.label_name]):  # Label columns
                self.table_loaded_input.column(str(idx), minwidth=10, width=100)
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

            # TODO: loop below 10 times

            # Get a randomised split of the data set, cloned so the master set remains ready for re-use
            self.training_set, self.testing_set = clone_spliter(self.master_data_set)

            # Build that model!
            self.model = train(self.training_set)

            # TODO: Test training data

            # TODO: Build up 10 graph/results view

            # TODO: Switch to first results/graph view
            self.show_subframe_results()

            # Make Graph using pydot python objects and return as a tk PhotoImage & PNG
            self.photoimage_img_data, self.png_img_data = graph_model(self.model)

            # Paint image
            self.tree_canvas.create_image(0, 0, image=self.photoimage_img_data, anchor=tk.NW)
            # Reconfigure scrolling area of canvas to the area of the current graph
            self.tree_canvas.config(scrollregion=(0, 0, self.photoimage_img_data.width(), self.photoimage_img_data.height()))

            # Write score

            # Put results into datatable

            # TODO:     Also, make Prev/Next buttons work
        else:
            messagebox.showwarning("No file loaded", "Cannot train model: no data file has been loaded")

    def show_results(self):
        pass

    def save_results(self):
        # TODO: this is just a stub
        # Write PNG file out
        open("graph.png", "wb").write(self.png_img_data)



DEBUG = True
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

root = tk.Tk()
root.minsize(1, 700)  # Must be at least this tall
# root.geometry("1x700")  # DEBUG: weird, very skinny
master_app = Application(master=root)
master_app.mainloop()
