import tkinter as tk
from PIL import Image as Img

class GifTk:
   
   def __init__(self, label, image_path):
      self.path = image_path #direccion del Gif
      self.label=label #Label en que se encuentra el Gif
      self.n_frames = Img.open(image_path).n_frames #numero de frames de la animacion
      self.frames = [tk.PhotoImage(file=image_path, format='gif -index %i' %(i)) for i in range(self.n_frames)] #fotogramas del Gif
      
   def update(self,label:tk.Label, delay=20,ind=0 ):
      """Actualiza el fotograma actual
      
      Parametros
      ----------
      label : Label
         cuadro de tipo Label en el que se actualiza el fotograma
      delay: int
         velocidad de la animacion
      ----------
      """
      
      frame = self.frames[ind]
      ind += 1
      if ind == self.n_frames:
         ind = 0
      label.configure(image=frame)
      label.image = frame
      label.after(delay, self.update, self.label, delay, ind)

      
   def start(self, delay=20):
      """Inicia la Animacion del Gif"""
      self.label.after(0, self.update,self.label,delay, 0 )

   def stop(self):
      self.label.after_cancel(self.label.after_id)
   
   
   
      