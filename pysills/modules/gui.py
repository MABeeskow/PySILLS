#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# gui.py
# Maximilian Beeskow
# 22.06.2021
# ----------------------
#
## MODULES
from modules import data, plotting
from modules import standard
from modules import sample
from modules import statistics
import numpy as np
import scipy
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, Text
import tkinter.filedialog as fd
import os, re
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import time
import sys

# LISTS
list_standards = []
data_standards = []
list_samples = []
data_samples = []

# CLASSES
class Plotting:
    def __init__(self, root, data):
        self.lines = {}
        self.pos = []

        try:
            self.fig.clf()
            self.ax.cla()
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        try:
            if self.canvas:
                self.canvas.destroy()
            if self.toolbar:
                self.toolbar.destroy()
        except AttributeError:
            pass

        self.canvas = None
        self.toolbar = None
        #
        self.color_background = "#FFFFFF"
        self.root = root
        self.data = data
        self.times = self.data. iloc[:, 0]

        self.frame_main = tk.Frame(self.root, bg=self.color_background)
        self.frame_main.place(relwidth=0.8, relheight=0.8, relx=0.01, rely=0.01)
        #
        self.frame_main_check = tk.Frame(self.frame_main, bg=self.color_background)
        self.frame_main_check.place(relwidth=0.10, relheight=0.92, relx=0.90, rely=0.08)
        self.frame_main_plot = tk.Frame(self.frame_main, bg=self.color_background)
        self.frame_main_plot.place(relwidth=0.895, relheight=1.0, relx=0.0, rely=0.0)

        self.names = list(self.data.columns.values)
        self.names.pop(0)
        self._states = {name: tk.BooleanVar(name=name) for name in self.names}
        self._values = {name: self.data[name] for name in self.names}
        self.values = np.array([[self.data[name] for name in self.names]])
        self.y_max = np.amax(self.values)

        btn_select_all = tk.Button(self.frame_main, text="Select all", height=1, width=10, padx=2, pady=2,
                                   fg="#22252D", bg="#F1F1EB",
                                   command=lambda: self.cb_select_all(states=self._states))
        btn_select_all.place(relx=0.9, rely=0.0)
        btn_deselect_all = tk.Button(self.frame_main, text="Deselect all", height=1, width=10, padx=2, pady=2,
                                     fg="#22252D", bg="#F1F1EB",
                                     command=lambda: self.cb_deselect_all(states=self._states))
        btn_deselect_all.place(relx=0.9, rely=0.04)

        self.fig = Figure(figsize=(1,2), facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot()

        for name, state in self._states.items():
            state.set(True)
            cb = tk.Checkbutton(master=self.frame_main_check, variable=state, text=name,
                                height=1, width=15, anchor=tk.W, bg=self.color_background)
            cb.pack()
            state.trace_add("write", self._value_changed)
            if state.get():
                ln = self.ax.plot(self.times, self._values[name], label=name, visible=True)
                self.lines[name] = ln
        self.ax.grid(True)
        self.ax.set_yscale("log")
        self.ax.set_ylim(bottom=100, top=1.5*self.y_max)
        self.ax.set_axisbelow(True)
        self.ax.set_xlabel("x", labelpad=0.5)
        self.ax.set_ylabel("f(x)", labelpad=0.5)
        self.ax.legend(fontsize="x-small", framealpha=1.0, bbox_to_anchor=(0.125, 0.02), loc=3, borderaxespad=0,
                  bbox_transform=plt.gcf().transFigure, ncol=int(len(self._states)/2))
        #
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_main_plot)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_main_plot)
        self.toolbar.config(background=self.color_background)
        self.toolbar._message_label.config(background=self.color_background)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        self.pos.append([event.xdata,event.ydata])
        print("Cursor position:", self.pos)

    def _value_changed(self, name, _, op):
        if self._states[name].get():
            self.lines[name][0].set_visible(True)
        else:
            self.lines[name][0].set_visible(False)
        self.canvas.draw()

    def cb_select_all(self, states):
        for state in states.values():
            state.set(True)
        state.trace_add("write", self._value_changed)
    #
    def cb_deselect_all(self, states):
        for state in states.values():
            state.set(False)
        state.trace_add("write", self._value_changed)

    def plot_csv(self, parent, listbox, list_data, event):
        t = time.process_time()
        id = listbox.curselection()
        dataset = data.Data(filename=list_data[id[0]])
        df = dataset.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
        Plotting(root=parent, data=df)
        elapsed_time = time.process_time() - t
        print("Execution time:", elapsed_time)

