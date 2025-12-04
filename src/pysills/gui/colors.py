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
        if name == "green":
            green_dark = "#282D28"
            green_medium = "#616D61"
            green_light = "#CFD3CF"
            colors_dict = {"Dark": green_dark, "Medium": green_medium, "Light": green_light}
            return colors_dict
        elif name == "red":
            red_dark = "#E76F51"
            red_medium = "#F1A896"
            red_light = "#FDF0ED"
            colors_dict = {"Dark": red_dark, "Medium": red_medium, "Light": red_light}
            return colors_dict
        elif name == "yellow":
            yellow_dark = "#E9C46A"
            yellow_medium = "#F3DFAE"
            yellow_light = "#FDFAF2"
            colors_dict = {"Dark": yellow_dark, "Medium": yellow_medium, "Light": yellow_light}
            return colors_dict
        elif name == "blue":
            blue_dark = "#5B828E"
            blue_medium = "#8CA7AF"
            blue_light = "#CDD9DD"
            colors_dict = {"Dark": blue_dark, "Medium": blue_medium, "Light": blue_light}
            return colors_dict
        elif name == "brown":
            brown_dark = "#AC7E62"
            brown_medium = "#C4A491"
            brown_light = "#EEE5DF"
            colors_dict = {"Dark": brown_dark, "Medium": brown_medium, "Light": brown_light}
            return colors_dict
        elif name == "slate grey":
            slate_grey_dark = "#6E7894"
            slate_grey_medium = "#9AA1B4"
            slate_grey_light = "#E2E4EA"
            colors_dict = {"Dark": slate_grey_dark, "Medium": slate_grey_medium, "Light": slate_grey_light}
            return colors_dict
        elif name == "background":
            colors_dict = {
                "BG Window": "#2C2C2C", "Very Dark": "#3C3C3C", "Dark": "#676767", "Medium": "#909090",
                "Light": "#BABABA", "Very Light": "#E3E3E3", "Dark Font": "#292929", "Light Font": "#F7F7F7",
                "White": "#FFFFFF", "Black": "#000000", "Accent": "#E76F51"}
            return colors_dict
        elif name == "standard dark":
            colors_dict = {
                "BG Window": "#2C2C2C", "Very Dark": "#3C3C3C", "Dark": "#676767", "Medium": "#909090",
                "Button": "#BABABA", "Very Light": "#E3E3E3", "Dark Font": "#2C2C2C", "Light Font": "#E3E3E3",
                "White": "#FFFFFF", "Black": "#000000", "Accent": "#E76F51"}
            return colors_dict
        elif name == "standard light":
            colors_dict = {
                "BG Window": "#E3E3E3", "Very Dark": "#BABABA", "Dark": "#909090", "Medium": "#676767",
                "Light": "#BABABA", "Very Light": "#E3E3E3", "Dark Font": "#E3E3E3", "Light Font": "#E3E3E3",
                "White": "#FFFFFF", "Black": "#000000", "Accent": "#E76F51"}
            return colors_dict
        elif name == "green dark":
            colors_dict = {
            "BG Window": "#323A25", "Very Dark": "#505D3C", "Dark": "#606F49", "Medium": "#676767", "Light": "#CDD5BF",
            "Very Light": "#FAFBF9", "Dark Font": "#323A25", "Light Font": "#FAFBF9", "White": "#FFFFFF",
            "Black": "#000000", "Accent": "#E76F51"}
            return colors_dict
        elif name == "boho":
            colors_dict = {
                "BG Window": "#72574f", "Very Dark": "#a3573a", "Dark": "#e5af9e", "Medium": "#e7b7a7",
                "Light": "#f2d7ce", "Very Light": "#f9efeb", "Dark Font": "#2d231f", "Light Font": "#f9efeb",
                "White": "#FFFFFF", "Black": "#000000", "Accent": "#B15C4D"}
            return colors_dict
        elif name == "accent colors":    
            sign_red = "#E84258"
            sign_yellow = "#FFDE00"
            sign_green = "#B0D8A4"
            colors_dict = {"Green": sign_green, "Red": sign_red, "Yellow": sign_yellow}
            return colors_dict
        elif name == "interval colors":
            colors_dict = {
                "BG": "#7F4F24", "SIG": "#414833", "MAT": "#414833", "INCL": "#F4D35E", "BG LB": "#D8CABD",
                "SIG LB": "#C6C8C1", "MAT LB": "#C6C8C1", "INCL LB": "#FBF1CE"}
            return colors_dict