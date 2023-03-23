#!/usr/bin/env python

"""
FileDiff.py: It identifies the differences between the two files.
"""
__author__      = "Dbad"

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import filecmp
import difflib

class DiffChecker:
    def __init__(self, master):
        self.master = master
        master.title("FileDiff")

        self.panel1 = tk.Text(master, wrap=tk.WORD, width=50, height=20)
        self.panel1.grid(row=0, column=0, sticky="nsew")
        self.panel1.bind("<Button-1>", self.open_file1)

        self.panel2 = tk.Text(master, wrap=tk.WORD, width=50, height=20)
        self.panel2.grid(row=0, column=1, sticky="nsew")
        self.panel2.bind("<Button-1>", self.open_file2)

        self.check_button = tk.Button(master, text="Find differences", command=self.check_diff)
        self.check_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(0, weight=1)

    def open_file1(self, event=None):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file1:
                self.panel1.delete('1.0', 'end')
                self.panel1.insert('1.0', file1.read())

    def open_file2(self, event=None):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file2:
                self.panel2.delete('1.0', 'end')
                self.panel2.insert('1.0', file2.read())

    def check_diff(self):
        text1 = self.panel1.get('1.0', 'end')
        text2 = self.panel2.get('1.0', 'end')

        with open('file1.txt', 'w') as file1:
            file1.write(text1)
        with open('file2.txt', 'w') as file2:
            file2.write(text2)

        compare = filecmp.cmp('file1.txt', 'file2.txt')

        if compare:
            messagebox.showinfo("FileDiff", "The files are equals.")
        else:
            with open('file1.txt', 'r') as file1:
                file1_lines = file1.readlines()
            with open('file2.txt', 'r') as file2:
                file2_lines = file2.readlines()

            diff = difflib.HtmlDiff().make_file(file1_lines, file2_lines)

            with open('diff.html', 'w') as diff_file:
                diff_file.write(diff)

            messagebox.showinfo("FileDiff", "Review the difference in the diff.html file.")

    def show_diff(self):
        with open('diff.html', 'r') as diff_file:
            diff_html = diff_file.read()

        top = tk.Toplevel()
        top.title("Differences founded")
        top.geometry('800x600')

        diff_panel = tk.Text(top, width=120, height=40)
        diff_panel.pack()

        diff_panel.insert('end', diff_html)
# Create main window
root = tk.Tk()
# Create instance of DiffChecker class
diff_checker = DiffChecker(root)
root.geometry('800x600')
# Start the main event loop
root.mainloop()