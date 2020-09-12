import tkinter as tk  
import os 
import time
  
top = tk.Tk()
  
  
top.geometry("200x50") 


 
def opening():
    os.system("pytesseract_capturer.py")
b = tk.Button(top,text = "quit",width=10, fg="red", command=quit)  
b.pack(side=tk.RIGHT)
a = tk.Button(top,text = "capture",width=10, fg="blue", command=opening)   

a.pack(side=tk.LEFT)


top.mainloop() 