import sys
import tkinter
from tkinter import font
sys.path.insert(0, "./")

from tkinter import *
from PIL import Image, ImageTk
import urllib.request
from threading import Thread
import numpy as np
import pickle
import time
import os
import io
from tkinter import messagebox
import requests

# var
path = "saved_model"
curDir = os.path.dirname(os.path.abspath(__file__))
BG_COLOR = "azure"
TEXT_COLOR = "gray"
BUTTON_COLOR = "dodgerblue"

root = Tk()
root.title('Find Stock')
root.geometry('900x360')
root.config(bg=BG_COLOR)

# title
name = Label(root, text='Find Stock', justify=CENTER, fg=TEXT_COLOR, bd=2, bg=BG_COLOR)
name.config(font=("Arial", 24))
name.pack(side=TOP, pady=50)

# link input
link_entry = Entry(root, width=60, justify=CENTER, fg=BUTTON_COLOR)
link_entry.config(font=('Arial', 14))
link_entry.pack(side=TOP, pady=10)

def getStock(code):
    url = "http://vnindex.herokuapp.com/getStockInfo?code=" + code.upper()
    result = requests.get(url)

    return result.json()

# Process info
def processing():
    inp = link_entry.get()
    print(inp)

    # không nhập input
    if inp == "":
        messagebox.showinfo(title='Alert', message="URL is empty!\n")
        return

    # Nhập đúng
    else:

        # mở cửa số thông tin
        newWindow = Toplevel(root)
        newWindow.title("Result")
        newWindow.geometry('600x360')
        newWindow.config(bg=BG_COLOR)
        
        FONT1 = ('Aria', 12)
        FONT2 = ('Aria', 16, 'bold')

        pad_label1 = Label(newWindow, bg=BG_COLOR)
        pad_label1.pack(side=TOP, pady=5)

        res_label = Label(newWindow, text='Information for '+ inp, font=FONT2, bg=BG_COLOR, fg='gray')
        res_label.pack(side=TOP, pady=5)


        info = getStock(inp)
    
        txt = f"Price: {info['price']} \nVolume: {info['volume']} \n"

        msg = Message( newWindow, text = txt, font=FONT1, bg=BG_COLOR, fg='gray')  
        msg.pack(side=TOP)

        

def startThread():
    thread = Thread(target=processing)
    thread.start()
    return thread
    
process_btn = Button(root, text='Process', width=16, height=2, font=('Arial', 12, 'bold'), bd=0, bg=BUTTON_COLOR, fg='white', command=startThread)
process_btn.pack(side=TOP, pady=20, padx=20)

# Main Loop
root.mainloop()