class Plotting2:
    def __init__(self, root, listbox):
        t = time.process_time()
        id = listbox.curselection()
        dataset = data.Data(filename=list_standards[id[0]])
        df = dataset.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)

        self.lines = {}

        try:
            self.fig.clf()
            self.ax.cla()
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        try:
            if self.canvas:
                self.canvas.destroy()
            if self.toolbar:
                self.toolbar.destroy()
        except AttributeError:
            pass

        self.canvas = None
        self.toolbar = None
        #
        self.color_background = "#FFFFFF"
        self.root = root
        self.data = data
        self.times = self.data. iloc[:, 0]

        self.frame_main = tk.Frame(self.root, bg=self.color_background)
        self.frame_main.place(relwidth=0.8, relheight=0.8, relx=0.01, rely=0.01)
        #
        self.frame_main_check = tk.Frame(self.frame_main, bg=self.color_background)
        self.frame_main_check.place(relwidth=0.10, relheight=0.92, relx=0.90, rely=0.08)
        self.frame_main_plot = tk.Frame(self.frame_main, bg=self.color_background)
        self.frame_main_plot.place(relwidth=0.895, relheight=1.0, relx=0.0, rely=0.0)

        self.names = list(self.data.columns.values)
        self.names.pop(0)
        self._states = {name: tk.BooleanVar(name=name) for name in self.names}
        self._values = {name: self.data[name] for name in self.names}
        self.values = np.array([[self.data[name] for name in self.names]])
        self.y_max = np.amax(self.values)

        btn_select_all = tk.Button(self.frame_main, text="Select all", height=1, width=10, padx=2, pady=2,
                                   fg="#22252D", bg="#F1F1EB",
                                   command=lambda: self.cb_select_all(states=self._states))
        btn_select_all.place(relx=0.9, rely=0.0)
        btn_deselect_all = tk.Button(self.frame_main, text="Deselect all", height=1, width=10, padx=2, pady=2,
                                     fg="#22252D", bg="#F1F1EB",
                                     command=lambda: self.cb_deselect_all(states=self._states))
        btn_deselect_all.place(relx=0.9, rely=0.04)

        self.fig = Figure(figsize=(1,2), facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot()

        for name, state in self._states.items():
            state.set(True)
            cb = tk.Checkbutton(master=self.frame_main_check, variable=state, text=name,
                                height=1, width=15, anchor=tk.W, bg=self.color_background)
            cb.pack()
            state.trace_add("write", self._value_changed)
            if state.get():
                ln = self.ax.plot(self.times, self._values[name], label=name, visible=True)
                self.lines[name] = ln
        self.ax.grid(True)
        self.ax.set_yscale("log")
        self.ax.set_ylim(bottom=100, top=1.5*self.y_max)
        self.ax.set_axisbelow(True)
        self.ax.set_xlabel("x", labelpad=0.5)
        self.ax.set_ylabel("f(x)", labelpad=0.5)
        self.ax.legend(fontsize="x-small", framealpha=1.0, bbox_to_anchor=(0.125, 0.02), loc=3, borderaxespad=0,
                  bbox_transform=plt.gcf().transFigure, ncol=int(len(self._states)/2))
        #
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_main_plot)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_main_plot)
        self.toolbar.config(background=self.color_background)
        self.toolbar._message_label.config(background=self.color_background)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_buttons(self, parent):
        btn_select_all = tk.Button(parent, text="Select all", height=1, width=10, padx=2, pady=2,
                                   fg="#22252D", bg="#F1F1EB",
                                   command=lambda: self.cb_select_all(states=self._states))
        btn_select_all.place(relx=0.9, rely=0.0)
        btn_deselect_all = tk.Button(parent, text="Deselect all", height=1, width=10, padx=2, pady=2,
                                     fg="#22252D", bg="#F1F1EB",
                                     command=lambda: self.cb_deselect_all(states=self._states))
        btn_deselect_all.place(relx=0.9, rely=0.04)

    def _value_changed(self, name, _, op):
        if self._states[name].get():
            self.lines[name][0].set_visible(True)
        else:
            self.lines[name][0].set_visible(False)
        self.canvas.draw()

    def cb_select_all(self, states):
        for state in states.values():
            state.set(True)
        state.trace_add("write", self._value_changed)
    #
    def cb_deselect_all(self, states):
        for state in states.values():
            state.set(False)
        state.trace_add("write", self._value_changed)

    def plot_csv(self, parent, listbox, event):
        t = time.process_time()
        id = listbox.curselection()
        dataset = data.Data(filename=list_standards[id[0]])
        df = dataset.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
        Plotting(root=parent, data=df)
        elapsed_time = time.process_time() - t
        print("Execution time:", elapsed_time)

