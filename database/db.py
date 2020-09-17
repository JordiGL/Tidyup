from collections import namedtuple
import os
import sqlite3

# CREATE

# gui
def create_table():
    connection = sqlite3.Connection('tidyup.db') # Connect to database
    cursor = connection.cursor() # Create cursor
    # Query the database
    command = "CREATE TABLE IF NOT EXISTS tidytable(name_list TEXT, tidy_list TEXT,  path_folder TEXT)"
    cursor.execute(command)
    connection.commit() # Commit  changes
    connection.close() # Close connection
# gui
def create_table_origin():
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    command = "CREATE TABLE IF NOT EXISTS origin(folder_name TEXT PRIMARY KEY, path_folder TEXT)"
    cursor.execute(command)
    connection.commit()
    connection.close()

# INSERT

# insert
def insert(name, tidies, path):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tidytable VALUES (:name_list, :tidy_list, :path_folder)",
            {
                'name_list': name,
                'tidy_list': tidies,
                'path_folder': path        
            })
    connection.commit()
    connection.close()
    
# origin
def insert_origin_path(name_folder, folder_path):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    cursor.execute("INSERT or IGNORE INTO origin VALUES (:folder_name, :path_folder)",
            {
                'folder_name': name_folder,
                'path_folder': folder_path        
            })
    connection.commit()
    connection.close()

# SELECT

# insert
def check_value(row, value):
    # convert name to a set type for compare with results
    n = ""
    n = set(n)
    n.add(value)
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    if row == "name_list":
        cursor.execute("SELECT name_list FROM tidytable")
    elif row == "tidy_list":
        cursor.execute("SELECT tidy_list FROM tidytable")
    elif row == "id":
        cursor.execute("SELECT oid FROM tidytable")  
    results = str(cursor.fetchall())
    # Clean a str
    r={'[':'',']':'',"'":'', ',':'','(':'',')':'','"':''}
    results = ''.join(r.get(s,s) for s in results)
    # Convert str to a set type
    results = set(results.lower().split(" "))
    connection.commit()
    connection.close()
    # Search value in results 
    found = len(n & results) 
    return found

# modify
def different_id(row, value, id_list):
    # convert name to a set type for compare with results
    n = ""
    n = set(n)
    n.add(value)
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    if row == "name_list":
        cursor.execute("SELECT name_list FROM tidytable WHERE oid != :id", {'id': id_list})
    elif row == "tidy_list":
        cursor.execute("SELECT tidy_list FROM tidytable WHERE oid != :id", {'id': id_list})
    elif row == "path_folder":
        cursor.execute("SELECT tidy_list FROM tidytable WHERE oid != :id", {'id': id_list})    
    results = str(cursor.fetchall())
    # Clean a str
    r={'[':'',']':'',"'":'', ',':'','(':'',')':'','"':''}
    results = ''.join(r.get(s,s) for s in results)
    # Convert str to a set type
    results = set(results.lower().split(" "))
    connection.commit()
    connection.close()
    # Search value in results 
    found = len(n & results) 
    return found

# modify
def select(row, id_list):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tidytable WHERE oid = " + str(id_list))
    results = tuple(cursor.fetchall())
    listas = namedtuple('Lista','Nombre Tidies Destino')
    for index, x in enumerate(results):   
        tidies = x[1].replace("'",'').replace(']','').replace('[','')
        lista = listas(x[0], tidies, x[2])
        documentos = listas._make(lista)   
    connection.commit() 
    connection.close()
    if row == "name_list":
        return documentos[0]
    elif row == "tidy_list":
        return documentos[1]
    elif row == "path_folder":
        return documentos[2]
    elif row == "all":
        return documentos

# modify
def select_id_for_name(name):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    cursor.execute("SELECT oid FROM tidytable WHERE name_list = :name_list", {'name_list': name})
    results = str(cursor.fetchall())
    results = results.replace("[(", '').replace(",)]", '')
    connection.commit()
    connection.close()
    return results

# origin - program
def select_origin_path(folder_name, option):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()   
    cursor.execute('SELECT path_folder FROM origin WHERE folder_name="tidyup"')
    if option == "string":
        results = str(cursor.fetchall())
        results = results.replace("[('", '').replace("',)]", '')
        results = os.path.normpath(results)
    elif option == "list":
        results = list(cursor.fetchall())
    connection.commit()
    connection.close()
    return results

# showLists
def select_list(table):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    if table == "tidytable":
        cursor.execute("SELECT *, oid FROM tidytable")
    elif table == "origin":
        cursor.execute("SELECT *, oid FROM origin")    
    results = list(cursor.fetchall())
    connection.commit()
    connection.close()
    return results

# fuera/search/in_database
def select_for_query(user_query):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tidytable WHERE name_list LIKE '%'||?||'%' OR tidy_list LIKE '%'||?||'%' OR  path_folder LIKE '%'||?||'%'", (user_query, user_query, user_query))
    results = list(cursor.fetchall())
    connection.commit()
    connection.close()
    return results

# program
def select_path_for_tidies(tidy):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    cursor.execute("SELECT path_folder FROM tidytable WHERE tidy_list LIKE '%'||?||'%'", (tidy,) )
    results = str(cursor.fetchall())
    results = results.replace("[('", '').replace("',)]", '')
    results = os.path.normpath(results)
    # Convert str to a list type
    results = results.split(" ")
    results = results[-1].replace("('", '') # Clean last result.
    connection.commit()
    connection.close()    
    return results

# UPDATE

# modify
def update(id_list, name, tidies, path):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    cursor.execute("""UPDATE tidytable SET 
                   name_list = :new_name, 
                   tidy_list = :tidies, 
                   path_folder = :new_path 
                   WHERE oid = :id_list""",
                   {
                       'new_name': name, 
                       'tidies': tidies,
                       'new_path': path,
                       'id_list': id_list
                       })    
    connection.commit()
    connection.close() 

# origin
def update_origin_path(name_folder, folder_path):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    cursor.execute(""" UPDATE origin SET path_folder = :path_folder WHERE folder_name = :name_folder""",
                   {
                       'path_folder': folder_path,
                       'name_folder': name_folder
                        })
    connection.commit()
    connection.close()

# DELETE

# delete
def delete(id_list):
    connection = sqlite3.Connection('tidyup.db')
    cursor = connection.cursor()
    cursor.execute("SELECT oid FROM tidytable WHERE oid = " + id_list)
    results = str(cursor.fetchall())
    # Clean a str
    r={'[':'',']':'',"'":'', ',':'','(':'',')':'','"':''}
    results = ''.join(r.get(s,s) for s in results)
    # Convert str to a list type
    results = list(results.split(" "))
    for x in results:
        if x == id_list:
            cursor.execute("DELETE FROM tidytable WHERE oid = " + id_list)
            connection.commit()
            connection.close()
            return True
    else:
        connection.commit()
        connection.close()
        return False