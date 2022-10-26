import os
from threading import Thread
import tkinter as tk
from Scraper import Scraper
from gg import GUI
import shutil


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
        try:
            shutil.copy(temporal_path,gui.getSavePath())
        except:
            pass
        finally:
            os.remove(temporal_path)
        gui.executeButton.config(command=scraping)
    else:
        # Si no, volver a chequear en unos momentos.
        gui.updateProgressbar(scraper.counter)
        schedule_check(t)


def scraping():
    scraper.setPropertiesIDs(gui.getCity())
    gui.build_progressBar_window(scraper.properties.__len__())
    th = Thread(target=scraper.mainloop, 
                args=[
                        temporal_path,
                        gui.getCity(),
                      ]
                )

    schedule_check(th)


path = os.path.dirname(os.path.realpath(__file__))
root = tk.Tk()
temporal_path=path+"/temporal.csv"
gui = GUI(path, root)
gui.setMain()
scraper = Scraper()

gui.executeButton.config(command=scraping)

root.mainloop()
