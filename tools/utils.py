from tkinter import  *
from tkinter import filedialog
from tkinter import messagebox as m
from tkinter import ttk
import database.db as db
import os
import subprocess
import tools.constant as c
import unicodedata

class refreshing():
    
    def update(results, window, treebox):
        treebox.delete(*treebox.get_children())
        for index, result in enumerate(results):
            r={'[':'',']':'',"'":'',',':''}
            tidies = ''.join(r.get(s,s) for s in result[1])
            treebox.insert(parent="", index="end", iid=index, text="Parent", values=(result[0], tidies, result[2]))
        check.yscroll(window, treebox)
    
    def origin_update(treebox):
        results = db.select_origin_path("tidyup", "list")
        treebox.delete(*treebox.get_children())
        for index, result in enumerate(results):
            treebox.insert(parent="", index="end", iid=index, text="Parent", values=result[0].replace('\\', r"\\"))                                      

class clear():          
    
    def textbox(*args):
        for arg in args:
            if arg != None:
                arg.delete(0, END)
    
    def search(window, treebox):
        results = db.select_list("tidytable")   
        refreshing.update(results, window, treebox)


class get_value():
    
    def list_id(list_name):
        return db.select_id_for_name(list_name)
    
    def path(window, box, comment):
        try:
            user_directory = os.environ['USERPROFILE'] 
            window.tempdir = filedialog.askdirectory(parent = window, initialdir = user_directory, title = comment)
            path = os.path.normpath(window.tempdir)
            if not window.tempdir:
                pass
            else:
                clear.textbox(box)
                box.insert(0, path)
                box.config(fg = 'black')
        except Exception as error:
            messagebox.error(error) 

class window_position():
    
    def capture(window):
        x = window.winfo_x()
        y = window.winfo_y()
        position = str(x) + " " + str(y)
        # Create, open and write position
        file = open('dump.txt', 'w')
        file.write(position)
        file.close()

    def apply():
        window_position.check_dump_file()      
        file = open('dump.txt', 'r')
        position = file.read()
        position = tuple(position.split(" "))
        position_in_screen = "+"+ str(position[0]) + "+" + str(position[1])
        file.close()
        return position_in_screen

    def check_dump_file():
        if os.path.exists('.\dump.txt') == False:
            db.create_table()
            db.create_table_origin()
            c.WINDOW.eval('tk::PlaceWindow . center')
            window_position.capture(c.WINDOW)  

class exit():
    
    def program(window):
        window_position.capture(window) # Capture window position
        pid = os.getpid()
        subprocess.check_output("Taskkill /PID %d /F" % pid) # Kill task
        
    
