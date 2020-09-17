from main.options import control_program
from main.options import value_options as values
from tkinter import  *
from tkinter import ttk
from tools.utils import check
from tools.utils import clear
from tools.utils import exit
from tools.utils import get_value
from tools.utils import messagebox
from tools.utils import refreshing
from tools.utils import change
import tools.constant as c
import database.db as db

list_frame = LabelFrame(c.WINDOW, bg = c.BACKGROUND_COLOR, highlightthickness = 0, borderwidth = 0)
program_frame = LabelFrame(c.WINDOW, bg = c.BACKGROUND_COLOR, text = "TIDYUP")
origin_frame = LabelFrame(c.WINDOW, bg = c.BACKGROUND_COLOR, highlightthickness = 0, borderwidth = 0)
modify_frame = LabelFrame(c.WINDOW, bg = c.BACKGROUND_COLOR, highlightthickness = 0, borderwidth = 0)
treeview_style = ttk.Style()
treeview_style.configure('MyStyle.Treeview', rowheight=24)
origin_treebox = ttk.Treeview(origin_frame, height = 1, style='MyStyle.Treeview')
list_treebox = ttk.Treeview(list_frame, height = 4)
selected = False

class interface():
    
    def origen():
        global origin_frame
        global origin_treebox
        
        origin_frame.grid(row = 1, column = 0, columnspan = 48, ipadx = 0, sticky = W, padx = (2, 0), pady = (4, 0))
        
        origin_treebox.grid(row = 0, column = 0, columnspan = 1, sticky = W, padx = (3, 0), pady = (2, 0))
        origin_treebox['columns'] = "OrigenActual"
        origin_treebox["show"] = "headings" 
        origin_treebox.column("#0", width = 0, stretch = NO)
        origin_treebox.column("OrigenActual", anchor = W, width = 471)  
        origin_treebox.heading("#0", text = "", anchor = W)
        origin_treebox.heading("OrigenActual", text = "Carpeta de origen", anchor = W)

        menu.right_click(origin_treebox, "origin")
        
        modify_origin = Button(origin_frame, text = "...", width = 2, borderwidth = 1, command = lambda:[check.new_origin_folder(c.WINDOW, "update", origin_treebox)], bg = c.BUTTON_COLOR, activebackground = c.BUTTON_ACTIVE_COLOR)
        modify_origin.grid(row = 0, column = 0, columnspan = 1, rowspan= 1, padx = (453, 4), pady = (27, 0)) 

        check.origin(origin_frame, "insert", origin_treebox)
        
        refreshing.origin_update(origin_treebox)
    
    def list_box():
        global list_frame
        global list_treebox

        list_frame.grid(row = 2, column = 0, columnspan = 48, ipadx = 0, sticky = W, padx = (2, 2), pady = (3, 5))

        list_treebox.grid(row = 0, column = 0, columnspan = 48, padx = (3, 4), pady = (0, 2), sticky = W)
        list_treebox['columns'] = ("Nombre", "Tidies", "Destino")
        list_treebox["show"] = "headings" 
        list_treebox.column("#0", width = 0, stretch = NO)
        list_treebox.column("Nombre", anchor = W, stretch=True, width = 100)    
        list_treebox.column("Tidies", anchor = W, stretch=True, width = 121)    
        list_treebox.column("Destino", anchor = W, stretch=True, width = 250)
        list_treebox.heading("#0", text = "", anchor = W)
        list_treebox.heading("Nombre", text = "  Nombre", anchor = W)
        list_treebox.heading("Tidies", text = "  Tidies", anchor = W)
        list_treebox.heading("Destino", text = "  Destino", anchor = W) 
        
        check.yscroll(list_frame, list_treebox)

        menu.right_click(list_treebox, "lists") 
        interface.search(list_frame)       
        
        results = db.select_list("tidytable")        
        refreshing.update(results, list_frame, list_treebox)

    def search(window):
        global list_frame
        global list_treebox
        global search_box
        path_comment = "Selecciona el directorio a buscar en las listas"
        
        search_box = Entry(window, width = 43)
        search_box.grid(row = 1, column = 0, columnspan = 4, ipady = 3, sticky = W, padx = (78, 0), pady = (2, 3))
        
        search_origin = Button(window, text = "...", width = 2, borderwidth = 1, command = lambda:[get_value.path(window, search_box, path_comment)], bg = c.BUTTON_COLOR, activebackground = c.BUTTON_ACTIVE_COLOR)
        search_origin.grid(row = 1, column = 0, columnspan = 2, rowspan= 1, padx = (183, 0), pady = (0, 0))  
        search_button = Button(window, text = "Buscar", width = 7, borderwidth = 1, command = lambda:[values.search(list_frame, search_box, list_treebox)], bg = c.BUTTON_COLOR, activebackground = c.BUTTON_ACTIVE_COLOR)
        search_button.grid(row = 1, column = 0, columnspan = 2, rowspan= 1, ipady = 0.35, padx = (280, 0), pady = (0, 0))
        clear_button = Button(window, text = "Refrescar", width = 8, borderwidth = 1, command = lambda:[clear.search(list_frame, list_treebox), clear.textbox(search_box)], bg = c.BUTTON_COLOR, activebackground = c.BUTTON_ACTIVE_COLOR)
        clear_button.grid(row = 1, column = 0, columnspan = 2, rowspan= 1, ipady = 0.35, padx = (411, 0), pady = (0, 0))

        menu_button = Menubutton (window, text = "Opciones", width = 9, borderwidth = 1, relief = RAISED, bg = c.BUTTON_COLOR, activebackground = c.BUTTON_ACTIVE_COLOR)
        menu_button.grid(row = 1, column = 0, sticky = W, padx = (4, 0), pady = (0, 0))
        menu_button.menu = Menu(menu_button, tearoff = 0)
        menu_button["menu"] = menu_button.menu
        menu_button.menu.add_command(label = "Crear lista", command = lambda:[interface.modify("insert")])
        menu_button.menu.add_command(label = "Modificar lista", command = lambda:[interface.modify("modify"), menu.get_row(menu.double_click(list_treebox))])
        menu_button.menu.add_command(label ="Borrar lista", command = lambda:[values.delete(list_frame, list_treebox)])
        menu_button.menu.add_command(label = "Cerrar pestaña", command = lambda:[interface.quit_frame_modify(modify_frame)]) 
        menu_button.menu.add_separator()
        menu_button.menu.add_command(label ="Iniciar Tidyup", command = lambda:[control_program.start(), menu_button.menu.entryconfig(6, state = NORMAL), menu_button.menu.entryconfig(5, state = DISABLED), change.options_button_color("forest green", menu_button)])
        menu_button.menu.add_command(label ="Parar Tidyup", state = DISABLED, command = lambda:[control_program.pause(), menu_button.menu.entryconfig(5, state = NORMAL), menu_button.menu.entryconfig(6, state = DISABLED), change.options_button_color("red", menu_button)])
        menu_button.menu.add_separator()
        menu_button.menu.add_command(label ="Cerrar Tidyup", command = lambda:[exit.program(c.WINDOW)])
        menu_button.menu.entryconfig(5, foreground= "green")
        menu_button.menu.entryconfig(6, foreground= "red")
        
        menu.right_click(search_box, "edit_text")
        
        def on_entry_click(event):
            if search_box.get() == 'Buscador':
                search_box.delete(0, "end")
                search_box.insert(0, '') 
                search_box.config(fg = 'black')
    
        def on_focusout(event):
            if search_box.get() == '':
                search_box.insert(0, 'Buscador')
                search_box.config(fg = 'grey')
        
        def enterKey_bind(event):
            values.search(list_frame, search_box, list_treebox)
            
        search_box.bind('<Return>', enterKey_bind)        
        search_box.bind('<FocusIn>', on_entry_click)
        search_box.bind('<FocusOut>', on_focusout)
        search_box.insert(0, 'Buscador')
        search_box.config(fg = 'grey')
    
    def modify(option):
        global modify_frame
        global list_treebox
        global down
        global list_frame
        path_comment = "Selecciona la carpeta de destino"

        c.WINDOW.geometry(c.WINDOW_SIZE_FOR_MODIFY)
        modify_frame.destroy()
        modify_frame = LabelFrame(c.WINDOW, bg = c.BACKGROUND_COLOR, highlightthickness = 0, borderwidth = 0)
        modify_frame.grid(row = 3, column = 0, columnspan = 48, padx = (2, 0))

        name = Label(modify_frame, text = "Nombre", bg = c.BACKGROUND_COLOR)
        name.grid(row = 0, column = 0, sticky = "sw", padx = (2, 0))
        tidies = Label(modify_frame, text = "Tidies", bg = c.BACKGROUND_COLOR)
        tidies.grid(row = 1, column = 0, sticky = "sw", padx = (2, 0))
        path = Label(modify_frame, text = "Destino", bg = c.BACKGROUND_COLOR)
        path.grid(row = 2, column = 0, sticky = "sw", padx = (2, 0))        
        c.NAME_BOX = Entry(modify_frame, width = 54)
        c.NAME_BOX.grid(row = 0, column = 2, columnspan = 4, ipady = 2, sticky = W, padx = (15, 270))
        c.TIDIES_BOX = Entry(modify_frame, width = 54)
        c.TIDIES_BOX.grid(row = 1, column = 2, columnspan = 4, ipady = 2, sticky = W,  pady = (1, 0), padx = (15, 5))
        c.PATH_BOX = Entry(modify_frame, width = 54)
        c.PATH_BOX.grid(row = 2, column = 2, columnspan = 4, ipady = 3, sticky = W, pady = (1, 0), padx = (15, 5))
        
        if option == "modify": 
            save_command = lambda:[values.modify(list_frame, list_treebox)]    
        elif option == "insert":
            save_command = lambda:[values.insert(list_frame, list_treebox)]       
        
        menu.right_click(c.NAME_BOX, "edit_text")
        menu.right_click(c.TIDIES_BOX, "edit_text")
        menu.right_click(c.PATH_BOX, "edit_text")
        
        path_button = Button(modify_frame, text = "...", width = 2, borderwidth = 1, command = lambda:[get_value.path(modify_frame, c.PATH_BOX, path_comment)], bg = c.BUTTON_COLOR, activebackground = c.BUTTON_ACTIVE_COLOR)
        path_button.grid(row = 2, column = 2, columnspan = 1, sticky = W, padx = (321, 0), pady = (2, 0))
        save_modify = Button(modify_frame, text = "Guardar", width = 9, pady = 25, borderwidth = 1, command = save_command, bg = c.BUTTON_COLOR, activebackground = c.BUTTON_ACTIVE_COLOR)
        save_modify.grid(row = 0, column = 2, columnspan = 2, rowspan= 3, sticky = W, padx = (353, 2))
        
        def on_entry_click(event):
            if c.TIDIES_BOX.get() == 'Inserta un espacio entre los tidies (.txt importante .gif)':
                c.TIDIES_BOX.delete(0, "end")
                c.TIDIES_BOX.insert(0, '') 
                c.TIDIES_BOX.config(fg = 'black')
    
        def on_focusout(event):
            if c.TIDIES_BOX.get() == '':
                c.TIDIES_BOX.insert(0, 'Inserta un espacio entre los tidies (.txt importante .gif)')
                c.TIDIES_BOX.config(fg = 'grey')
        
        c.TIDIES_BOX.insert(0, 'Inserta un espacio entre los tidies (.txt importante .gif)')
        c.TIDIES_BOX.bind('<FocusIn>', on_entry_click)
        c.TIDIES_BOX.bind('<FocusOut>', on_focusout)
        c.TIDIES_BOX.config(fg = 'grey')

    def quit_frame_modify(treebox):
        global list_frame
        treebox.destroy()
        c.WINDOW.geometry(c.SIZE)
        
