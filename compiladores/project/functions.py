import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

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

def salir(principal, editor_texto):
    """Pregunta al usuario si desea guardar antes de salir."""
    respuesta = messagebox.askyesnocancel("Salir", "¿Quieres guardar los cambios antes de salir?")
    
    if respuesta is None:
        # Si el usuario presiona "Cancelar", no hace nada
        return
    elif respuesta:
        # Si el usuario presiona "Sí", guarda el archivo antes de salir
        guardar_archivo(editor_texto)
    
    # Cierra la aplicación
    principal.quit()
#---------------------------------------------------------------------------------------------------------------------
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

#---------------------------------------------------------------------------------------------------------------------
# Funciones del boton ayuda
def abrir_documentacion():
    """Abre la documentación oficial de Perl en el navegador."""
    url = "https://perldoc.perl.org/"
    webbrowser.open(url)

def mostrar_atajos():
    """Muestra una ventana con la lista de atajos de teclado disponibles."""
    atajos = """
    📌 Atajos de Teclado:
    - Ctrl + N → Nuevo archivo
    - Ctrl + O → Abrir archivo
    - Ctrl + S → Guardar archivo
    - Ctrl + Q → Salir
    - Ctrl + Z → Deshacer
    - Ctrl + Y → Rehacer
    - Ctrl + X → Cortar
    - Ctrl + C → Copiar
    - Ctrl + V → Pegar
    - Ctrl + A → Seleccionar todo
    - Ctrl + E → Cambiar fondo del editor
    """
    messagebox.showinfo("Atajos de Teclado", atajos)

#---------------------------------------------------------------------------------------------------------------------
# Atajos de teclado
def buscar_texto(editor_texto):
    """Abre un cuadro de diálogo para buscar texto en el editor."""
    buscar = tk.simpledialog.askstring("Buscar", "Ingrese el texto a buscar:")
    if buscar:
        inicio = editor_texto.search(buscar, "1.0", stopindex=tk.END)
        if inicio:
            fin = f"{inicio}+{len(buscar)}c"
            editor_texto.tag_add("buscar", inicio, fin)
            editor_texto.tag_config("buscar", background="yellow")
        else:
            messagebox.showinfo("Buscar", "Texto no encontrado.")

def seleccionar_todo(editor_texto):
    """Selecciona todo el texto dentro del editor."""
    editor_texto.tag_add("sel", "1.0", "end")
    return "break"  # Evita que se agregue un carácter accidentalmente
