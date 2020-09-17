from main.program import MyHandler
from tools.utils import check
from tools.utils import clear
from tools.utils import get_value
from tools.utils import messagebox
from tools.utils import refreshing
import tools.constant as c
import database.db as db
import os

class value_options():   
    
    def insert(window, treebox):
        try:
            if check.name(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX, "insert"):
                if check.tidies(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX, "insert"):
                    if check.path(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX):
                        name = c.NAME_BOX.get()
                        tidies = str(c.TIDIES_BOX.get().split())
                        path = c.PATH_BOX.get()
                        db.insert(name, tidies, path)
                        results = db.select_list("tidytable") 
                        refreshing.update(results, window, treebox)
                        clear.textbox(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX)
        except Exception as error:
            clear.textbox(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX)
            messagebox.error(error)
    
    # Moodify                 
    def modify(window, treebox):
        try:
            if check.name(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX, "modify"):
                if check.tidies(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX, "modify"):
                    if check.path(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX):
                        name = c.NAME_BOX.get()
                        tidies = str(c.TIDIES_BOX.get().split())
                        path = c.PATH_BOX.get()
                        clear.textbox(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX)
                        db.update(c.ID_LIST, name, tidies, path)
                        results = db.select_list("tidytable")
                        refreshing.update(results, window, treebox)
        except Exception as error:
            clear.textbox(c.NAME_BOX, c.TIDIES_BOX, c.PATH_BOX)
            messagebox.error(error) 
    # Delete a list   
    def delete(window, list_treebox):
        try:
            lists = list_treebox.selection()
            for aList in lists:
                name_list = list_treebox.item(aList)["values"][0]
                id_list = get_value.list_id(name_list)
                response = messagebox.ask('¿Quiere borrar la lista "' + name_list + '"?')
                if response == 'yes':
                    db.delete(id_list)
                    results = db.select_list("tidytable")  
                    refreshing.update(results, window, list_treebox)
        except Exception as error:
            messagebox.error(error)               
    # Origin
    def origin(path_box):
        try:
            if check.path(None, None, path_box) == True:
                origin_path = path_box.get()
                origin_path = origin_path + r"\tidyup"
                origin_path = os.path.normpath(origin_path)
                dbPath = db.select_origin_path("tidyup", "string")
                dbPath = os.path.normpath(dbPath)
                if sum(1 for results in db.select_list("origin")) == 0:
                    # Insert origin path
                    db.insert_origin_path('tidyup', origin_path)
                    if os.path.exists(origin_path) == False:
                        os.makedirs(origin_path)
                        messagebox.info('La carpeta "tidyup" se ha creado correctamente\nLa ruta es la siguiente: ' + origin_path)
                        clear.textbox(path_box)
                        return origin_path                      
                elif origin_path == dbPath:
                    if os.path.exists(origin_path) == False:
                        os.makedirs(origin_path)
                        messagebox.info('Se ha creado la carpeta "tidyup" en la ruta introducida')
                        clear.textbox(path_box)    
                    else:
                        messagebox.info('La carpeta "tidyup" ya se encuentra en la ruta introducida')
                        clear.textbox(path_box)
                    return origin_path
                elif os.path.exists(origin_path):
                    # Update origin path
                    db.update_origin_path('tidyup', origin_path)
                    messagebox.info('Ahora "tidyup" se encuentra en la siguiente ruta: ' + origin_path)
                    clear.textbox(path_box) 
                    return origin_path
                else:
                    # Update origin path
                    db.update_origin_path('tidyup', origin_path)
                    messagebox.info('Ahora "tidyup" se encuentra en la siguiente ruta: ' + origin_path)
                    os.makedirs(origin_path) # Create directory
                    clear.textbox(path_box)
                    return origin_path
        except Exception as error:
            clear.textbox(path_box)
            messagebox.error(error)             
    
    def search(window, textbox, treebox):
        try:
            user_query = textbox.get()
            results = db.select_for_query(user_query)
            refreshing.update(results, window, treebox)
        except Exception as error:
            messagebox.error(error) 

class control_program():  

    def start():
        c.PROGRAM = True
        MyHandler.__init__(True)
    
    def pause():
        c.PROGRAM = False              
