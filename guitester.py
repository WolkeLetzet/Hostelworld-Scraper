import tkinter as tk
from PIL import Image, ImageTk
import scrap as scrap
ORANGE= '#f25621'

######## MAIN WINDOW ########

ventana = tk.Tk()
ventana.title("HostelScraper")
ventana.geometry("600x325")
ventana.iconbitmap("icon.ico")
ventana.config(bg=ORANGE)
ventana.resizable(0, 0)

######## FRAME 1 ########

title_frame = tk.Frame(ventana, bg=ORANGE)

logo=Image.open("scraper logo.png")
logo=ImageTk.PhotoImage(logo)
label_logo=tk.Label(title_frame, image=logo, bg=ORANGE)
label_logo.pack(padx=10, pady=10)

title_frame.pack(side=tk.TOP, fill=tk.X)


######## FRAME 2  ########
entry_frame = tk.Frame(ventana, bg=ORANGE)

scrollbar = tk.Scrollbar(entry_frame,orient="horizontal")
entry = tk.Entry(entry_frame, font=("Sitka Display", 12), width=50, bg="white", fg="black", xscrollcommand=scrollbar.set)
entry.focus()
#entry.bind("<Return>", lambda x: scrap.__main__(entry.get()))
entry.pack(fill=tk.X, padx=10)
scrollbar.config(command=entry.xview)
scrollbar.pack(fill=tk.X, padx=10)
entry_frame.pack( fill=tk.X,ipady=2)

######## FRAME 3 ########

#############  CheckBox  ##############
option1= tk.BooleanVar()
option2= tk.BooleanVar()
option3= tk.BooleanVar()

frame=tk.Frame(ventana, bg=ORANGE)

checkbutton1=tk.Checkbutton(frame, text="Puntaje",
                            variable=option1, onvalue=True, offvalue=False,
                            bg=ORANGE, fg="black", font=("Sitka Display", 11), activebackground=ORANGE, activeforeground="white")
checkbutton2=tk.Checkbutton(frame, text="Todos Los comentarios",
                            variable=option2, onvalue=True, offvalue=False,
                            bg=ORANGE, fg="black", font=("Sitka Display", 11),activebackground=ORANGE, activeforeground="white")
checkbutton3=tk.Checkbutton(frame, text="Solo Comentarios",
                            variable=option3, onvalue=True, offvalue=False,
                            bg=ORANGE, fg="black", font=("Sitka Display", 11), activebackground=ORANGE, activeforeground="white")

checkbutton1.grid(row=0, column=0, padx=10, pady=10)
checkbutton2.grid(row=0, column=1, padx=10, pady=10)
checkbutton3.grid(row=0, column=2, padx=10, pady=10)
frame.pack(padx=10,expand=1, fill=tk.X)


#############  Frame 4  ####################

#############  Search Button  ######################

button_frame = tk.Frame(ventana, bg=ORANGE)

search_button = tk.Button(button_frame, text="Buscar", font=("Sitka Display", 11), bg="white", fg="black",
                          command=lambda: scrap.__main__(entry.get()))

search_button.config(width=10, height=1, activebackground=ORANGE, activeforeground="white",
                     highlightthickness=0, highlightbackground="white")

search_button.pack(ipadx=15, ipady=5, padx=10, pady=10)
button_frame.pack(padx=10, ipady=20)


#############  Main Loop  ###################
ventana.mainloop()
