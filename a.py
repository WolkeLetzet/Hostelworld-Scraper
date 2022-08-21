import threading as th
import time
import logging
import tkinter as tk

root = tk.Tk()
second_window = tk.Toplevel(root)
threads = [th.Thread(target=root.mainloop())]

threads[0].start()