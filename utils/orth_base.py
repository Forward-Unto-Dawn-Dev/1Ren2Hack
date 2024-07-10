import os
import sys
from contextlib import contextmanager
import time
import ctypes
from tkinter.filedialog import askdirectory
from tkinter import *

def getpath():
    "Creates a window for selecting a path. Used in conjunction with a variable to save."
    window = Tk()
    window.withdraw()
    path = askdirectory(parent=window, title='Select path to your novell')
    return path

def errwait():
    "A simple 1-second pause after outputting an error."
    time.sleep(1)

@contextmanager
def except_handler(exc_handler):
    "Modified exception output module handler."
    sys.excepthook = exc_handler
    yield
    sys.excepthook = sys.__excepthook__

def err(type, value, traceback):
    "New type of exception."
    print(': '.join([str(type.__name__), str(value)]))
    print("Oops! I'll leave you with an error, mane.")
    errwait()
    print("")

def clear():
    "Clears the command line."
    os.system('cls')