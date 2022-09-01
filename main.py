from GUI import GUI
from threading import Thread
import scrap

def schedule_check(t):
    """
    Programar la ejecución de la función `check_if_done()` dentro de 
    un segundo.
    """
    root.ventana.after(1000, check_if_done, t)
def check_if_done(t):
    # Si el hilo ha finalizado, restaruar el botón y mostrar un mensaje.
    if not t.is_alive():
        root.destroy_loading_frame()
        root.build_main_frame()
        root.button_scrap.config(command=scraping)
    else:
        # Si no, volver a chequear en unos momentos.
        schedule_check(t)

def scraping():
    th  =Thread(target=scrap.main , args=[root.get_entry(),"reviews.xlsx",root.options])
    root.destroy_main_frame()
    root.build_loading_frame()
    th.start()
    
    schedule_check(th)
    
    

root =GUI()

root.button_scrap.config(command=scraping)

root.mainloop()
