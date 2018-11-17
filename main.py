from readFile import parse_csv
from classes.Case import Case
from train import train

import tkinter as tk


class Application(tk.Frame):
    data_cases = None
    trainer = None

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.read_file = tk.Button(self)
        self.read_file["text"] = "Parse 'owls.csv'"
        self.read_file["command"] = self.parse_csv
        self.read_file.pack(side="top")

        self.train = tk.Button(self)
        self.train["text"] = "Train on Data Set"
        self.train["command"] = self.train_on_data
        self.train.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.QUIT.pack(side="bottom")

    def parse_csv(self):
        self.data_cases = parse_csv("owls.csv")

    def train_on_data(self):
        self.trainer = train(self.data_cases)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
