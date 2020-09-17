import threading
from main.gui import interface
from tools.utils import exit
from tools.utils import messagebox
from tools.utils import check
import main.program as tidyup
import tools.constant as c

if __name__ == "__main__":
    try:  
        window = c.WINDOW
        window.resizable(False, False)
        window.title("Tidyup")
        window.iconbitmap('.\logo.ico')
        window.geometry(c.WINDOW_SIZE)
        window.configure(bg=c.BACKGROUND_COLOR)
        window.protocol('WM_DELETE_WINDOW', lambda:[exit.program(c.WINDOW)])
        interface.list_box()
        interface.origen()
        threading.Thread(target=tidyup.program).start()      
    except Exception as error:
        messagebox.error(error)    
    window.mainloop()