class menu():

    def get_row(event):
        try:
            global list_treebox
            
            interface.modify("modify")
            clear.textbox(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX)
            #row_name = c.LISTA.identify_row(event.y)
            item = list_treebox.item(list_treebox.focus())
            c.NAME_BOX.insert(0, item['values'][0])  
            c.TIDIES_BOX.insert(0, item['values'][1].replace(",", ""))
            c.TIDIES_BOX.config(fg = 'black')
            c.PATH_BOX.insert(0, item['values'][2])
            c.ID_LIST = db.select_id_for_name(item['values'][0])
        except IndexError:
            pass
        except Exception as error:
            messagebox.error(error)   
    
    def right_click(box, option):
        popup_menu = Menu(box, tearoff = 0)

        def copy(event):
            global selected
            
            if event:
                selected = c.WINDOW.clipboard_get()
                
            if box.selection_get():
                selected = box.selection_get()
                c.WINDOW.clipboard_get()
                c.WINDOW.clipboard_append(selected)
                    
        def cut(event):
            global selected
            
            if event:
                selected = c.WINDOW.clipboard_get()               
            else:
                if  box.selection_get():
                    selected = box.selection_get()
                    box.delete("sel.first","sel.last")
                    c.WINDOW.clipboard_get()
                    c.WINDOW.clipboard_append(selected)

        def paste(event):
            global selected
            
            if event:
                selected = c.WINDOW.clipboard_get()               
            else:
                if selected:
                    position = box.index(INSERT)
                    box.insert(position, selected)  
        
        def do_popup(event): 
            try: 
                popup_menu.tk_popup(event.x_root, event.y_root) 
            finally: 
                popup_menu.grab_release()
        
        def program_menu():
            global list_frame
        
        if option == "lists": 
            #double_click = box.bind("<Double 1>", menu.get_row)                    
            popup_menu.add_command(label ="Crear lista", command = lambda:[interface.modify("insert")])        
            popup_menu.add_command(label ="Modificar lista", command = lambda:[menu.get_row(menu.double_click(box))])
            popup_menu.add_command(label ="Borrar listas", command = lambda:[values.delete(list_frame, box)])   
        elif option == "origin":
            popup_menu.add_command(label ="Modificar origen", command = lambda:[check.new_origin_folder(c.WINDOW, "update", origin_treebox)])       
        elif option == "edit_text":
            popup_menu.add_command(label ="Copiar", command = lambda:[copy(False)])        
            popup_menu.add_command(label ="Cortar", command = lambda:[cut(False)])
            popup_menu.add_command(label ="Pegar", command = lambda:[paste(False)])

            c.WINDOW.bind('<Control-c>', copy)
            c.WINDOW.bind('<Control-x>', cut)
            c.WINDOW.bind('<Control-v>', paste)             
        
        box.bind("<Button-3>", do_popup)

    def double_click(box):
        double_click = box.bind("<Double 1>", menu.get_row)
        return double_click
