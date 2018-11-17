from readFile import parse_csv

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.read_file = tk.Button(self)
        self.read_file["text"] = "Parse 'owls.csv'"
        self.read_file["command"] = self.parse_csv
        self.read_file.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.QUIT.pack(side="bottom")

    def parse_csv(self):
        parse_csv("owls.csv")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
