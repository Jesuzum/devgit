import tkinter as tk

ventana = tk.Tk()
ventana.title("Ejemplo label")

etiqueta = tk.Label(ventana, text="Hola, soy un label")
etiqueta.config(fg="blue", bg="yellow", font=("Arial", 14, "italic"))
etiqueta.pack()

ventana.mainloop()