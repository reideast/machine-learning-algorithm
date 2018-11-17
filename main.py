from parse_csv import parse_csv
from classes.Case import Case
from train import train

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import logging


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        self.filename = ""
        self.data_cases = None
        self.trainer = None

    def createWidgets(self):
        self.button_load_file = tk.Button(self)
        self.button_load_file["text"] = "Load Data File"
        self.button_load_file["command"] = self.load_file
        self.button_load_file.pack(side=tk.LEFT)

        self.button_train = tk.Button(self)
        self.button_train["text"] = "Train on Data Set"
        self.button_train["command"] = self.train_on_data
        self.button_train.pack(side=tk.LEFT)

        self.button_quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.button_quit.pack(side=tk.BOTTOM)

    def load_file(self):
        self.filename = filedialog.askopenfilename()
        logging.debug("Loading data file: " + self.filename)

        if self.filename is not "":
            self.data_cases = parse_csv(self.filename)

    def train_on_data(self):
        if self.filename is not "":
            self.trainer = train(self.data_cases)
        else:
            messagebox.showwarning("No file loaded", "Cannot train model: no data file has been loaded")


logging.basicConfig(level=logging.DEBUG)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
