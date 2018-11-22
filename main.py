from parse_csv import parse_csv, read_one
from classes.Case import Case
from about import get_about_message
from split import clone_spliter
from train import train
from graph_tree import create_sample_graph, graph_model

import tkinter as tk
from tkinter import filedialog, messagebox, IntVar

import logging
import os
import base64


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.winfo_toplevel().title("Decision Tree Machine Learning")
        self.pack()

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
        self.button_save["command"] = lambda: self.show_subframe_tree()  # DEBUG
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

        self.subframe_tree_canvas = tk.Frame(self.frame_bottom)
        self.subframe_tree_canvas.grid(row=0, column=0, stick="nsew")

        self.tree_canvas = tk.Canvas(self.subframe_tree_canvas, width=600, height=600)
        self.tree_canvas.pack()
        self.tree_canvas.create_rectangle(0, 0, 600, 600, fill="white")

        self.subframe_columns = tk.Frame(self.frame_bottom)
        self.subframe_columns.grid(row=0, column=0, stick="nsew")

        self.subframe_col_options = tk.Frame(self.subframe_columns)
        self.subframe_col_options.pack()
        self.subframe_col_options_inner = None

        self.button_process_csv = tk.Button(self.subframe_columns)
        self.button_process_csv["text"] = "Read Whole CSV File"
        self.button_process_csv["command"] = self.save_file_attributes
        self.image_process_csv = tk.PhotoImage(file="images/data.png")
        self.button_process_csv["compound"] = tk.LEFT
        self.button_process_csv["image"] = self.image_process_csv
        pack_options_button["side"] = tk.TOP
        self.button_process_csv.pack(pack_options_button)

        self.label_processed_csv = tk.Label(self.subframe_columns,
                                            text="Data set loaded",
                                            font="TkDefaultFont 8 italic")
        # Not packed, so it is hidden

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

    def show_subframe_tree(self):
        self.disable_subframe_columns()
        self.subframe_tree_canvas.tkraise()

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
                                   text="Label", variable=self.cols_radio_var, value=idx)
            radio.grid(row=2, column=idx)
            self.cols_radio_buttons.append(radio)
        self.cols_radio_buttons[num_cols - 1].select()  # Select last in list, since many data sets have the final column as the label

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

            # Made Graph using pydot python objects and return as binary image data
            # self.binary_img_data = create_sample_graph()
            self.binary_img_data = graph_model(self.model)
            # print(self.binary_img_data)

            # Convert to a tkinter picture object
            self.base64_img_data = base64.standard_b64encode(self.binary_img_data)
            # print(self.base64_img_data)
            self.photoimage_img_data = tk.PhotoImage(data=self.base64_img_data)
            # print(self.photoimage_img_data)

            # Show graph pane and paint image
            self.show_subframe_tree()
            self.tree_canvas.create_image(0, 0, image=self.photoimage_img_data, anchor=tk.NW)

    # ##################   Methods called by buttons to do main functionality   ################## #
    def load_file(self):
        chosen_file = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                 title="Choose a data file",
                                                 filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if chosen_file is not "":
            self.filename = chosen_file  # Temp variable used so cancelling the dialog when a file had already been loaded will not prevent proceeding

            self.is_file_prepared = False
            self.label_processed_csv.pack_forget()  # Essentially, hide
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

            if DEBUG:
                print("Metadata for Case: (label col num=" + str(Case.label_column) + ")")
                print(", ".join(Case.attributes_names) + ", label=" + Case.label_name)

            self.master_data_set = parse_csv(self.filename)
            self.label_processed_csv.pack()
            self.button_train["state"] = tk.NORMAL
            self.is_file_prepared = True
        else:
            messagebox.showwarning("No file loaded", "Cannot select file attributes: no data file has been loaded")

    def train_on_data(self):
        if self.master_data_set is not "":
            self.training_set, self.testing_set = clone_spliter(self.master_data_set)

            self.model = train(self.training_set)
        else:
            messagebox.showwarning("No file loaded", "Cannot train model: no data file has been loaded")


DEBUG = True
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

root = tk.Tk()
master_app = Application(master=root)
master_app.mainloop()
