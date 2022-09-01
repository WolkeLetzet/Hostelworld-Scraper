
from logging import root
from threading import Thread
from time import sleep
import tkinter as tk
from PIL import Image as Img
from PIL import ImageTk as ImgTk
from GifTk import GifTk

ORANGE= '#f25621'

class GUI:
   def __init__(self):
      self.ventana = tk.Tk()
      self.ventana.title("HostelWorldScraper")
      self.ventana.geometry("600x325")
      self.ventana.iconbitmap("icon.ico")
      self.ventana.config(bg=ORANGE)
      self.ventana.resizable(0, 0)
            
      self.options = [tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar()]
      
      self.build_main_frame()
      
   def build_title_frame(self,frame=None):
      if frame is None:
         frame = self.mainFrame
         
      self.title_frame = tk.Frame(frame, bg=ORANGE)
      self.logo=Img.open("logo.png")
      self.logo=ImgTk.PhotoImage(self.logo)
      self.label_logo=tk.Label(self.title_frame, image=self.logo, bg=ORANGE)
      self.label_logo.pack(padx=10, pady=10)
      self.title_frame.pack(side=tk.TOP, fill=tk.X)
      
   def build_entry_frame(self):
         
      self.entry_frame = tk.Frame(self.mainFrame, bg=ORANGE)
      self.scrollbar = tk.Scrollbar(self.entry_frame,orient="horizontal")
      self.entry = tk.Entry(self.entry_frame, font=("Sitka Display", 12), width=50, bg="white", fg="black", xscrollcommand=self.scrollbar.set)
      self.entry.focus()
      self.entry.pack(fill=tk.X, padx=10,ipady=5)
      self.scrollbar.config(command=self.entry.xview)
      self.scrollbar.pack(fill=tk.X, padx=10)
      self.entry_frame.pack( fill=tk.X,ipady=2)
      
   def build_options_frame(self):
      
      self.options[0].set(True)
      self.options[1].set(True)
      self.options[2].set(True)
      self.options[3].set(True)
      
      self.options_frame=tk.Frame(self.mainFrame, bg=ORANGE)
      self.checkbutton1=tk.Checkbutton(self.options_frame, text="Puntaje",
                                       variable=self.options[0], onvalue=True, offvalue=False,
                                       bg=ORANGE, fg="black", font=("Sitka Display", 11), activebackground=ORANGE, activeforeground="white")
      self.checkbutton2=tk.Checkbutton(self.options_frame, text="Todos Los Idiomas",
                                       variable=self.options[1], onvalue=True, offvalue=False,
                                       bg=ORANGE, fg="black", font=("Sitka Display", 11),activebackground=ORANGE, activeforeground="white")
      self.checkbutton3=tk.Checkbutton(self.options_frame, text="Incluir Comnetarios",
                                       variable=self.options[2], onvalue=True, offvalue=False,
                                       bg=ORANGE, fg="black", font=("Sitka Display", 11),activebackground=ORANGE, activeforeground="white")
      self.checkbutton4=tk.Checkbutton(self.options_frame, text="Reseñas sin rate",
                                       variable=self.options[3], onvalue=True, offvalue=False,
                                       bg=ORANGE, fg="black", font=("Sitka Display", 11),activebackground=ORANGE, activeforeground="white")
      
      self.checkbutton1.pack(side=tk.LEFT, padx=10)
      self.checkbutton2.pack(side=tk.LEFT, padx=10)
      self.checkbutton3.pack(side=tk.LEFT, padx=10)
      self.checkbutton4.pack(side=tk.LEFT, padx=10)
      self.options_frame.pack(side=tk.TOP, fill=tk.X)
   
   def build_button_frame(self):
      self.button_frame = tk.Frame(self.mainFrame, bg=ORANGE)
      self.button_scrap = tk.Button(self.button_frame, text="Scrap", font=("Sitka Display", 12), bg='white', fg="black")
      self.button_scrap.pack(padx=10, pady=20,ipady=10, ipadx=20)
      self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
      
   def build_main_frame(self):
      
      self.mainFrame = tk.Frame(self.ventana, bg=ORANGE)
      self.build_title_frame(self.mainFrame)
      self.build_entry_frame()
      self.build_options_frame()
      self.build_button_frame()
      self.mainFrame.pack(fill=tk.BOTH, expand=True)
      self.ventana.update()      
   
   def mainloop(self):
      self.ventana.mainloop()
   
   def set_cursor_busy(self):
      self.ventana.config(cursor="wait")
      self.ventana.update()
   
   def reset_cursor(self):
      self.ventana.config(cursor="")
      self.ventana.update()
       
   def build_loading_frame(self,frame=None):
      
      if frame is None:
         self.loading_frame = tk.Frame(self.ventana, bg=ORANGE)
      else:
         self.loading_frame = tk.Frame(frame, bg=ORANGE)
      
      self.loading_label = tk.Label(self.loading_frame, bg=ORANGE)
      self.loading_label.pack()
      self.loading_frame.pack(fill=tk.BOTH, expand=True)
      
      self.loading_gif = GifTk(self.loading_label, "loading.gif")
      self.loading_gif.start(35)

   def destroy_loading_frame(self):
      self.loading_frame.destroy()
      self.ventana.update()
   
   def destroy_main_frame(self):
      self.mainFrame.destroy()
      self.ventana.update()

   def after(self, ms, func=None, *args):
      self.ventana.after(ms,func,args)



root = GUI()

root.mainloop()