# FUNCTIONS
def main():

    def newFile():
        print("New File!")
    def openFile():
        name = filedialog.askopenfile()
        print(name)

    def open_csv_standard():
        name = fd.askopenfilenames(parent=root, filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        for i in name:
            if i not in list_standards:
                list_standards.append(i)
                file_parts = i.split("/")
                #standard_listbox.insert(tk.END, i)
                standard_listbox.insert(tk.END, file_parts[-1])
        return name

    def open_csv_sample():
        name = fd.askopenfilenames(parent=root, filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        for i in name:
             if i not in list_samples:
                list_samples.append(i)
                file_parts = i.split("/")
                #sample_listbox.insert(tk.END, i)
                sample_listbox.insert(tk.END, file_parts[-1])
        return name

    def delete_csv_standard():
        item = standard_listbox.curselection()
        #list_standards.remove(standard_listbox.get(item))
        list_standards.remove(list_standards[item[0]])
        standard_listbox.delete(tk.ANCHOR)
        return list_standards

    def delete_csv_sample():
        item = sample_listbox.curselection()
        #list_samples.remove(sample_listbox.get(item))
        list_samples.remove(list_samples[item[0]])
        sample_listbox.delete(tk.ANCHOR)
        return list_samples

    def create_list(parent):
        listbox = tk.Listbox(parent, bg="#DFDFDF", width=25, height=17)
        scrollbar_y = tk.Scrollbar(parent, orient="vertical")
        scrollbar_x = tk.Scrollbar(parent, orient="horizontal")
        listbox.config(yscrollcommand = scrollbar_y.set, xscrollcommand = scrollbar_x.set)
        scrollbar_y.config(command = listbox.yview)
        scrollbar_x.config(command = listbox.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        listbox.pack(side="left", fill="both")
        scrollbar_y.pack(side="right", fill="y")
        #scrollbar_x.pack(side="bottom", fill="x")
        return listbox

    def open_csv():
        filename = filedialog.askopenfilename(filetypes=(("csv files", "*.csv"),("all files", "*.*")),
                                              initialdir=os.getcwd())
        return filename

    def saveFile():
        name = filedialog.asksaveasfile()
        #print(name)
    def saveAsFilename():
        name = filedialog.asksaveasfilename()
        #print(name)
    def newWindow():
        toplevel = tk.Toplevel()
        toplevel.title('Another window')
        toplevel.focus_set()

    def add_csv(relx, rely, command):
        btn_add_standard = tk.Button(root, text="Add", height=1, width=6, padx=2, pady=2, fg="#22252D",
                                     bg="#F1F1EB", command=command)
        btn_add_standard.place(relx=relx, rely=rely)
        #btn_add_standard.grid()

    def delete_csv(relx, rely, command):
        btn_delete_standard = tk.Button(root, text="Delete", height=1, width=6, padx=2, pady=2, fg="#22252D",
                                        bg="#F1F1EB", command=command)
        btn_delete_standard.place(relx=relx, rely=rely)

    def analyze_csv(relx, rely, command):
        btn_delete_standard = tk.Button(root, text="Analyze", height=1, width=8, padx=2, pady=2, fg="#22252D",
                                        bg="#F1F1EB", command=command)
        btn_delete_standard.place(relx=relx, rely=rely)

    # def plot_csv_standard(event):
    #     id = standard_listbox.curselection()
    #     dataset = data.Data(filename=list_standards[id[0]])
    #     df = dataset.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
    #     Plotting(root=root, data=df)
    #
    # def plot_csv_sample(event):
    #     id = sample_listbox.curselection()
    #     dataset = data.Data(filename=list_samples[id[0]])
    #     df = dataset.import_data_to_pandas(delimiter=",", skip_header=3, skip_footer=1)
    #     Plotting(root=root, data=df)

    # FRAME
    root = tk.Tk()
    root.title("PySILLS")

    # MENU
    menu = tk.Menu(root)
    root.config(menu=menu)

    filemenu = tk.Menu(menu)
    menu.add_cascade(label="Project", menu=filemenu)
    filemenu.add_command(label="New", command=newFile)
    filemenu.add_command(label="Open", command=openFile)
    filemenu.add_command(label = "Save", command = saveFile)
    filemenu.add_command(label = "Save as", command = saveAsFilename)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)

    standardmenu = tk.Menu(menu)
    menu.add_cascade(label="Standard", menu=standardmenu)
    standardmenu.add_command(label="Load SRM data", command=open_csv)
    standardmenu.add_command(label="Load SRM measurements", command=open_csv_standard)
    standardmenu.add_separator()
    standardmenu.add_command(label="Settings", command=newWindow)

    samplemenu = tk.Menu(menu)
    menu.add_cascade(label="Sample", menu=samplemenu)
    samplemenu.add_command(label="Load sample measurements", command=open_csv_sample)
    samplemenu.add_separator()
    samplemenu.add_command(label="Settings", command=newWindow)

    resultsmenu = tk.Menu(menu)
    menu.add_cascade(label="Results", menu=resultsmenu)
    resultsmenu.add_command(label="Show sensitivities", command=newWindow)
    resultsmenu.add_command(label="Show concentrations", command=newWindow)

    helpmenu = tk.Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="Q&A", command=newWindow)

    aboutmenu = tk.Menu(menu)
    menu.add_cascade(label="About", menu=aboutmenu)
    aboutmenu.add_command(label="About PySILLS", command=newWindow)

    canvas = tk.Canvas(root, height=900, width=1600, bg="#2D4D59")
    canvas.pack()

    frame_main = tk.Frame(root, bg="#2D4D59")
    frame_main.place(relwidth=0.8, relheight=0.8, relx=0.01, rely=0.01)
    pysills_logo = tk.PhotoImage(file = "../documentation/images/PySILLS_Logo.png")
    pysills_logo = pysills_logo.subsample(2, 2)
    tk.Label(frame_main, image=pysills_logo, borderwidth=0, highlightthickness=0, padx=0, pady=0).pack(fill="none",
                                                                                                       expand=True)

    # LISTBOX
    frame_standard = tk.Frame(root, bg="#DFDFDF")
    frame_standard.place(relwidth=0.17, relheight=0.32, relx=0.82, rely=0.08)
    standard_listbox = create_list(parent=frame_standard)
    label_standard = tk.Label(root, text ="Standard files", fg="#F1F1EB", bg="#2D4D59")
    label_standard.place(relx = 0.82, rely = 0.01)
    add_csv(relx=0.82, rely=0.04, command=open_csv_standard)
    delete_csv(relx=0.87, rely=0.04, command=delete_csv_standard)
    analyze_csv(relx=0.92, rely=0.04, command=open_csv_standard)
    standard_listbox.bind("<Double-1>", lambda event, parent=root,
                                               listbox=standard_listbox,
                                               list_data=list_standards: Plotting.plot_csv("", parent, listbox,
                                                                                           list_data, event))

    frame_sample = tk.Frame(root, bg="#DFDFDF")
    frame_sample.place(relwidth=0.17, relheight=0.33, relx=0.82, rely=0.48)
    sample_listbox = create_list(parent=frame_sample)
    label_standard = tk.Label(root, text ="Sample files", fg="#F1F1EB", bg="#2D4D59")
    label_standard.place(relx = 0.82, rely = 0.41)
    add_csv(relx=0.82, rely=0.44, command=open_csv_sample)
    delete_csv(relx=0.87, rely=0.44, command=delete_csv_sample)
    analyze_csv(relx=0.92, rely=0.44, command=open_csv_sample)
    sample_listbox.bind("<Double-1>", lambda event, parent=root,
                                               listbox=sample_listbox,
                                               list_data=list_samples: Plotting.plot_csv("", parent, listbox,
                                                                                         list_data, event))

    frame_results = tk.Frame(root, bg="#DFDFDF")
    frame_results.place(relwidth=0.8, relheight=0.17, relx=0.01, rely=0.82)

    # BUTTONS
    btn_bg_sig = tk.Button(root, text="Set background + signal", height=1, width=24, padx=2, pady=2, fg="#22252D",
                           bg="#F1F1EB", command=newWindow)
    btn_bg_sig.place(relx=0.82, rely=0.82)
    set_inclusion = tk.Button(root, text="Set inclusion", height=1, width=24, padx=2, pady=2, fg="#22252D",
                              bg="#F1F1EB", command=newWindow)
    set_inclusion.place(relx=0.82, rely=0.86)
    btn_driftcorr = tk.Button(root, text="Drift correction", height=1, width=24, padx=2, pady=2, fg="#22252D",
                              bg="#F1F1EB", command=newWindow)
    btn_driftcorr.place(relx=0.82, rely=0.90)
    btn_calculation = tk.Button(root, text="Calculation settings", height=1, width=24, padx=2, pady=2, fg="#22252D",
                                bg="#F1F1EB", command=newWindow)
    btn_calculation.place(relx=0.82, rely=0.94)

    Label_middle = tk.Label(root, text ="PySILLS - Version 1.0 - 2021", fg="#F1F1EB", bg="#2D4D59")
    Label_middle.place(relx = 0.83, rely = 0.975)

    root.mainloop()

# PROGRAM
if __name__ == "__main__":
    main()