import os
import sys
from contextlib import contextmanager
import time
import ctypes



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

clear = lambda: os.system('cls')