#!/usr/bin/env python
import PySimpleGUI as sg
import os
import sys
import numpy as np
import CannyEdgeDetector as ced
from PIL import Image, ImageOps
import io
np.set_printoptions(threshold=sys.maxsize)

NewImage = 0

Edges = ced.cannyEdgeDetector(NewImage)

filetypes = [
    ("PNG", "*.png"),
    ("All Files", "*.*")
]

Filebrowser = [
    [
        sg.Text("Choose Image"),
        sg.Input(size=(25, 1), key="-FILE-"),
        sg.FileBrowse(file_types=filetypes),
        sg.Button("Load Image")
    ]
]
ImageViewer = [
    [
        sg.Image(key="-IMAGE-")
    ]
]

layout = [
    [Filebrowser,
    sg.VerticalSeparator(),
    ImageViewer]
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
            image = Image.open(values["-FILE-"])
            image.thumbnail((1000,1000))
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