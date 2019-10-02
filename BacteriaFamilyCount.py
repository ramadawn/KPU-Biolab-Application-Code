import tkinter as tk

from tkinter import *
from tkinter.filedialog import askopenfilename

import pandas as pd

from csv import reader

#initialize application window

window = tk.Tk()

#Window name
window.title("Bacteria Family Counting Application")


"""logo"""
logo = PhotoImage(file="logo.gif")
Label (window, image=logo, bg="black") .grid(row=0, column=0, sticky=W)

"""Header"""
Label (window, text="KPU Lab Bacteria Family Counting Application", font="none 16 bold") .grid(row=0, column=1, sticky=E)
"""empty row"""
Label (window, text="", font="none 16 bold") .grid(row=1, column=0, sticky=W)

"""initialize data storage class"""
class FileData:
    def __init__(self):
        self.data = 0
        self.dictionary = 0
        self.fileName = 0

"""Initialize a data storage object"""
LoadData = FileData()

"""load file callback function"""
def loadFileCallback():
    name = askopenfilename(
                           filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    
    """Using try in case user types in unknown file or closes without choosing a file."""
    try:
        df = pd.read_csv(name, delimiter=r"\s+")
        LoadData.data = df
        LoadData.fileName = name.split("/")[-1]
        print("File Data Loaded ",name)

   
    except:
        print("No file exists")

"""Print out object"""
def printDataCallback():
    """dump dataframe family column into a list"""
    familyList = LoadData.data['Family'].tolist()

    """create an instance counter dictionary"""
    familyNameDictionary = {}

    
    """iterate through family name list and pick out unique instances load
        them into the dictionary"""
    for familyName in familyList:
        if familyName in familyNameDictionary:
            familyNameDictionary[familyName] = familyNameDictionary[familyName] + 1
            

        else:
            familyNameDictionary[familyName] = 1  
            
    familyNameDictionary["Single Instance Families"] = 0

    LoadData.dictionary = familyNameDictionary

    

    root = tk.Tk()
    root.title(LoadData.fileName)

    c_width = 800  # Define it's width
    c_height = 700  # Define it's height
    c = tk.Canvas(root, width=c_width, height=c_height, bg='white')
    c.pack()

    # The variables below size the bar graph
    LeftCanvasGap = 10
    barWidth = 20
    barGap = 20
    barLengthPerUnit = 40
    counter = 0

    

    # A quick for loop to calculate the rectangle
    for key in LoadData.dictionary:

        DataValue = LoadData.dictionary[key]

        if DataValue == 1:
            familyNameDictionary["Single Instance Families"] = familyNameDictionary["Single Instance Families"] + 1
            continue

        entry = counter
        # coordinates of each bar

        # Top left coordinate
        x0 = LeftCanvasGap

        y0 = entry * (barWidth + barGap) + 10

        # Bottom right coordinates
        x1 = LeftCanvasGap + DataValue * barLengthPerUnit

        y1 = entry * (barWidth + barGap) + barWidth + 10

        # Draw the bar
        c.create_rectangle(x0, y0, x1, y1, fill="red")
        print(x0,y0,x1,x0)
        print(entry,DataValue)

        # Put the y value above the bar
        c.create_text(x0 + 2, y0 + 35, anchor=tk.SW, text=key+" "+str(DataValue))

        counter = counter + 1


"""load File button"""
loadFileButton = tk.Button(text="Load File", command = loadFileCallback) .grid(row=3, column=1, sticky=W)

"""diaplay Data""" 
displayButton = tk.Button(text="Process And Display Family Data", command = printDataCallback) .grid(row=5, column=1, sticky=W)

"""bar graphg info"""


"""appliction main loop"""
window.mainloop()
