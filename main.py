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
        self.button_launch_load_file = tk.Button(self)
        self.button_launch_load_file["text"] = "Load Data File"
        self.button_launch_load_file["command"] = self.load_file
        self.button_launch_load_file.pack(side=tk.LEFT)

        self.button_train = tk.Button(self)
        self.button_train["text"] = "Train on Data Set"
        self.button_train["command"] = self.train_on_data
        self.button_train.pack(side=tk.LEFT)

        self.button_quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.button_quit.pack(side=tk.BOTTOM)

    def load_file(self):
        # window_load = WindowLoadFile(self)
        # window_load.pack()

        # window_load = tk.Toplevel(self)
        # tk.Label(window_load, text="Hello!").pack()

        window_load = WindowLoadFile(self)
        # window_load = WindowLoadFile(root)


    # def parse_csv(self):
    #     self.data_cases = parse_csv("owls.csv")

    def train_on_data(self):
        self.trainer = train(self.data_cases)


class WindowLoadFile(tk.Toplevel):
    def __init(self, parent):
        # tk.Frame.__init__(self, parent)
        # self.pack()
        # self.create_widgets()

        tk.Toplevel.__init__(self, parent)
        self.title("Load Data File")

        self.frame = tk.Frame(self)
        self.frame.pack()

        self.label = tk.Label(self, text="hello child")
        self.label.pack()

        self.create_widgets()

    def create_widgets(self):
        self.button_read_file = tk.Button(self)
        self.button_read_file["text"] = "Parse 'owls.csv'"
        self.button_read_file["command"] = self.parse_csv
        self.button_read_file.pack(side=tk.LEFT)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
