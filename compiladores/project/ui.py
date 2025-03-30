import platform
import tkinter as tk
from tkinter import ttk
from functions import *
def ui_init():
    # Configuración de la ventana principal
    principal = tk.Tk()
    principal.title("Perl Compilator")
    principal.geometry("1600x920")
    principal.minsize(900, 560)
    principal.iconbitmap("assets/icon.ico")
    principal.config(bg="#5b518d")

    #----------------------------------------------------------------------------------------------------------------------
    # Frame de la barra de menú
    if platform.system() == "Darwin":  # macOS
        menubar = tk.Menu(principal)
        principal.config(menu = menubar)

    frame_menu = tk.Frame(principal, height=20, bg="#c2bcdf")
    frame_menu.pack(fill='x')
    frame_menu.pack_propagate(False)

    # Función para desplegar los menús
    def mostrar_menu(menu, boton):
        x, y, _, _ = boton.bbox("insert")  # Obtener posición del botón
        x = boton.winfo_rootx()  # Posición global en X
        y = boton.winfo_rooty() + boton.winfo_height()  # Posición global en Y, debajo del botón
        menu.post(x, y)

    # Configuración de estilos de menú
    menu_bg = "#c2bcdf"
    menu_fg = "black"
    menu_active_bg = "#9885bf"
    menu_active_fg = "white"

    # Función para crear menús
    def crear_menu(ventana):
        menu = tk.Menu(ventana, tearoff=0, bg=menu_bg, fg=menu_fg, activebackground=menu_active_bg,
        activeforeground=menu_active_fg)
        return menu

    # Cargar iconos para los menús
    icono_nuevo = tk.PhotoImage(file="assets/new.png").subsample(30, 30)
    icono_abrir = tk.PhotoImage(file="assets/open.png").subsample(30, 30)
    icono_guardar = tk.PhotoImage(file="assets/save.png").subsample(30, 30)
    icono_salir = tk.PhotoImage(file="assets/exit.png").subsample(4, 4)

    icono_deshacer = tk.PhotoImage(file="assets/deshacer.png").subsample(2, 2)
    icono_rehacer = tk.PhotoImage(file="assets/rehacer.png").subsample(2, 2)
    icono_copiar = tk.PhotoImage(file="assets/copy.png").subsample(3, 3)
    icono_pegar = tk.PhotoImage(file="assets/paste.png").subsample(4, 4)

    icono_lexer = tk.PhotoImage(file="assets/lexer.png").subsample(30, 30)
    icono_parser = tk.PhotoImage(file="assets/parser.png").subsample(30, 30)
    icono_semantic = tk.PhotoImage(file="assets/sintax.png").subsample(30, 30)
    icono_limpiar = tk.PhotoImage(file="assets/clean.png").subsample(30, 30)

    icono_doc = tk.PhotoImage(file="assets/docs.png").subsample(4, 4)
    icono_acerca = tk.PhotoImage(file="assets/about.png").subsample(4, 4)

    # Menús desplegables
    # Menú Archivo
    menu_archivo = crear_menu(principal)
    menu_archivo.add_command(label="Nuevo", image=icono_nuevo, compound="left", command=lambda: nuevo_archivo(editor_texto))
    menu_archivo.add_command(label="Abrir", image=icono_abrir, compound="left", command=lambda: abrir_archivo(editor_texto, principal))
    menu_archivo.add_command(label="Guardar", image=icono_guardar, compound="left", command=lambda: guardar_archivo(editor_texto))
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Salir", image=icono_salir, compound="left", command=lambda: salir(principal, editor_texto))


    # Menú Editar
    menu_editar = crear_menu(principal)
    menu_editar.add_command(label="Deshacer", image=icono_deshacer, compound="left", command=lambda: deshacer(editor_texto))
    menu_editar.add_command(label="Rehacer", image=icono_rehacer, compound="left", command=lambda: rehacer(editor_texto))
    menu_editar.add_separator()
    menu_editar.add_command(label="Copiar", image=icono_copiar, compound="left", command=lambda: copiar(editor_texto))
    menu_editar.add_command(label="Pegar", image=icono_pegar, compound="left", command=lambda: pegar(editor_texto))


    # Menú Ejecutar 
    menu_ejecutar = crear_menu(principal)
    menu_ejecutar.add_command(label="Analisis", image=icono_lexer, compound="left", command=lambda: ejecutar_analisis(editor_texto, salida_texto))
    menu_ejecutar.add_command(label="Código Prueba Sin Errores", image=icono_parser, compound="left",command=lambda: insertar_codigo_prueba(editor_texto, sin_errores=True))
    menu_ejecutar.add_command(label="Código Prueba Con Errores", image=icono_semantic, compound="left",command=lambda: insertar_codigo_prueba(editor_texto, sin_errores=False))
    menu_ejecutar.add_separator()
    menu_ejecutar.add_command(label="Limpiar salida", image=icono_limpiar, compound="left", command=lambda: limpiar_salida(salida_texto))

    # Menú Ayuda
    menu_ayuda = crear_menu(principal)
    menu_ayuda.add_command(label="Documentación", image=icono_doc, compound="left", command=abrir_documentacion)
    menu_ayuda.add_command(label="Atajos", image=icono_acerca, compound="left", command=mostrar_atajos)

    # Botones del menú con función de despliegue
    if platform.system() == "Darwin":
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menubar.add_cascade(label="Editar", menu=menu_editar)
        menubar.add_cascade(label="Ejecutar", menu=menu_ejecutar)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
    else:
        boton1 = tk.Button(frame_menu, text="Archivo", bg=menu_bg, borderwidth=0, activebackground=menu_active_bg,
        command=lambda: mostrar_menu(menu_archivo, boton1))
        boton1.pack(side='left')

        boton2 = tk.Button(frame_menu, text="Editar", bg=menu_bg, borderwidth=0, activebackground=menu_active_bg,
                            command=lambda: mostrar_menu(menu_editar, boton2))
        boton2.pack(side='left')

        boton3 = tk.Button(frame_menu, text="Ejecutar", bg=menu_bg, borderwidth=0, activebackground=menu_active_bg,
                            command=lambda: mostrar_menu(menu_ejecutar, boton3))
        boton3.pack(side='left')

        boton4 = tk.Button(frame_menu, text="Ayuda", bg=menu_bg, borderwidth=0, activebackground=menu_active_bg,
                            command=lambda: mostrar_menu(menu_ayuda, boton4))
        boton4.pack(side='left')

    # Frame contenedor para icono y texto en el lado derecho con ancho fijo
    contenedor_icono = tk.Frame(frame_menu, bg=menu_bg, height=30, width=150)
    contenedor_icono.pack(side="right")
    contenedor_icono.pack_propagate(False) 

    imagen = tk.PhotoImage(file="assets/perl1.png")
    imagen = imagen.subsample(30, 30)

    icono = tk.Label(contenedor_icono, image=imagen, bg=menu_bg)
    icono.pack(side="right")

    name_label = tk.Label(contenedor_icono, text="Perl Compilator", bg=menu_bg, fg="black")
    name_label.pack(side="right") 

    contenedor_icono.image = imagen

    # Borde inferior en referencia al menú
    borde_inferior = tk.Frame(principal, height=1, bg="black")
    borde_inferior.pack(fill='x')


    #----------------------------------------------------------------------------------------------------------------------
    # Frame editor de texto
    frame_editor = tk.Frame(principal, bg="#77747e", borderwidth=0)
    frame_editor.pack(fill="both", expand=True)

    # Estilo para los Scrollbars
    style = ttk.Style()
    style.theme_use("clam")  # Usa un tema que permita personalización

    # Scrollbars con ttk
    scroll_y = ttk.Scrollbar(frame_editor, orient='vertical')
    scroll_y.pack(side='right', fill='y')

    scroll_x = ttk.Scrollbar(frame_editor, orient='horizontal')
    scroll_x.pack(side='bottom', fill='x')

    # Editor de texto
    editor_texto = tk.Text(
        frame_editor, bg="#403853", borderwidth=0, fg="white",
        wrap="none", undo=True,
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )
    editor_texto.pack(fill="both", expand=True)

    # Conectar los Scrollbars al Text
    scroll_y.config(command=editor_texto.yview)
    scroll_x.config(command=editor_texto.xview)

    # Cambiar el fondo del editor de texto
    def cambiar_fondo_editor(editor_texto):
        """Cambiar el fondo del editor de texto y la fuente."""
        color_actual = editor_texto.cget("bg")
        
        if color_actual == "#403853":
            # Cambiar a fondo oscuro y texto blanco
            editor_texto.config(bg="#f3edff", fg="black")
        else:
            # Cambiar a fondo claro y texto blanco
            editor_texto.config(bg="#403853", fg="white")

    #----------------------------------------------------------------------------------------------------------------------
    # Frame de la salida 
    frame_salida = tk.Frame(principal, bg="black", height=200)
    frame_salida.pack(fill="x", side="bottom")
    frame_salida.pack_propagate(False)

    # Agregar un "handle" para redimensionar con el mouse
    handle = tk.Frame(frame_salida, height=5, cursor="sb_v_double_arrow", bg="black")
    handle.pack(fill="x", side="top")

    salida_label = tk.Label(frame_salida, text="Salida >>", bg="black", fg="white")
    salida_label.pack(side="left")

    salida_texto = tk.Text(frame_salida, height=10, bg="black", fg="white", wrap="word")
    salida_texto.pack(fill="both", expand=True, padx=5, pady=5)

    # Función para redimensionar el frame de salida
    def start_resize(event):
        frame_salida._y = event.y_root

    def resize(event):
        dy = event.y_root - frame_salida._y
        new_height = frame_salida.winfo_height() - dy
        if new_height > 50:  # Evitar que se haga demasiado pequeño
            frame_salida.config(height=new_height)
            frame_salida._y = event.y_root

    # Asociar eventos al "handle"
    handle.bind("<ButtonPress-1>", start_resize)
    handle.bind("<B1-Motion>", resize)




    #---------------------------------------------------------------------------------------------------------------------
    # Atajos de teclado
    # Asignar atajos de teclado
    editor_texto.bind("<Control-e>", lambda event: cambiar_fondo_editor(editor_texto))
    principal.bind("<Control-n>", lambda event: nuevo_archivo(editor_texto))
    principal.bind("<Control-o>", lambda event: abrir_archivo(editor_texto))
    principal.bind("<Control-s>", lambda event: guardar_archivo(editor_texto))
    principal.bind("<Control-q>", lambda event: salir(principal))
    principal.bind("<Control-z>", lambda event: editor_texto.edit_undo())
    principal.bind("<Control-y>", lambda event: editor_texto.edit_redo())
    principal.bind("<Control-c>", lambda event: editor_texto.event_generate("<<Copy>>"))
    principal.bind("<Control-v>", lambda event: editor_texto.event_generate("<<Paste>>"))
    principal.bind("<Control-f>", lambda event: buscar_texto(editor_texto))
    principal.bind("<Control-a>", lambda event: seleccionar_todo(editor_texto))
    principal.bind("<Control-l>", lambda event: limpiar_salida(salida_texto))
    principal.bind("<Control-d>", lambda event: abrir_documentacion())
    principal.bind("<Control-h>", lambda event: mostrar_atajos())
    principal.bind("<Control-p>", lambda event: insertar_codigo_prueba(editor_texto, sin_errores=True))
    principal.bind("<Control-t>", lambda event: insertar_codigo_prueba(editor_texto, sin_errores=False))
    principal.bind("<Control-r>", lambda event: ejecutar_analisis(editor_texto, salida_texto))
    #----------------------------------------------------------------------------------------------------------------------
    principal.mainloop()

if __name__ == "__main__": # Si se ejecuta este archivo directamente
    ui_init()