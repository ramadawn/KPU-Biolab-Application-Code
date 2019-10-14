import tkinter as tk

from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.filedialog

import pandas as pd

from csv import reader
import csv
import re

import matplotlib.pyplot as plt

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
        self.extractData = 0 #sorted list of tuples

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
        df = pd.read_csv(name, sep=r'[ \t]{2,}', engine='python')
        """load File name into object"""
        splitName = name.split("/")[-1]
        LoadData.fileName = splitName
        """list for holding family name and %total reads"""
        readDataList = []
        """interate through dataframe and pick out "Family" and "% of total reads" """
        """parse % of total reads' pick out first sets of digits then decimal then digists turn into float"""
        for index, row in df.iterrows():
            value = float(re.findall("\d+\.\d+",row['% of total reads'])[0])
            dataTuple = [row['Family'],value]
            """load tuple into readDataList"""
            readDataList.append(dataTuple)

    except:
        print("Error No data loaded")
   
    DataColationDict = {}

    """iterate through readDataList and group data inside dictionary"""

    for dataTuple in readDataList:
        
        
        if dataTuple[0] in DataColationDict:
            """add value to total and round to two digits"""
            DataColationDict[dataTuple[0]] = round((DataColationDict[dataTuple[0]] + dataTuple[1]), 2)
            
        else:
            
            DataColationDict[dataTuple[0]] = dataTuple[1]
            
    
    """turn dictionary into list"""
    colateList = []

    for key in DataColationDict:
        temp = [key,DataColationDict[key]]
        colateList.append(temp)

    """sort list by tuple[1] value"""
    tempList = sorted(colateList, key=lambda x: x[1])

    sortedColateList = []
    """reverse sorted list"""
    for item in reversed(tempList):
        sortedColateList.append(item)

    LoadData.extractData = sortedColateList

    print("File Data Loaded ",name)

"""Print out object"""
def printDataCallback():
    data = LoadData.extractData

    
    """draw bar graph windows"""
    root = tk.Tk()
    root.title(LoadData.fileName)

    """draw canvas dimetions"""
    c_width = 800  # Define it's width
    c_height = 1000  # Define it's height
    c = tk.Canvas(root, width=c_width, height=c_height, bg='white')
    c.pack()

    """ The variables below size the bar graph"""
    LeftCanvasGap = 10 #left margin
    barWidth = 10 #Height of each bar
    barGap = 15 #distance between each bar
    barLengthPerUnit = 20 #Width of each bar per value
    counter = 0

    """List containing keys to remove"""
    singleKeyList = []

    # A quick for loop to calculate the rectangle
    """filter out single instance data"""
    for value in data:

        DataValue = value[1]
        key = value[0]

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
       

        # Put the y value above the bar
        c.create_text(x0 + 2, y0 + 25, anchor=tk.SW, text=key+" "+str(DataValue))

        counter = counter + 1

    """draw pie chart"""

    """create label list"""
    labels = []
    """create datapiont list"""
    dataPoints = []

    i = 0 #iterator
    maxdisplayNum = 10
    for entry in data:
        if i < maxdisplayNum:
            labels.append(entry[0])
            dataPoints.append(entry[1])

        elif i == maxdisplayNum:
            
            labels.append("Other")
            dataPoints.append(entry[1])

        else:

            lastItemSum = dataPoints[-1]
            dataPoints.pop()
            value = lastItemSum + entry[1]
            dataPoints.append(value)

        i = i + 1

       

    """create explode"""
    explode = [0.1]
    for number in range(maxdisplayNum):
        explode.append(0)

    fig1, ax1 = plt.subplots()
    ax1.pie(dataPoints, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)

    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax1.set_title(LoadData.fileName)

    plt.show()

    
    
    

"""Funtion for sile save dialogue"""
def saveFileCallback():
    f = tkinter.filedialog.asksaveasfile(mode='a', filetypes = (("csv files","*.csv"),("all files","*.*")))
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return

    fileName = f.name
    print("File Name = ",fileName[-4:])
    
    if fileName[-4:] != ".csv":
        print("True")
        fileName = fileName + ".csv"
    else:
        print("False")

    data = LoadData.extractData
    name = LoadData.fileName

    
    with open(fileName, 'a') as file:
        file.write(name+",\n")
        for Datatuple in data:
            writeString = Datatuple[0] + " , " + str(Datatuple[1]) + ",\n"
            file.write(writeString)
        
   
  

    

"""load File button"""
loadFileButton = tk.Button(text="Load File", command = loadFileCallback) .grid(row=3, column=1, sticky=W)

"""diaplay Data""" 
displayButton = tk.Button(text="Process And Display Family Data", command = printDataCallback) .grid(row=5, column=1, sticky=W)

"""append file Button"""
saveButton = tk.Button(text="Append to Data File", command = saveFileCallback) .grid(row=7, column=1, sticky=W)








"""appliction main loop"""
window.mainloop()
