import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry


class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Dokusyo App")


if __name__ == "__main__":
    root = tk.Tk()
    mainWindow = MainWindow(master=root)
    mainWindow.mainloop()
