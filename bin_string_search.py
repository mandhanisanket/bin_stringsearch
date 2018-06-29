import tkFileDialog as filedialog
from Tkinter import *
import os 
import numpy as np
import progressbar
import csv
import string
from mmap import mmap, ACCESS_READ
import re
import sys

def strings(fname, n=6):
    f = open(fname, 'rb')
    m = mmap(f.fileno(), 0,access = ACCESS_READ)
    for match in re.finditer(('([\w/]{%s}[\w/]*)' % n).encode(), m):
        yield match.group(0)
       
def call_strings(filename):
    sl = []
    for word in strings(filename):
        sl.append(word)
    return sl


def ssearch(filename) :
    path = filename
    path = path.replace('/','\\')
    path = path + '\\'
    list_of_files = os.listdir(path)
    no_of_files = len(list_of_files)
    bar = progressbar.ProgressBar(maxval=no_of_files,widgets=[progressbar.Bar('*', '[', ']'), ' ', progressbar.Percentage()])
    file1 = list_of_files[1]
    
    FullFilePath = path+file1
    lines1 = call_strings(FullFilePath)
    
    length = len(lines1)
    arr = np.zeros(shape=length)
    counter = 0
    bar.start()
    for fil in list_of_files:
        
        FullFilePath1 = path+fil
        lines2 = call_strings(FullFilePath1)
        i = 0
        try:
            bar.update(counter)
        except:
            pass
        counter = counter +1
        for substring in lines1:
            
            for substring2 in lines2:
                if(substring == substring2):
                    arr[i] = arr[i] + 1
            i = i + 1
    try:
        bar.finish()
    except:
        pass        
    i = 0
    with open(path+'result.csv', 'w') as f:
        for line in lines1 :
            j = arr[i]
            i = i + 1 
            if(j == 0 or j > no_of_files or len(line) < 7 or j < (no_of_files/2)):
                continue   
            f.write(line+","+str(j)+"\n")  

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    ssearch(filename)
    print(filename)


root = Tk()
root.geometry("200x100") 
folder_path = StringVar()
lbl1 = Label(master=root,textvariable=folder_path)
lbl1.grid(row=10, column=10)
button2 = Button(text="Browse", command=browse_button)
button2.place(relx=0.5, rely=0.5, anchor=CENTER)
##button2.grid(row=5, column=5)

mainloop()