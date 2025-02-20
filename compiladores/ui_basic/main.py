import tkinter as tk

window = tk.Tk()

window.title("Perl compiler")
window.geometry("1600x900")
window.minsize(1400, 900)
window.iconbitmap("assets/iconperl.ico")
window.config(bg="#c2bcdf")

labelf = tk.LabelFrame(window, text="Grupo de widgets", bg="green", padx=10, pady=10)
labelf.configure(width=300, height=200, bd=5)
labelf.pack()


window.mainloop()