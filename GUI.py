import tkinter as tk
from PIL import Image, ImageTk
import scrap as scrap
from threading import *
ORANGE= '#f25621'

class GUI:
   def __init__(self):
      self.ventana = tk.Tk()
      self.ventana.title("HostelWorldScraper")
      self.ventana.geometry("600x325")
      self.ventana.iconbitmap("icon.ico")
      self.ventana.config(bg=ORANGE)
      self.ventana.resizable(0, 0)
      
      self.title_frame = tk.Frame(self.ventana, bg=ORANGE)
      self.logo=Image.open("scraper logo.png")
      self.logo=ImageTk.PhotoImage(self.logo)
      self.label_logo=tk.Label(self.title_frame, image=self.logo, bg=ORANGE)
      self.label_logo.pack(padx=10, pady=10)
      self.title_frame.pack(side=tk.TOP, fill=tk.X)
      
      self.entry_frame = tk.Frame(self.ventana, bg=ORANGE)
      self.scrollbar = tk.Scrollbar(self.entry_frame,orient="horizontal")
      self.entry = tk.Entry(self.entry_frame, font=("Sitka Display", 12), width=50, bg="white", fg="black", xscrollcommand=self.scrollbar.set)
      self.entry.focus()
      self.entry.pack(fill=tk.X, padx=10,ipady=5)
      self.scrollbar.config(command=self.entry.xview)
      self.scrollbar.pack(fill=tk.X, padx=10)
      self.entry_frame.pack( fill=tk.X,ipady=2)
      
      self.options = [tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar()]
      self.options[0].set(True)
      self.options[1].set(True)
      self.options[2].set(True)
      
      self.options_frame=tk.Frame(self.ventana, bg=ORANGE)
      self.checkbutton1=tk.Checkbutton(self.options_frame, text="Puntaje",
                                       variable=self.options[0], onvalue=True, offvalue=False,
                                       bg=ORANGE, fg="black", font=("Sitka Display", 11), activebackground=ORANGE, activeforeground="white")
      self.checkbutton2=tk.Checkbutton(self.options_frame, text="Todos Los Idiomas",
                                       variable=self.options[1], onvalue=True, offvalue=False,
                                       bg=ORANGE, fg="black", font=("Sitka Display", 11),activebackground=ORANGE, activeforeground="white")
      self.checkbutton3=tk.Checkbutton(self.options_frame, text="Incluir Comnetarios",
                                       variable=self.options[2], onvalue=True, offvalue=False,
                                       bg=ORANGE, fg="black", font=("Sitka Display", 11),activebackground=ORANGE, activeforeground="white")
      
      self.checkbutton1.pack(side=tk.LEFT, padx=10)
      self.checkbutton2.pack(side=tk.LEFT, padx=10)
      self.checkbutton3.pack(side=tk.LEFT, padx=10)
      self.options_frame.pack(side=tk.TOP, fill=tk.X)
      
      self.button_frame = tk.Frame(self.ventana, bg=ORANGE)
      self.button_scrap = tk.Button(self.button_frame, text="Scrap", font=("Sitka Display", 12), bg='white', fg="black")
      self.button_scrap.pack(padx=10, pady=20,ipady=10, ipadx=20)
      self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
      
            
   
gui=GUI()

gui.ventana.mainloop()