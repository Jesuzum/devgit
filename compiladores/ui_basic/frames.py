import tkinter as tk
window = tk.Tk()

window.title("Perl compiler")
window.geometry("1600x900")
window.config(bg="#c2bcdf")
"""
frame1 = tk.Frame(window)
frame1.configure(width=300, height=200, bg="red", bd=5)
frame1.pack()

frame2 = tk.Frame(frame1)
frame2.configure(width=100, height=100, bg="blue", bd=5)
frame2.pack()

boton = tk.Button(frame1, text="Hola")
boton.pack()
"""
labelf = tk.LabelFrame(window, text="Grupo de widgets", bg="green", padx=10, pady=10)
labelf.configure(width=300, height=200, bd=5)
labelf.pack()

window.mainloop()