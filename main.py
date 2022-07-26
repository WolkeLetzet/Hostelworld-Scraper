import os
from threading import Thread
import tkinter as tk
import pandas as pd
import Scraper
from gg import GUI
import shutil

scrap1= True

def schedule_check(t):
    """
    Programar la ejecución de la función `check_if_done()` dentro de 
    un segundo.
    """
    root.after(100, check_if_done, t)


def check_if_done(t):
    # Si el hilo ha finalizado, restaruar la pantalla principal
    if not t.is_alive():        
        gui.destroy_pgBar()
        gui.saveAsDialogue()
        
        #guardar archivo en ...
        try:
            if gui.getSavePath().endswith('.xlsx'):
                #convertir a Excel
                pd.read_csv(temporal_path, sep=";", header='infer', ).to_excel(gui.getSavePath(), index=None, header=True)
                
            else:
                shutil.copy(temporal_path,gui.getSavePath())
        except Exception as ex:
            gui.errorWindow(str(ex))
        finally:
            os.remove(temporal_path) #eliminar archivo temporal
            gui.executeButton.config(command=scraping,state='normal',text='Iniciar')
            gui.urlButton.config(command=scrapingSelenium,state='normal')
    else:
        # Si no, volver a chequear en unos momentos.
        if scrap1:
            #actualizar barra de progreso
            gui.updateProgressbar(scraper.counter)
        schedule_check(t)


def scraping():
    '''Iniciar el scraping con la clase Scraper'''
    
    try:
        gui.executeButton.config(state='disabled',text='Cargando')
        scraper.setPropertiesIDs(gui.getContinent(),gui.getCountry(),gui.getCity())
    except Exception as ex:
        gui.executeButton.config(text='Iniciar',state='normal')
        gui.errorWindow(str(ex))
    
    th = Thread(target=scraper.mainloop, 
                args=[
                        temporal_path,
                        gui.getContinent(),
                        gui.getCountry(),
                        gui.getCity(),
                      ]
                )
    try:
        th.start()
    except Exception as ex:
        gui.errorWindow(str(ex))
        raise ex
    else:
        gui.build_progressBar_window(scraper.properties.__len__())
    scrap1=True
    schedule_check(th)



def scrapingSelenium():
    '''Iniciar el scraping con la clase SeleniumScraper '''
    
    gui.urlButton.config(state="disabled")
    #crear hilo de trabajo
    th = Thread(target=Scraper.seleniumMainloop,
                args=[
                        temporal_path,
                        gui.urlVar.get()
                      ]
                )
    try:
        #construir barra de progreso
        gui.build_progressBar_window(100,"indeterminate")
        th.start() #iniciar hilo
    except Exception as ex:
        gui.urlButton.config(state="normal")
        gui.errorWindow(str(ex)) #mostrar error
        raise ex
    scrap1=False
    schedule_check(th)


path = os.path.dirname(os.path.realpath(__file__)) #ruta actual del proyecto
root = tk.Tk() #ventana raiz
temporal_path=path+"/temporal.csv" #direccion del archivo temporal
gui = GUI(path, root) #intanciar Interfaz grafica
gui.setMain() #contruir GUI
scraper = Scraper.Scraper() #instanciar clase Scraper

#configurar botones para distintos metodos de scraping
gui.executeButton.config(command=scraping) 
gui.urlButton.config(command=scrapingSelenium)
root.mainloop()
