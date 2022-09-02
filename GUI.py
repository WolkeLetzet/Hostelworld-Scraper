import tkinter as tk
from tkinter import Menu, filedialog
from tkinter.filedialog import asksaveasfile
from PIL import Image as Img
from PIL import ImageTk as ImgTk
from GifTk import GifTk

ORANGE= '#f25621'

class GUI:
   def __init__(self):
      self.ventana = tk.Tk()
      self.ventana.title("HostelWorldScraper")
      self.ventana.geometry("600x400")
      self.ventana.iconbitmap("icon.ico")
      self.ventana.config(bg=ORANGE)
      self.ventana.resizable(0, 0)
      self.url= tk.StringVar()
      self.path= tk.StringVar()
      
      self.options = [tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar()] #variables de opciones
      
      self.options[0].set(True)
      self.options[1].set(True)
      self.options[2].set(True)
      self.options[3].set(True)
      
      
      
      
      self.build_main_frame()  
      
   def build_title_frame(self,frame=None):
      if frame is None:
         frame = self.mainFrame
         
      self.title_frame = tk.Frame(frame, bg=ORANGE)
      self.logo=Img.open("logo.png")
      self.logo=ImgTk.PhotoImage(self.logo)
      self.label_logo=tk.Label(self.title_frame, image=self.logo, bg=ORANGE)
      self.label_logo.pack(padx=10, pady=10)
      self.title_frame.pack(side=tk.TOP, fill=tk.X,pady=10)
      
   def build_entry_frame(self):
         
      self.entry_frame = tk.Frame(self.mainFrame, bg=ORANGE)
      
      
      self.scrollbar = tk.Scrollbar(self.entry_frame,orient="horizontal")
      self.url_entry = tk.Entry(self.entry_frame,textvariable=self.url, font=("Sitka Display", 12), width=50, bg="white", fg="black", xscrollcommand=self.scrollbar.set)
      self.url_entry.focus()
      
      self.rcm = Menu(self.entry_frame,tearoff= 0)
      self.rcm.add_command(label ="Copy",command=self.__copy)
      self.rcm.add_command(label ="Paste",command=self.__paste)
      self.url_entry.bind("<Button-3>", self.do_popup)
      self.url_entry.pack(fill=tk.X, padx=10,ipady=5)
      self.scrollbar.config(command=self.url_entry.xview)
      self.scrollbar.pack(fill=tk.X, padx=10)
      
      
      self.entry_frame.pack( fill=tk.X,ipady=2)
    
   def do_popup(self,event):
      try:
         self.rcm.tk_popup(event.x_root,event.y_root)
      finally:
         self.rcm.grab_release()
  
   def build_path_frame(self):
      
      self.path_frame = tk.Frame(self.mainFrame,bg= ORANGE)
      
      self.path_entry= tk.Entry(self.path_frame,textvariable=self.path, font=("Sitka Display", 10), width=40, bg="white", fg="black")
      self.path_button = tk.Button(self.path_frame, text="Save As", font=("Sitka Display", 10), bg='white', fg="black",command=self.saveAsDialogue)
      self.path_label = tk.Label(self.path_frame,text="Ubicacion:", font=("Sitka Display", 12), bg=ORANGE, fg="white")
      
      self.path_label.pack(side=tk.LEFT,padx=10)
      self.path_entry.pack(side=tk.LEFT, padx=10)
      self.path_button.pack(side=tk.LEFT, padx=10)
      self.path_frame.pack(side=tk.TOP, fill=tk.X,pady=20,padx=30)
      
   def saveAsDialogue(self):
      
      path= filedialog.asksaveasfilename(defaultextension=".xlsx",initialdir = "/",title = "Select file",filetypes = (("Libro Excel","*.xlsx"),("all files","*.*")))
      if ".xlsx" not in path and path.__len__()>0 :
         path+= ".xlsx"
         
      self.path.set(path)
         
   def build_options_frame(self):
            

      self.options_frame=tk.Frame(self.mainFrame, bg=ORANGE)
      
      self.checkbutton1=tk.Checkbutton(self.options_frame, text="Valores",
                                       variable=self.options[0], onvalue=True, offvalue=False,
                                       bg=ORANGE, fg="black", font=("Sitka Display", 11), activebackground=ORANGE, activeforeground="white")
      self.checkbutton2=tk.Checkbutton(self.options_frame, text="Todos Los Idiomas",
                                       variable=self.options[1], onvalue=True, offvalue=False,
                                       bg=ORANGE, fg="black", font=("Sitka Display", 11),activebackground=ORANGE, activeforeground="white")
      self.checkbutton3=tk.Checkbutton(self.options_frame, text="Comnetarios",
                                       variable=self.options[2], onvalue=True, offvalue=False,
                                       bg=ORANGE, fg="black", font=("Sitka Display", 11),activebackground=ORANGE, activeforeground="white")
      self.checkbutton4=tk.Checkbutton(self.options_frame, text="Reseñas sin valores",
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
      
      """Contstruir main frame en la ventana"""
      
      self.mainFrame = tk.Frame(self.ventana, bg=ORANGE)
      self.build_title_frame(self.mainFrame)
      self.build_entry_frame()
      
      self.build_options_frame()
      self.build_path_frame()
      self.build_button_frame()
      self.mainFrame.pack(fill=tk.BOTH, expand=True)
      
   def mainloop(self):
      """iniciar mainloop"""
      self.ventana.mainloop()
      
   def build_loading_frame(self):
      """Construir pantalla de carga"""
      
      self.loading_frame = tk.Frame(self.ventana, bg=ORANGE)
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
   
   def __copy(self):
      self.url_entry.event_generate("<<Copy>>")
      
   def __paste(self):
      self.url_entry.event_generate("<<Paste>>")
   
   def get_url(self):
      return self.url.get()
   
   def get_path(self):
      return self.path.get()
   
   def get_options(self):
      return [self.options[0].get(),self.options[1].get(),self.options[2].get(),self.options[3].get()]
   
gui = GUI()



gui.mainloop()