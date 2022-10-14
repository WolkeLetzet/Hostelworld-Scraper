from threading import Thread
import tkinter as tk
from Scraper import Scraper
from gg import GUI

def schedule_check(t):
    """
    Programar la ejecución de la función `check_if_done()` dentro de 
    un segundo.
    """
    root.ventana.after(1000, check_if_done, t)
def check_if_done(t):
    # Si el hilo ha finalizado, restaruar la pantalla principal
    if not t.is_alive():
        root.destroy_loading_frame()
        root.build_main_frame()
        root.button_scrap.config(command=scraping)
    else:
        # Si no, volver a chequear en unos momentos.
        schedule_check(t)

def scraping():
    #th  =Thread(target=scrap.main , args=[root.get_url(),root.get_path(),root.get_options()])
    gui.savePath.get()
    
    scraper.setPropertiesIDs()
    #th.start()
    
    schedule_check(th)
    
    
path='C:\\Users\\n1_na\\Repositorios\\hostelworld scraper'     
root =tk.Tk()
gui = GUI(path,root)
scraper = Scraper()




root.mainloop()