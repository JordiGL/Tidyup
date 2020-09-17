from tkinter import  *
from tools.utils import window_position 
from ttkthemes import  ThemedTk

# Control program (start, stop)
PROGRAM = False
# Program window
WINDOW = ThemedTk(theme="plastik")
SIZE = "483x200"
WINDOW_SIZE = (SIZE + window_position.apply())
WINDOW_SIZE_FOR_MODIFY = ("482x280")
# GUI window
BACKGROUND_COLOR = "SlateGray2"
BUTTON_COLOR = "gray82"
BUTTON_ACTIVE_COLOR = "gray90"
# Label frames
LIST_FRAME = LabelFrame(WINDOW, bg = BACKGROUND_COLOR, highlightthickness = 0, borderwidth = 0)
MODIFY_FRAME = Frame(LIST_FRAME, bg = BACKGROUND_COLOR)
# Modify boxes for user input
NAME_BOX = Entry(MODIFY_FRAME, width = 46)
TIDIES_BOX = Entry(MODIFY_FRAME, width = 46)
PATH_BOX = Entry(MODIFY_FRAME, width = 46)
SEARCH_BOX = Entry(LIST_FRAME, width = 29)
# Global id list
ID_LIST = "" # ID of the list for modify.
