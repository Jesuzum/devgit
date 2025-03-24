import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import io
import sys

# Funciones de la barra de menú
# Funciones del boton Archivo
def nuevo_archivo(editor_texto):
    """Crea un nuevo archivo, preguntando si se desean guardar cambios."""
    
    if editor_texto.edit_modified():  # Verifica si hubo cambios en el texto
        respuesta = messagebox.askyesnocancel("Nuevo archivo", "¿Deseas guardar los cambios antes de continuar?")
        
        if respuesta:  # Si elige "Sí", guardar archivo
            guardar_archivo(editor_texto)
        elif respuesta is None:  # Si elige "Cancelar", no hacer nada
            return
    
    # Limpiar el editor de texto
    editor_texto.delete("1.0", tk.END)
    
    # Restablecer estado del editor
    editor_texto.edit_modified(False)  # Restablecer flag de cambios

def abrir_archivo(editor_texto, principal):
    """Abre un archivo y carga su contenido en el editor de texto."""
    archivo = filedialog.askopenfilename(filetypes=[("Archivos Perl", "*.pl"), ("Todos los archivos", "*.*")])
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        editor_texto.delete("1.0", tk.END)
        editor_texto.insert("1.0", contenido)
        principal.title(f"Perl Compilator - {archivo}")

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
# Funciones del boton Ejecutar
def ejecutar_analisis(editor_texto, salida_texto):
    """
    Ejecuta el análisis completo del código presente en el editor:
      1. Análisis Léxico
      2. Análisis Sintáctico
      3. Análisis Semántico
    Se captura la salida de cada etapa y se muestra en el área de salida (salida_texto).
    """
    # Extraer y validar el código de entrada.
    codigo = editor_texto.get("1.0", tk.END).strip()
    salida_texto.delete("1.0", tk.END)
    if not codigo:
        salida_texto.insert("1.0", "No hay código para analizar.")
        return

    resultados = []  # Lista para acumular todos los mensajes de salida.

    # --- Fase Léxica ---
    resultados.append("=== ANÁLISIS LÉXICO ===")
    try:
        from analyzer.lexer import AnalizadorLexico
        analizador_lex = AnalizadorLexico()
        analizador_lex.analizar(codigo)
        tokens = analizador_lex.tokens
        
        resultados.append("Tokens reconocidos:")
        for token, tipo in tokens:
            resultados.append(f"{token}: {tipo}")
        
        if analizador_lex.warnings:
            resultados.append("Advertencias:")
            for warn in set(analizador_lex.warnings):
                resultados.append(warn)
    except Exception as e:
        resultados.append(f"Error en el análisis léxico: {str(e)}")
        salida_texto.insert("1.0", "\n".join(resultados))
        return

    # --- Fase Sintáctica ---
    resultados.append("\n=== ANÁLISIS SINTÁCTICO ===")
    try:
        from analyzer.parser import AnalizadorSintactico
        analizador_sintactico = AnalizadorSintactico(tokens)
        
        # Redirigir la salida de print para capturar los mensajes del parser.
        old_stdout = sys.stdout
        sys.stdout = parser_buffer = io.StringIO()
        
        analizador_sintactico.parse()
        
        sys.stdout = old_stdout  # Restaurar stdout.
        parser_output = parser_buffer.getvalue()
        
        if parser_output.strip():
            resultados.append(parser_output.strip())
        
        if analizador_sintactico.errors:
            resultados.append("Errores sintácticos:")
            for err in analizador_sintactico.errors:
                resultados.append(err)
        else:
            resultados.append("Análisis sintáctico completado sin errores.")
    except Exception as e:
        sys.stdout = old_stdout
        resultados.append(f"Error en el análisis sintáctico: {e}")
        salida_texto.insert("1.0", "\n".join(resultados))
        return

    # --- Fase Semántica ---
    resultados.append("\n=== ANÁLISIS SEMÁNTICO ===")
    try:
        from analyzer.semantic import AnalizadorSemantico
        analizador_semantico = AnalizadorSemantico()
        analizador_semantico.analizar(tokens)
        
        if analizador_semantico.errores:
            resultados.append("Errores semánticos:")
            for err in analizador_semantico.errores:
                resultados.append(err)
        else:
            resultados.append("Análisis semántico completado sin errores.")
    except Exception as e:
        resultados.append(f"Error en el análisis semántico: {e}")

    # Mostrar el resumen completo en el área de salida.
    salida_texto.insert("1.0", "\n".join(resultados))

def insertar_codigo_prueba(editor_texto, sin_errores=True):
    """
    Inserta un código de prueba en el editor de texto.
    Si sin_errores es True, se inserta un código de prueba sin errores;
    de lo contrario, se inserta un código de prueba que contiene errores.
    """
    if sin_errores:
        codigo = (
            "use strict;\n"
            "my $a = 5;\n"
            "sub suma {\n"
            "  my ($x, $y) = @_;\n"
            "  return $x + $y;\n"
            "}\n"
            "my $resultado = suma($a, 10);\n"
            "print $resultado;\n"
        )
    else:
        codigo = (
            "use strict;\n"
            "my $a = ;   # Error: falta valor\n"
            "sub suma {\n"
            "  my ($x, $y) = @_;\n"
            "  return $x + $y;\n"
            "}\n"
            "my $resultado = sum($a, 10);  # Error: nombre de función incorrecto\n"
            "print $resultado;\n"
        )
    # Limpiar el contenido previo del editor y cargar el código de prueba
    editor_texto.delete("1.0", tk.END)
    editor_texto.insert("1.0", codigo)
#---------------------------------------------------------------------------------------------------------------------
# Funciones del boton ayuda
def abrir_documentacion():
    """Abre la documentación oficial de Perl en el navegador."""
    url = "https://perldoc.perl.org/"
    webbrowser.open(url)

def mostrar_atajos():
    """Muestra una ventana con la lista de atajos de teclado disponibles."""
    atajos = """
    Atajos de Teclado:
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