
# coding: utf-8

# In[ ]:


import os
import pandas as pd
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt

def open_file():
  
    try:
        Tk().withdraw()
        local_file = askopenfilename()
        print("Current file: " + local_file)
    except FileNotFoundError:
        print("No file selected.")
        sys.exit(1)
    except:
        local_file = ""
    local = pd.read_csv(local_file, delimiter=",",decimal = b".", usecols=[0,1,2,3,4,5])
    local = local[['x [nm]', 'y [nm]', 'frame', 'intensity [photon]']]
    local = local.rename(columns={'frame':'t [frame]', 'intensity [photon]':'I [A.D. counts]'})
    convf = float(txt.get()) 
    local['I [A.D. counts]'] = local['I [A.D. counts]'].astype(float)
    local['I [A.D. counts]'] = local['I [A.D. counts]'] * convf
    #local = local.round(decimals=2)
    #print(local)
    #export_file_path = filedialog.asksaveasfilename(defaultextension='.txt')
    local_file = os.path.splitext(local_file)[0]
    export_file_path = local_file + ".txt"
    local.to_csv(export_file_path, header=None, index=None, sep='\t', mode='a')
    with open(export_file_path, 'r') as original: data = original.read()
    with open(export_file_path, 'w') as modified: modified.write(
        '# localization roi file (Malk format)\n# x[nm]\ty[nm]\tt[frame]\tI[A.D. counts]\n'+ data)
    print("Saved as ", export_file_path)

def gui_run():
    run_main()
    done_box()

def done_box():
    messagebox.showinfo('TStoMALK', 'Done!')

def show_hist():
    try:
        Tk().withdraw()
        local_file = askopenfilename()
        print("Current file: " + local_file)
    except FileNotFoundError:
        print("No file selected.")
        sys.exit(1)
    except:
        local_file = ""
    df = pd.read_csv(local_file, skiprows = 2, sep = "   ", names=["x", "y", "frame", "intensity"], engine = "python")
    fig, ax = plt.subplots()
    range1 = float(txt2.get())
    range2 = float(txt3.get())
    df['intensity'].hist(bins=20, weights=np.ones_like(df[df.columns[0]]) / len(df), range = [range1, range2])
    local_file = os.path.splitext(local_file)[0]
    export_file_path = local_file + ".png"
    fig.suptitle('CBC Analysis')
    plt.xlabel('CBC value')
    plt.ylabel('Frequency')
    fig.savefig(export_file_path)

    
window = Tk()
window.title("CKS")
window.geometry('275x140')

lbl = Label(window, text="Thunderstorm .csv file")
lbl.grid(column=0, row=0)

lbl1 = Label(window, text="Conversion Factor")
lbl1.grid(column=0, row=1)

lbl2 = Label(window, text="(Gain: 200, red = 13.00, green = 12.95)")
lbl2.grid(column=0, row=2)

lbl3 = Label(window, text="(Create Histogram from cbc.txt file)")
lbl3.grid(column=0, row=3)

lbl4 = Label(window, text="lower range")
lbl4.grid(column=0, row=4)

lbl5 = Label(window, text="upper range")
lbl5.grid(column=1, row=4)

var = IntVar()
var.set(13.00)
txt = Entry(window, width=8, textvariable=var)
txt.grid(column=1, row=1)

var2 = IntVar()
var2.set(-1)
txt2 = Entry(window, width=8, textvariable=var2)
txt2.grid(column=0, row=5)

var3 = IntVar()
var3.set(1)
txt3 = Entry(window, width=8, textvariable=var3)
txt3.grid(column=1, row=5)

btn = Button(window, text="Load file", command = open_file)
btn.grid(column=1, row=0)

btn2 = Button(window, text="Histogram", command = show_hist)
btn2.grid(column=1, row=3)

window.mainloop()