class check():
    
    def name(name_box, tidies_box, path_box, option):
        try:
            name = name_box.get().lower()
            list_id = c.ID_LIST
            if not name_box.get():
                clear.textbox(name_box)
                messagebox.error("Introduce el nombre de la lista")
            elif option == "modify": 
                if db.different_id("name_list", name, list_id) > 0:
                    clear.textbox(name_box)
                    messagebox.error("Ya se encuentra una lista con este nombre")
                else:
                    return True 
            elif option == "insert":
                if db.check_value("name_list", name) > 0:
                    clear.textbox(name_box)
                    messagebox.error("Ya se encuentra una lista con este nombre")            
                else:
                    return True 
        except Exception as error:
            clear.textbox(name_box, tidies_box, path_box)
            messagebox.error(error) 
    
    def tidies(name_box, tidies_box, path_box, option):
        #try:
        list_id = c.ID_LIST
        if not tidies_box.get():
            clear.textbox(name_box, tidies_box, path_box)
            messagebox.error("No has introducido ningún tidy")
        elif option == "modify":
            tidies = tidies_box.get().lower().split(" ")
            for tidy in tidies:
                if db.different_id("tidy_list", tidy, list_id) > 0:
                    clear.textbox(tidies_box)
                    messagebox.error('El tidy "'+ tidy +'" ya se encuentra en otra lista') 
                    return False
            result = check.repeated_tidy(tidies_box)        
            return result
        elif option == "insert":
            tidies = tidies_box.get().lower().split(" ")      
            for tidy in tidies:
                if db.check_value("tidy_list", tidy) == 1:
                    clear.textbox(tidies_box)
                    messagebox.error('El tidy "'+ tidy +'" ya se encuentra en otra lista')
                    return False
            return True        
        #except Exception as error:
        #    clear.textbox(tidies_box)
        #    messagebox.error(error)
            
    def repeated_tidy(tidies_box):
        tidies = tidies_box.get()
        check_tidies = tidies.lower().split(" ")
        if len(set(check_tidies)) < len(check_tidies):
            clear.textbox(tidies_box)
            messagebox.error('Uno de los tidies introducidos ya se encuentra en la lista') 
            return False       
        else:
            return True 
        
    def path(name_box, tidies_box, path_box):
        try:
            if not path_box.get():
                messagebox.error("Introduce el destino")
            elif os.path.exists(path_box.get()):
                return True
            else:
                response = m.askokcancel("¡Atención!", "¿Crear la carpeta en la ruta indicada?")
                if response == 1:
                    os.makedirs(path_box.get())
                    return True
                else:
                    clear.textbox(path_box)
                    return False 
        except Exception as error:
            clear.textbox(name_box, tidies_box, path_box)
            messagebox.error(error) 
                
    def origin(window, option, treebox):
        try:
            if sum(1 for results in db.select_list("origin")) == 0:
                boolean = False
                while boolean == False:
                    boolean = check.new_origin_folder(window, option, treebox)
                    if boolean == False:             
                        messagebox.info('Tienes que seleccionar la ubicación en la cual se creara la carpeta de origen "tidyup"; esta carpeta se encargara de organizar los archivos que el usuario vaya añadiendo.')
        except Exception as error:
            messagebox.error(error)
    
    def new_origin_folder(window, option, treebox):
        user_directory = os.environ['USERPROFILE']    
        window.tempdir = filedialog.askdirectory(parent=window, initialdir=user_directory, title='Selecciona el directorio en el que se creara la carpeta de origen')
        origin_folder = os.path.normpath(window.tempdir + "/tidyup")
        message = 'La carpeta organizadora "tidyup" se ha creado correctamente'
        if not window.tempdir:
            return False
        else:
            origin_folder = os.path.normpath(window.tempdir + "/tidyup")
            if os.path.exists(origin_folder):
                if option == "insert":
                    messagebox.with_insert_and_directory(make_folder=False, origin_folder=origin_folder, message=message)
                elif option == "update":
                    messagebox.with_update_and_directory(make_folder=False, origin_folder=origin_folder, message=message)
                refreshing.origin_update(treebox)                  
                return True
            else:
                refreshing.origin_update(treebox)    
                if option == "insert":
                    messagebox.with_insert_and_directory(make_folder=True, origin_folder=origin_folder, message=message)
                elif option == "update":
                    messagebox.with_update_and_directory(make_folder=True, origin_folder=origin_folder, message=message)
                refreshing.origin_update(treebox) 
                return True

    def yscroll(window, treebox):
        if sum(1 for results in db.select_list("tidytable")) > 4:
            yscrollbar = ttk.Scrollbar(window, orient = "vertical", command = treebox.yview)           
            yscrollbar.grid(row = 0, column = 1, sticky = "ns", padx = (389, 0), pady = (25, 3))
            treebox.configure(yscrollcommand = yscrollbar.set)

class messagebox():
    
    def error(message):
        m.showwarning("Error", message)
    
    def info(message):
        m.showinfo("Información", message)
    
    def with_insert_and_directory(make_folder, origin_folder, message):
        try:
            if make_folder:
                os.makedirs(origin_folder)
            db.insert_origin_path('tidyup', origin_folder)
            m.showinfo("Información", message)
        except Exception as error:
            m.showwarning("Error", error)
    
    def with_update_and_directory(make_folder, origin_folder, message):
        try:
            if make_folder:
                os.makedirs(origin_folder)
            db.update_origin_path('tidyup', origin_folder)
            m.showinfo("Información", message)
        except Exception as error:
            m.showwarning("Error", error)        
    
    def ask(message):
        return m.askquestion("askquestion", message)         

class change():
    def options_button_color(color, button):
        button.config(fg = color, activeforeground = color)