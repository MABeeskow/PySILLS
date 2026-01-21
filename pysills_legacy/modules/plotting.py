#!/usr/bin/env python
# -*-coding: utf-8 -*-
# ----------------------
# plotting.py
# Maximilian Beeskow
# 01.06.2021
# ----------------------
#
# MODULES
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

# CLASSES
class Plotting:
    def __init__(self, root, data):
        try:
            self.fig.clf()
            self.ax.cla()
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
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
                self.ax.plot(self.times, self._values[name], label=name, visible=True)
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
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_main_plot)
        self.toolbar.config(background=self.color_background)
        self.toolbar._message_label.config(background=self.color_background)
        #self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def _value_changed(self, name, _, op):
        self.fig.clf()
        self.ax.cla()
        self.frame_main_plot = tk.Frame(self.frame_main, bg=self.color_background)
        self.frame_main_plot.place(relwidth=0.875, relheight=1.0, relx=0.0, rely=0.0)
        self.fig.clear()
        self.fig = Figure(figsize=(1,2), facecolor="#FFFFFF")
        self.ax = self.fig.add_subplot()
        try:
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        if self._states[name].get():
            for name, state in self._states.items():
                if state.get():
                    self.ax.plot(self.times, self._values[name], label=name, visible=True)
        else:
            for name, state in self._states.items():
                if state.get():
                    self.ax.plot(self.times, self._values[name], label=name, visible=True)
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
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_main_plot)
        self.toolbar.config(background=self.color_background)
        self.toolbar._message_label.config(background=self.color_background)
        #self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def cb_select_all(self, states):
        for state in states.values():
            state.set(True)
        state.trace_add("write", self._value_changed)
    #
    def cb_deselect_all(self, states):
        for state in states.values():
            state.set(False)
        state.trace_add("write", self._value_changed)