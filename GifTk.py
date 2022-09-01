import tkinter as tk
from PIL import Image as Img

class GifTk:
   
   def __init__(self, label, image_path):
      self.path = image_path
      self.label=label
      self.n_frames = Img.open(image_path).n_frames
      self.frames = [tk.PhotoImage(file=image_path, format='gif -index %i' %(i)) for i in range(self.n_frames)]
      
   def update(self,label, delay=20,ind=0 ):
      frame = self.frames[ind]
      ind += 1
      if ind == self.n_frames:
         ind = 0
      label.configure(image=frame)
      label.image = frame
      label.after(delay, self.update, self.label, delay, ind)

      
   def start(self, delay=20):
      self.label.after(0, self.update,self.label,delay, 0 )

   def stop(self):
      self.label.after_cancel(self.label.after_id)
   
   
   
      