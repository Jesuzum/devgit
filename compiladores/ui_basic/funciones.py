import tkinter as tk

"""
def on_click(event):
    print("Boton presionado")
ventana = tk.Tk()

button = tk.Button(ventana, text="Haz click aquí")
button.pack()
button.bind("<Button-1>", on_click)

def on_key_press(event):
    if event.char == "a":
        print("Presionaste la tecla a")

ventana.bind("<KeyPress>", on_key_press)

def on_resize(event):
    print(f"La ventana ha sido redimensionada a {event.width}x{event.height}")

ventana.bind("<Configure>", on_resize)

def on_mouse_move(event):
    print(f"Mouse movido a {event.x}, {event.y}")

ventana.bind("<Motion>", on_mouse_move)
"""
def on_click(event):
    print(f"Boton {event.widget['text']} presionado")
ventana = tk.Tk()

buttons = [tk.Button(ventana, text=f"Boton {i}") for i in range(3)]
for button in buttons:
    button.pack()
    button.bind("<Button-1>", on_click)

ventana.mainloop()