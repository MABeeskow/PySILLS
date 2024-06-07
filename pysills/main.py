#!/usr/bin/env python
# -*-coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------

# Name:		main
# Author:	Maximilian A. Beeskow
# Version:	pre-release
# Date:		07.06.2024

# -----------------------------------------------------------------------------------------------------------------------

## MODULES
# external
import os, sys
import tkinter as tk
# internal
from pysills_app import PySILLS

def pysills():
	root = tk.Tk()
	root.title("PySILLS - LA-ICP-MS data reduction")
	path = os.path.dirname(os.path.realpath(sys.argv[0]))
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()

	PySILLS(parent=root, var_screen_width=screen_width, var_screen_height=screen_height, var_path=path)

	root.mainloop()