from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import database.db as db
import main.program as p
import os
import time
import tools.constant as c

class MyHandler(FileSystemEventHandler):
    
    def __init__(self):
        if c.PROGRAM:
            MyHandler.remitent()  
        
    def on_modified(self, event):
        if c.PROGRAM:
            MyHandler.remitent()           

    def remitent():
        try:
            origin_path = db.select_origin_path("tidyup", "string")
            for file in os.listdir(origin_path):
                src = origin_path + '\\' + file
                src = os.path.normpath(src)
                new_destination = MyHandler.assign_destination(file)
                if new_destination != 'Tidy sin lista':
                    os.rename(src, new_destination)
        except FileNotFoundError:
            pass             

    def assign_destination(file):
        name, extension = os.path.splitext(file)
        possible_tidy, separator, after = name.partition("_")   
        if db.check_value("tidy_list", possible_tidy) > 0:
            print(possible_tidy) 
            confirmed_tidy = possible_tidy
            destination = os.path.normpath(db.select_path_for_tidies(confirmed_tidy))
            new_destination = os.path.normpath(destination + '\\' + file)
            confirmed_destination = MyHandler.checking_file(destination, new_destination, file)
            return confirmed_destination
        elif db.check_value("tidy_list", extension.lower()) > 0:
            destination = os.path.normpath(db.select_path_for_tidies(extension))       
            new_destination = os.path.normpath(destination + '\\' + file)
            confirmed_destination = MyHandler.checking_file(destination, new_destination, file)
            return confirmed_destination
        else:
            return "Tidy sin lista"
    
    def checking_file(destination, new_destination, file):
        if os.path.exists(new_destination):
            new_destination = destination + '\\copy_' + file
            return new_destination
        return new_destination   
    
def program():   
    # Running the program
    origin_path = os.path.normpath(db.select_origin_path("tidyup", "string"))
    event_handler = p.MyHandler()
    observer = Observer()
    observer.schedule(event_handler, origin_path, recursive=True)
    observer.start()
    # Exception
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join   
