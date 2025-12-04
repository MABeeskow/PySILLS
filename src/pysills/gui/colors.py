#!/usr/bin/env python
# -*-coding: utf-8 -*-

#-----------------------------------------------

# Name:		colors.py
# Author:	Maximilian A. Beeskow
# Version:	1.0
# Date:		04.12.2025

#-----------------------------------------------

"""
Module: colors.py
This module controls colors that are used for the gui.
"""

# CODE
class Colors:
    def __init__(self):
        pass

    def get_colors(self, name: str):
        self.green_dark = "#282D28"
        self.green_medium = "#616D61"
        self.green_light = "#CFD3CF"
        green_dict = {"Dark": self.green_dark, "Medium": self.green_medium, "Light": self.green_light}
        self.red_dark = "#E76F51"
        self.red_medium = "#F1A896"
        self.red_light = "#FDF0ED"
        red_dict = {"Dark": self.red_dark, "Medium": self.red_medium, "Light": self.red_light}
        self.yellow_dark = "#E9C46A"
        self.yellow_medium = "#F3DFAE"
        self.yellow_light = "#FDFAF2"
        yellow_dict = {"Dark": self.yellow_dark, "Medium": self.yellow_medium, "Light": self.yellow_light}
        self.blue_dark = "#5B828E"
        self.blue_medium = "#8CA7AF"
        self.blue_light = "#CDD9DD"
        blue_dict = {"Dark": self.blue_dark, "Medium": self.blue_medium, "Light": self.blue_light}
        self.brown_dark = "#AC7E62"
        self.brown_medium = "#C4A491"
        self.brown_light = "#EEE5DF"
        brown_dict = {"Dark": self.brown_dark, "Medium": self.brown_medium, "Light": self.brown_light}
        self.slate_grey_dark = "#6E7894"
        self.slate_grey_medium = "#9AA1B4"
        self.slate_grey_light = "#E2E4EA"
        slategrey_dict = {"Dark": self.slate_grey_dark, "Medium": self.slate_grey_medium,
                          "Light": self.slate_grey_light}

        self.bg_colors = {
            "BG Window": "#2C2C2C", "Very Dark": "#3C3C3C", "Dark": "#676767", "Medium": "#909090", "Light": "#BABABA",
            "Very Light": "#E3E3E3", "Dark Font": "#292929", "Light Font": "#F7F7F7", "White": "#FFFFFF",
            "Black": "#000000", "Accent": "#E76F51"}

        self.standard_dark = {
            "BG Window": "#2C2C2C", "Very Dark": "#3C3C3C", "Dark": "#676767", "Medium": "#909090", "Button": "#BABABA",
            "Very Light": "#E3E3E3", "Dark Font": "#2C2C2C", "Light Font": "#E3E3E3", "White": "#FFFFFF",
            "Black": "#000000", "Accent": "#E76F51"}
        self.standard_light = {
            "BG Window": "#E3E3E3", "Very Dark": "#BABABA", "Dark": "#909090", "Medium": "#676767", "Light": "#BABABA",
            "Very Light": "#E3E3E3", "Dark Font": "#E3E3E3", "Light Font": "#E3E3E3", "White": "#FFFFFF",
            "Black": "#000000", "Accent": "#E76F51"}
        self.green_dark = {
            "BG Window": "#323A25", "Very Dark": "#505D3C", "Dark": "#606F49", "Medium": "#676767", "Light": "#CDD5BF",
            "Very Light": "#FAFBF9", "Dark Font": "#323A25", "Light Font": "#FAFBF9", "White": "#FFFFFF",
            "Black": "#000000", "Accent": "#E76F51"}
        self.boho_theme = {
            "BG Window": "#72574f", "Very Dark": "#a3573a", "Dark": "#e5af9e", "Medium": "#e7b7a7", "Light": "#f2d7ce",
            "Very Light": "#f9efeb", "Dark Font": "#2d231f", "Light Font": "#f9efeb", "White": "#FFFFFF",
            "Black": "#000000", "Accent": "#B15C4D"}

        self.accent_color = self.bg_colors["Accent"]
        self.colors_ma = {"Very Dark": "#2F3E46", "Dark": "#354F52", "Medium": "#52796F", "Light": "#84A98C",
                          "Very Light": "#CAD2C5", "Dark Font": "#182320", "Light Font": "#F2F6F5"}
        self.colors_fi = {"Very Dark": "#722F1C", "Dark": "#A04228", "Medium": "#D36A4D", "Light": "#E4A694",
                          "Very Light": "#F6E1DB", "Dark Font": "#411B10", "Light Font": "#FCF4F2"}
        self.colors_mi = {"Very Dark": "#013a63", "Dark": "#014f86", "Medium": "#2c7da0", "Light": "#61a5c2",
                          "Very Light": "#a9d6e5", "Dark Font": "#0D242E", "Light Font": "#EEF7FA"}
        self.colors_intervals = {"BG": "#7F4F24", "SIG": "#414833", "MAT": "#414833", "INCL": "#F4D35E",
                                 "BG LB": "#D8CABD", "SIG LB": "#C6C8C1", "MAT LB": "#C6C8C1", "INCL LB": "#FBF1CE"}

        self.sign_red = "#E84258"
        self.sign_yellow = "#FFDE00"
        self.sign_green = "#B0D8A4"
        sign_dict = {"Green": self.sign_green, "Red": self.sign_red, "Yellow": self.sign_yellow}