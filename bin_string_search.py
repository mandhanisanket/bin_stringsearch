import tkFileDialog as filedialog
from Tkinter import *
import Tkinter as tk
import os 
import numpy as np
import progressbar
import csv
import string
from mmap import mmap, ACCESS_READ
import re
import subprocess, sys

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


def ssearch(filename, threshold) :
    path = filename
    ##path = path.replace('/','\\')
    path = path + "/"
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
            if(j == 0 or j > no_of_files ):
                continue   
            f.write(line+","+str(j)+"\n")
	final_file=path+"result.csv"  
	opener ="open" if sys.platform == "darwin" else "xdg-open"
	subprocess.call([opener, final_file])

def browse_button(threshold):
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    ssearch(filename, threshold)
    #print(filename)

def show_text():
	label_text.set("You entered : " + entry_text.get())

def open_browse():
	browse_button(entry_text.get())


root = Tk()
root.geometry("320x150") 
folder_path = StringVar()
entry_text = tk.StringVar()
Label(root, text="Enter threshold value  :").pack()

entry = tk.Entry(root, width=10, textvariable=entry_text)
entry.pack()

button = tk.Button(root, text="Enter", command=show_text)
button.pack()

button1 = tk.Button(root, text="Browse", command=open_browse)
button1.pack()

label_text = tk.StringVar()
label = tk.Label(root, textvariable=label_text)
label.pack()

lbl1 = Label(master=root,textvariable=folder_path)

lbl1.pack()


mainloop()
