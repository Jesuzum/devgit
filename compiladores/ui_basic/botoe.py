import tkinter as tk

ventana = tk.Tk()
ventana.title("Ejemplo boton")

boton = tk.Button(ventana, text="Haz click")
boton.config(fg="white", bg="black", font=("Arial", 12))
boton.pack()

etiqueta = tk.Label(ventana, text="Hola soy un label")
etiqueta.pack()

def cambiar_texto():
    etiqueta.config(text="Haz presionado el boton")

boton.config(command=cambiar_texto)

ventana.mainloop()