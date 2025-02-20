import time
import tkinter as tk

ventana = tk.Tk()
ventana.title("Ejemplo entry")

etiqueta = tk.Label(ventana, text="lo de abajo es un entry")
etiqueta.pack()

entrada = tk.Entry(ventana)
entrada.config(fg="black", bg="lightgray", font=("Arial", 14, "italic"))
entrada.pack()

entrada.insert(0, "Nombre")

def aplicar_texto():
    texto = entrada.get()
    etiqueta.config(text=texto)

boton_aplicar = tk.Button(ventana, text="Aplicar", command=aplicar_texto)
boton_aplicar.pack()

ventana.mainloop()