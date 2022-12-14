#!/usr/bin/env python
import io
import os
import sys

import numpy as np
import PySimpleGUI as sg
from PIL import Image, ImageOps

import CannyEdgeDetector as ced

np.set_printoptions(threshold=sys.maxsize)

NewImage = 0

Edges = ced.cannyEdgeDetector(NewImage)

filetypes = [
  
    ("ALL FILES", "*.*")
]

Filebrowser = [
    
        [
            sg.Text("Choose Image"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=filetypes),
            sg.Button("Load Image")
        ],

        [sg.Text("Kernel Size")],
        [sg.Slider(orientation='h', range=(3, 25), resolution=2, size = (30, 5), key="-KERNEL-")],
        [sg.Text("Blur Variance")],
        [sg.Slider(orientation='h', range=(1, 50), resolution=2, size = (30, 5), key="-VAR-")],
        [sg.Text("High Threshold")],
        [sg.Input(key="-HT-", default_text=30)],
        [sg.Text("Low Threshold")],
        [sg.Input(key="-LT-", default_text=20)]
    
]


ImageViewer = [
    
        [sg.Image(key="-IMAGE-")]
    
]



layout = [
    [sg.Col(Filebrowser, vertical_alignment="top"),
    sg.VSeperator(),
    sg.Column(ImageViewer)]
]
window = sg.Window('Image Browser', layout)

while True:
    

    event, values = window.read()
    
    # perform button and keyboard operations
    if event == sg.WIN_CLOSED:
        break
    if event == "Load Image":
        filename = values["-FILE-"]
        if os.path.exists(filename):
            Edges.kernel_size = int(values["-KERNEL-"])
            Edges.sigma = int(values["-VAR-"])
            Edges.highThreshold = int(values["-HT-"])
            Edges.lowThreshold = int(values["-LT-"])
            image = Image.open(values["-FILE-"])
            #image.thumbnail((500,500))
            image = ImageOps.grayscale(image)
            NewImage = np.asarray(image)
            Edges.imgs = NewImage
            image = Image.fromarray(Edges.detect())
            bio = io.BytesIO()
            # Actually store the image in memory in binary 
            image.save(bio, format="PNG")
            # Use that image data in order to 
            window["-IMAGE-"].update(data=bio.getvalue())
    

window.close()