from parse_csv import parse_csv
from classes.Case import Case
from train import train

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import logging
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        self.winfo_toplevel().title("Decision Tree Machine Learning")

        self.filename = ""
        self.is_file_prepared = False
        self.data_cases = None
        self.trainer = None

    def createWidgets(self):
        self.frame_controls = tk.Frame(self)
        self.frame_controls.pack(side=tk.TOP)

        pack_options_button = {"side": tk.LEFT, "padx": 8, "pady": 8, "ipadx": 4, "ipady": 4}

        self.button_load_file = tk.Button(self.frame_controls)
        self.button_load_file["text"] = "Load Data File"
        self.button_load_file["command"] = self.load_file
        self.image_load_file = tk.PhotoImage(file="images/open.png")
        self.button_load_file["compound"] = tk.LEFT
        self.button_load_file["image"] = self.image_load_file
        self.button_load_file.pack(pack_options_button)

        self.button_train = tk.Button(self.frame_controls)
        self.button_train["text"] = "Train on Data Set"
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
        self.button_next["text"] = "Next"
        # self.button_next["state"] = tk.DISABLED
        # self.button_next["command"] = lambda: messagebox.showinfo("Next", "Next")
        self.button_next["command"] = lambda: self.show_subframe_columns()
        self.image_next = tk.PhotoImage(file="images/next.png")
        self.button_next["compound"] = tk.RIGHT
        self.button_next["image"] = self.image_next
        self.button_next.pack(pack_options_button)

        self.button_save = tk.Button(self.frame_controls)
        self.button_save["text"] = "Save Results"
        # self.button_save["state"] = tk.DISABLED
        # self.button_save["command"] = lambda: messagebox.showinfo("Save", "Save")
        self.button_save["command"] = lambda: self.show_subframe_tree()
        self.image_save = tk.PhotoImage(file="images/save.png")
        self.button_save["compound"] = tk.LEFT
        self.button_save["image"] = self.image_save
        self.button_save.pack(pack_options_button)

        # Frame switching code using tkraise() to bring z-order of frame up: Bryan Oakley (26 September 2011) https://stackoverflow.com/a/7557028/5271224
        self.frame_bottom = tk.Frame(self)
        self.frame_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame_bottom.grid_rowconfigure(0, weight=1)
        self.frame_bottom.grid_columnconfigure(0, weight=1)

        # self.subframe_columns = SubframeColumnSelector(self.frame_bottom, self)
        # self.subframe_columns.grid(row=0, column=0, stick="nsew")

        self.subframe_columns = tk.Frame(self.frame_bottom)
        self.subframe_columns.grid(row=0, column=0, stick="nsew")

        self.subframe_col_options = tk.Frame(self.subframe_columns)
        self.subframe_col_options.pack()
        self.add_col_options(3)

        self.button_process_csv = tk.Button(self.subframe_columns)
        self.button_process_csv["text"] = "Process All Rows"
        self.button_process_csv["command"] = lambda: messagebox.showinfo("process csv", "process csv")
        self.image_process_csv = tk.PhotoImage(file="images/data.png")
        self.button_process_csv["compound"] = tk.LEFT
        self.button_process_csv["image"] = self.image_process_csv
        pack_options_button["side"] = tk.TOP
        self.button_process_csv.pack(pack_options_button)

        self.subframe_tree_canvas = tk.Frame(self.frame_bottom)
        self.subframe_tree_canvas.grid(row=0, column=0, stick="nsew")

        self.tree_canvas = tk.Canvas(self.subframe_tree_canvas, width=600, height=600)
        self.tree_canvas.pack()
        self.tree_canvas.create_rectangle(0, 0, 600, 600, fill="white")

        # self.subframe_columns.tkraise()
        self.show_subframe_columns()
        # todo: DISABLE any controls on hidden frames s.t. they are not controllable, or part of tab order

    def show_subframe_columns(self):
        self.hide_subframe_tree()
        self.button_process_csv["state"] = tk.NORMAL
        self.subframe_columns.tkraise()

    def hide_subframe_columns(self):
        self.button_process_csv["state"] = tk.DISABLED

    def show_subframe_tree(self):
        self.hide_subframe_columns()
        self.subframe_tree_canvas.tkraise()

    def hide_subframe_tree(self):
        pass  # todo

    def add_col_options(self, param):
        pass

    def load_file(self):
        chosen_file = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                   title="Choose a data file",
                                                   filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if chosen_file is not "":
            self.filename = chosen_file  # Temp variable used so cancelling the dialog when a file had already been loaded will not prevent proceeding

            self.is_file_prepared = False
            logging.debug("Preparing to choose attributes for data file: " + self.filename)
            # todo: show attribute picker GUI

    def save_file_attributes(self):
        logging.debug("Loading data file: " + self.filename)
        self.data_cases = parse_csv(self.filename)

        # TOOD: NOTE: copy list w/ objects:
        # import copy
        # new_list = copy.deepcopy(old_list)
        # overridding deepcopy mechanism for classes: __deepcopy__(self): https://docs.python.org/2/library/copy.html

    def train_on_data(self):
        if self.filename is not "":
            self.trainer = train(self.data_cases)
        else:
            messagebox.showwarning("No file loaded", "Cannot train model: no data file has been loaded")


    # todo: About dialog with attribution:
    #   process by popcornarts from the Noun Project
    #       https://thenounproject.com/search/?q=process&i=1056444
    #   open by Landan Lloyd from the Noun Project
    #       https://thenounproject.com/search/?q=open&i=1509580
    #   previous by Three Six Five from the Noun Project
    #       https://thenounproject.com/search/?q=previous&i=1708821
    #   Next by Three Six Five from the Noun Project
    #       https://thenounproject.com/365/uploads/?i=1708819
    #   Save by Sophia Bai from the Noun Project
    #       https://thenounproject.com/search/?q=save&i=1919373
    #   Data by BomSymbols from the Noun Project
    #       https://thenounproject.com/term/data/610617/


class SubframeColumnSelector(tk.Frame):
    def __init(self, parent, app):
        tk.Frame.__init__(self, parent)
        # self.grid(row=0, column=0, stick="nsew")
        # self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.app = app

        pack_options_button = {"side": tk.TOP, "padx": 8, "pady": 8, "ipadx": 4, "ipady": 4}

        self.button_process_csv = tk.Button(self)
        self.button_process_csv["text"] = "Process All Rows"
        self.button_process_csv["command"] = lambda: messagebox.showinfo("process csv", "process csv")
        self.image_process_csv = tk.PhotoImage(file="images/data.png")
        self.button_process_csv["compound"] = tk.LEFT
        self.button_process_csv["image"] = self.image_process_csv
        self.button_process_csv.pack(pack_options_button)

logging.basicConfig(level=logging.DEBUG)

root = tk.Tk()
master_app = Application(master=root)
master_app.mainloop()
