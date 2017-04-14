#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on the 23 March 2017
author : olivier regniers (i-sea)
Application : reads metadata, applies coastline mask, performs atmospheric correction using DOS1 approach and export result in outFolder, estimates Turbidity with method from Dogliotti 2015 based on Red and NIR reflectance and exports result as an image, writes an xml file containing metadata about the image and statistics on estimated turbidity 
example : python C:\Users\ucfadko\Desktop\SEODWARF_S2_TURB_fMask.py -inFolder C:\Users\ucfadko\Desktop\S2A_MSIL1C_20170203T083141_N0204_R021_T36SWD_20170203T083527 -outFolder C:\Users\ucfadko\Desktop\S2_Results
Milto's example: python C:\Users\Milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\Code\SEODWARF_S2_TURB_fMask.py -inFolder C:\Users\Milto\Documents\TEPAK\RISE\TestData\S2A_MSIL1C_20170225T091021_N0204_R050_T35SLA_20170225T091220 -outFolder C:\Users\Milto\Documents\TEPAK\RISE\TestResults

note1 : classical folder and files structure for raw L1C S2 data has to be conserved for the code to run properly
note2 : code needs a coastline shapefile to apply land/water mask, check within the code if path to shapefile is correct (around line 170)
note 3 : code needs fmask to perform cloud masking, check within the code if path to fmask python functions is correct (around line 126) or add directory to working path
"""


import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-inFolder",
     required=True,
     help="path to folder containing S2 data (first folder, not IMG_DATA)",
     metavar='<string>')
parser.add_argument("-outFolder",
     required=True,
     help="path to folder where results are stored",
     metavar='<string>')
params = vars(parser.parse_args())
inFolder = params['inFolder']
outFolder = params['outFolder']
