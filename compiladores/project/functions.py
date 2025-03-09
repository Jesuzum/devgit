import tkinter as tk
from tkinter import filedialog, messagebox

# Funciones de la barra de menú
# Funciones del boton Archivo
def nuevo_archivo(editor_texto):
    """Borra el contenido del editor de texto."""
    editor_texto.delete("1.0", tk.END)

def abrir_archivo(editor_texto):
    """Abre un archivo y carga su contenido en el editor."""
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if ruta_archivo:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            editor_texto.delete("1.0", tk.END)
            editor_texto.insert("1.0", contenido)

def guardar_archivo(editor_texto):
    """Guarda el contenido del editor en un archivo."""
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if ruta_archivo:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(editor_texto.get("1.0", tk.END))
        messagebox.showinfo("Guardar", "Archivo guardado correctamente")

def salir(principal):
    """Cierra la aplicación."""
    principal.quit()

# Funciones del boton Editar
def deshacer(editor_texto):
    """Deshace la última acción en el editor de texto."""
    editor_texto.edit_undo()

def rehacer(editor_texto):
    """Rehace la última acción deshecha en el editor de texto."""
    editor_texto.edit_redo()

def copiar(editor_texto):
    """Copia el texto seleccionado al portapapeles."""
    editor_texto.event_generate("<<Copy>>")

def pegar(editor_texto):
    """Pega el texto del portapapeles en la posición actual del cursor."""
    editor_texto.event_generate("<<Paste>>")
