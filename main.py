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
        self.data_cases = None
        self.trainer = None

    def createWidgets(self):
        pack_options = {"side": tk.LEFT, "padx": 8, "pady": 8, "ipadx": 4, "ipady": 4}

        self.button_load_file = tk.Button(self)
        self.button_load_file["text"] = "Load Data File"
        self.button_load_file["command"] = self.load_file
        self.image_load_file = tk.PhotoImage(file="images/open.png")
        self.button_load_file["compound"] = tk.LEFT
        self.button_load_file["image"] = self.image_load_file
        self.button_load_file.pack(pack_options)

        self.button_train = tk.Button(self)
        self.button_train["text"] = "Train on Data Set"
        self.button_train["command"] = self.train_on_data
        self.image_train = tk.PhotoImage(file="images/process.png")
        self.button_train["compound"] = tk.LEFT
        self.button_train["image"] = self.image_train
        self.button_train.pack(pack_options)

        self.button_previous = tk.Button(self)
        self.button_previous["text"] = "Previous"
        self.button_previous["state"] = tk.DISABLED
        self.button_previous["command"] = lambda: messagebox.showinfo("Previous", "Previous")
        self.image_previous = tk.PhotoImage(file="images/previous.png")
        self.button_previous["compound"] = tk.LEFT
        self.button_previous["image"] = self.image_previous
        self.button_previous.pack(pack_options)

        self.button_next = tk.Button(self)
        self.button_next["text"] = "Next"
        self.button_next["state"] = tk.DISABLED
        self.button_next["command"] = lambda: messagebox.showinfo("Next", "Next")
        self.image_next = tk.PhotoImage(file="images/next.png")
        self.button_next["compound"] = tk.RIGHT
        self.button_next["image"] = self.image_next
        self.button_next.pack(pack_options)

    def load_file(self):
        chosen_file = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                   title="Choose a data file",
                                                   filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if chosen_file is not "":
            self.filename = chosen_file  # Temp variable used so cancelling the dialog when a file had already been loaded will not prevent proceeding

            logging.debug("Loading data file: " + self.filename)
            self.data_cases = parse_csv(self.filename)

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

logging.basicConfig(level=logging.DEBUG)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
