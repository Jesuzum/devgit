import tkinter as tk                 
from tkinter import ttk

class Gui:
    def __init__(self,mainframe):

        #set the style
        style = ttk.Style()
        style.configure('Horizontal.TScrollbar',background = "blue" )   

        #Create a mainframe
        self.mainframe = mainframe
        self.mainframe.title("example")


        #creating scrollbar frame
        scrl_attr_frame = ttk.Frame(self.mainframe)                            
        scrl_attr_frame.grid(column=0,row=5,sticky="ns")                                           
        scrl_attr_frame.rowconfigure(0, weight=1)                                                   
        attr_canvas = tk.Canvas(scrl_attr_frame)                                                   
        h_scroll = ttk.Scrollbar(scrl_attr_frame,orient="horizontal", command=attr_canvas.xview)
        attr_canvas.configure(xscrollcommand=h_scroll.set)                                       
        attr_canvas.grid(column=0,row=0,sticky="ns")                                                                            
        h_scroll.grid(column=0, row=1,sticky="we") 
        attr_frame = ttk.Frame(attr_canvas)                                                        
        attr_frame.grid(column=0,row=0,sticky="ns")                                                 
        attr_canvas.create_window((0,0),window=attr_frame, anchor='nw')
        attr_frame.bind("<Configure>",lambda event, canvas=attr_canvas : canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200,takefocus=False,highlightthickness=0))#attribute_frame.winfo_height()/20,highlightthickness=0))

        #setup treeview widget
        tree_columns = ("c1", "c2", "c3")

        self.tree = ttk.Treeview(attr_frame,columns=tree_columns, show="headings",takefocus=False)
        self.tree.grid(column=0, row=0, sticky='nsew')

        for head in tree_columns:
            self.tree.heading(head,text=head,anchor="w")


root = tk.Tk()
myapp = Gui(root)
root.mainloop()