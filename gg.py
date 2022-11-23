import json
import os
import tkinter as tk
from tkinter import Tk, Toplevel, ttk
from tkinter import filedialog
from PIL import Image as Img
from PIL import ImageTk as ImgTk

ORANGE = '#f25621'
# BLUE = '#101DF0'
# RED = '#F01A10'
# GREEN= '#10F01A'
# VIOLET = '#DF10F0'
# YELLOW= '#E2F010'
# PURPLE= "#7D3C98"


BLUE = ORANGE
RED = ORANGE
GREEN = ORANGE
VIOLET = ORANGE
YELLOW = ORANGE
PURPLE = ORANGE

FONT = 'Microsoft JhengHei UI'
FSIZE1 = 18
FSIZE2 = 16
FSIZE3 = 15
FSIZE4 = 12
FSIZE5 = 12


class GUI:

    def __init__(self, path=os.path.dirname(os.path.realpath(__file__)), *parent: Tk) -> None:
        if parent:
            self.parent = parent[0]
        else:
            self.parent = Tk()
        self.path = path
        self.parent.title("HostelWorldScraper")
        self.parent.geometry("1000x500")
        self.parent.iconbitmap(self.path+"/icon.ico")
        self.parent.config(bg=ORANGE)
        self.parent.resizable(0, 0)

        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)

        self.mainframe = tk.Frame(self.parent, background=ORANGE)

        # Titulo
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        # comboboxes
        self.mainframe.grid_rowconfigure(1, weight=1)
        # opciones
        self.mainframe.grid_rowconfigure(2, weight=1)
        # guardado
        self.mainframe.grid_rowconfigure(3, weight=1)
        # boton
        self.mainframe.grid_rowconfigure(4, weight=1)
        self.mainframe.grid_rowconfigure(5, weight=1)
        self.mainframe.grid_rowconfigure(6, weight=1)
        self.mainframe.grid_rowconfigure(7, weight=1)
        
        tk.Label(self.mainframe, text="Seleccione el lugar de donde dese recolectar Datos", font=(
            FONT, FSIZE2), fg="white", background=ORANGE).grid(row=1,column=0,sticky="nsew")
        tk.Label(self.mainframe, text="En caso de que el metodo anterior no funcione, intente ingresando el url de su busqueda en HostelWord en el campo de abajo \n *(Advertencia): Este metodo tarda mas tiempo y no se obtiene la misma cantidad de datos", font=(
            FONT, FSIZE4), fg="white", background=ORANGE).grid(row=4,column=0,sticky="sew")
        
        tk.Label(self.mainframe, text="created by C.Pastenes y C. Cerda", font=(
            FONT, 9), fg="white", background=ORANGE).grid(row=7,column=0,sticky="se")

        self.mainframe.grid(row=0, column=0, sticky="nsew")

        #### VARIABLES ####
        self.options = [tk.BooleanVar(), tk.BooleanVar(),
                        tk.BooleanVar()]  # variables de opciones
        for op in self.options:
            op.set(True)

        self.savePath = tk.StringVar()
        self.progVar = tk.IntVar()
        self.urlVar = tk.StringVar()
        

        self.continentes = {'Europa': 'europe',
                            'Norteamerica': 'north',
                            'Sudamerica': 'south',
                            'Asia': 'asia',
                            'Oceania': 'oceania'
                            }

    def build_title(self):
        self.title_frame = tk.Frame(self.mainframe, background=BLUE)

        self.title_frame.grid_rowconfigure(0, weight=1)
        self.title_frame.grid_columnconfigure(0, weight=1)

        logo = Img.open(self.path+"/logo.png")
        self.logo = ImgTk.PhotoImage(logo)
        self.label_logo = tk.Label(self.title_frame, image=self.logo, bg=RED)
        self.label_logo.grid(row=0, column=0, sticky="ns")
        self.title_frame.grid(row=0, column=0, sticky="ew")

    def build_cBoxes(self):
        self.cBoxes_frame = tk.Frame(self.mainframe, background=GREEN)
        self.cBoxes_frame.grid_rowconfigure(0, weight=1)
        self.cBoxes_frame.grid_columnconfigure(0, weight=1)
        self.cBoxes_frame.grid_columnconfigure(1, weight=1)
        self.cBoxes_frame.grid_columnconfigure(2, weight=1)

        self.cBoxes_frame.grid_rowconfigure(1, weight=1)

        self.continentsLabel = tk.Label(self.cBoxes_frame, text="Continente:", font=(
            FONT, FSIZE2), fg="white", background=ORANGE)
        self.countriesLabel = tk.Label(self.cBoxes_frame, text="Pais:", font=(
            FONT, FSIZE2), fg="white", background=ORANGE)
        self.citiesLabel = tk.Label(self.cBoxes_frame, text="Ciudad:", font=(
            FONT, FSIZE2), fg="white", background=ORANGE)

        self.continentsBox = ttk.Combobox(self.cBoxes_frame, state='readonly', font=(
            FONT, FSIZE3), values=tuple(self.continentes.keys()))
        self.countriesBox = ttk.Combobox(
            self.cBoxes_frame, state='readonly', font=(FONT, FSIZE3))
        self.citiesBox = ttk.Combobox(
            self.cBoxes_frame, state='readonly', font=(FONT, FSIZE3))

        self.continentsBox.bind("<<ComboboxSelected>>", self.on_countriesBox)
        self.countriesBox.bind("<<ComboboxSelected>>", self.on_citiesBox)
        self.citiesBox.bind("<<ComboboxSelected>>", self.unlock_button)

        self.continentsLabel.grid(row=0, column=0, sticky="sew")
        self.countriesLabel.grid(row=0, column=1, sticky="sew")
        self.citiesLabel.grid(row=0, column=2, sticky="sew")

        self.continentsBox.grid(row=1, column=0, sticky="ew", padx=15)
        self.countriesBox.grid(row=1, column=1, sticky="ew", padx=15)
        self.citiesBox.grid(row=1, column=2, sticky="ew", padx=20)

        self.cBoxes_frame.grid(row=2, column=0, sticky="new")

    def build_executeButton(self):
        self.executeButton_frame = tk.Frame(self.mainframe, background=YELLOW)
        self.executeButton_frame.rowconfigure(0, weight=1)
        self.executeButton_frame.columnconfigure(0, weight=4)

        self.executeButton = tk.Button(self.executeButton_frame, text='Iniciar',
                                       width=15, height=2,
                                       font=(FONT+'bold', FSIZE4),
                                       state="disabled",
                                       
                                       
                                       disabledforeground="#dcdcdc"
                                       )

        self.executeButton.grid(row=0, column=0)
        self.executeButton_frame.grid(row=3, column=0, sticky='nsew')

    def build_URLEntry(self):
        self.url_frame = tk.Frame(self.mainframe, background=PURPLE)

        self.url_frame.grid_rowconfigure(0, weight=1)
        self.url_frame.grid_columnconfigure(0, weight=1)
        self.url_frame.grid_columnconfigure(1, weight=1)
        self.url_frame.grid_columnconfigure(2, weight=1)

        frame0 = tk.Frame(self.url_frame, background=GREEN)
        frame0.rowconfigure(0, weight=1)
        frame1 = tk.Frame(self.url_frame, background=GREEN)
        frame1.rowconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame2 = tk.Frame(self.url_frame, background=BLUE)
        frame2.rowconfigure(0, weight=1)

        self.entry = tk.Entry(frame1, textvariable=self.urlVar,
                              font=(FONT, FSIZE4),
                              bg="white", fg="black",
                              
                              )

        self.urlButton = tk.Button(frame2, text="Ejecutar con Url",
                                       height=2, width=15, font=(FONT, FSIZE5),
                                       state="disabled"
                                       )
        
        
        label = tk.Label(frame0,text="URL",fg="white",font=(FONT, FSIZE2),background=GREEN)
        label.grid(row=0,column=0,sticky='we')
        
        frame0.grid(row=0, column=0, sticky='e')
        frame1.grid(row=0, column=1, sticky='nswe', ipadx=150)
        frame2.grid(row=0, column=2, sticky='nswe')

        self.entry.grid(row=0, column=1, sticky='we', padx=80)
        self.urlButton.grid(row=0, column=2, sticky='we')

        self.url_frame.grid(row=6, column=0, sticky='nsew')

    def mainloop(self):
        self.parent.mainloop()

    def getSavePath(self):
        return self.savePath.get()

    def getOptions(self):
        return[x.get() for x in self.options]

    def updateProgressbar(self, num):
        self.progVar.set(num)

    def build_progressBar_window(self, max:int,progressmode="determinate"):
        self.pgw = tk.Toplevel(background=ORANGE)
        self.pgw.geometry("300x200")
        self.pgw.iconbitmap(self.path+'/icon.ico')
        self.pgw.title("Cargando")
        x = self.parent.winfo_x()
        y = self.parent.winfo_y()
        self.pgw.geometry("+%d+%d" %(x+350,y+150))
        
        label = tk.Label(self.pgw, background=ORANGE,text="Cargando", font=(FONT, FSIZE2), fg="white")
        self.pgw.grid_columnconfigure(0, weight=1)
        self.pgw.grid_rowconfigure(0, weight=1)
        self.pgw.grid_rowconfigure(1, weight=1)
        self.pgw.transient(self.parent)
        if progressmode == "determinate":
            self.progbar = ttk.Progressbar(self.pgw, maximum=max, variable=self.progVar, length=200,mode=progressmode)
        elif progressmode == "indeterminate":
            self.progbar = ttk.Progressbar(self.pgw, maximum=max, length=200,mode=progressmode)
            self.progbar.start()
        label.grid(column=0,row=0,sticky='we')
        self.progbar.grid(column=0, row=1)

    def on_countriesBox(self, event):
        self.countriesBox.set("")
        self.citiesBox.set("")
        with open(self.path+'/geo/'+self.continentes[self.continentsBox.get()]+'.json', 'r') as fp:
            self.paises_file = json.load(fp)

        self.countriesBox.config(values=tuple(self.paises_file.keys()))

    def on_citiesBox(self, event):
        self.citiesBox.set("")
        self.ciudades = {}
        for i in self.paises_file[self.countriesBox.get()]:
            self.ciudades[i['name']] = i['urlFriendlyName']
        self.citiesBox.config(values=tuple(self.ciudades.keys()))

    def unlock_button(self, *arg):
        if self.citiesBox.get().__len__() > 1:
            self.executeButton.config(state="normal")
        else:
            self.executeButton.config(state="disabled")
            
    def unlock_button2(self, *arg):
        if self.urlVar.get().__len__() > 1:
            self.urlButton.config(state="normal")
        else:
            self.urlButton.config(state="disabled")
            
    def saveAsDialogue(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", initialdir="/", title="Select file", filetypes=(("CSV", "*.csv"),("Libro Excel", "*.xlsx")))

        self.savePath.set(path)

    def getCity(self):
        return self.ciudades[self.citiesBox.get()]
    
    def getContinent(self):
        return self.continentes[self.continentsBox.get()]
    
    def getCountry(self):
        return self.countriesBox.get().lower().replace(' ','-')
    
    def getGlobalPoint(self):
        return (self.continentes[self.continentsBox.get()],self.countriesBox.get().lower().replace(' ','-'),self.ciudades[self.citiesBox.get()])
    def setMain(self):
        self.build_title()
        self.build_cBoxes()
        self.build_executeButton()
        self.build_URLEntry()
        self.savePath.trace('w', self.unlock_button)
        self.urlVar.trace('w',self.unlock_button2)

    def destroy_pgBar(self):
        self.pgw.destroy()
    def errorWindow(self,message:str):
        errorWin= Toplevel(self.parent,height=150, width=300) 
        errorWin.title('ERROR')
        errorWin.iconbitmap(self.path+'/icon.ico')
        errorWin.attributes('-topmost', 'true')
        errorWin.transient(self.parent)
        x = self.parent.winfo_x()
        y = self.parent.winfo_y()
        errorWin.geometry("+%d+%d" %(x+350,y+150))
        
        label = tk.Label(errorWin,text=message)
        
        button = tk.Button(errorWin,text='OK',command=errorWin.destroy)
        label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)