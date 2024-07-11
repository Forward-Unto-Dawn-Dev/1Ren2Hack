import os
import sys
from contextlib import contextmanager
import time
from tkinter.filedialog import askdirectory
from tkinter import *
import io
import os
import pickle
import pickletools
import re
import struct
import zlib
import renpy.ast
import renpy.sl2.slast
import renpy.util

RPYC2_HEADER = b"RENPY RPC2"

class RPYCD():
    def write_file(filename: str, data: str):
        "Write data to file."

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, "w", encoding="utf-8") as file:
            file.write(data)

    def match_files(base_dir: str, pattern: str) -> list[str]:
        "Match files in dir with regex pattern."

        if pattern == "":
            pattern = ".*"
        results = []
        matched = re.compile(pattern)
        for root, _, files in os.walk(base_dir):
            for filename in files:
                filename = os.path.relpath(os.path.join(root, filename), base_dir)
                if matched.match(filename):
                    results.append(filename)
        return results

    def read_rpyc_data(file: io.FileIO, slot):
        "Reads the binary data from `slot` in a .rpyc file. Returns the data if the slot exists, or None if the slot does not exist."

        file.seek(0)
        header_data = file.read(1024)
        if header_data[: len(RPYC2_HEADER)] != RPYC2_HEADER:
            if slot != 1:
                return None
            file.seek(0)
            data = file.read()
            return zlib.decompress(data)
        pos = len(RPYC2_HEADER)
        while True:
            header_slot, start, length = struct.unpack("III", header_data[pos : pos + 12])
            if slot == header_slot:
                break
            if header_slot == 0:
                return None
            pos += 12
        file.seek(start)
        data = file.read(length)
        return zlib.decompress(data)

    def load_file(filename, disasm: bool = False) -> renpy.ast.Node:
        "Load Ren'Py code from RPYC file and return AST tree."

        ext = os.path.splitext(filename)[1]
        if ext in [".rpy", ".rpym"]:
            raise NotImplementedError(
                "Unsupport for pase RPY file or use renpy.parser.parse() in Ren'Py SDK."
            )
        if ext in [".rpyc", ".rpymc"]:
            with open(filename, "rb") as file:
                for slot in [1, 2]:
                    bindata = RPYCD.read_rpyc_data(file, slot)
                    if bindata:
                        if disasm:
                            disasm_file = filename + ".disasm"
                            with open(disasm_file, "w", encoding="utf-8") as disasm_f:
                                pickletools.dis(bindata, out=disasm_f)
                        _, stmts = pickle.loads(bindata)
                        return stmts
                    file.seek(0)
        return None

    def decompile_file(input_file, output_file=None):
        "decompile rpyc file into rpy file and write to output."

        if not output_file:
            output_file = input_file.removesuffix("c")
        if not output_file.endswith(".rpy"):
            output_file = os.path.join(
                output_file, os.path.basename(input_file).removesuffix("c")
            )
        stmts = RPYCD.load_file(input_file)
        code = renpy.util.get_code(stmts)
        RPYCD.write_file(output_file, code)

    def decompile_file_return(input_file, output_file=None):
        "Decompile RPYC file into output."

        if not output_file:
            output_file = input_file.removesuffix("c")
        if not output_file.endswith(".rpy"):
            output_file = os.path.join(
                output_file, os.path.basename(input_file).removesuffix("c")
            )
        stmts = RPYCD.load_file(input_file)
        code = renpy.util.get_code(stmts)
        return code

    def decompile(input_path, output_path=None):
        "Decompile RPYC file or directory into RPY."
        
        if not os.path.isdir(input_path):
            RPYCD.decompile_file(input_path, output_path)
            return
        if not output_path:
            output_path = input_path
        for filename in RPYCD.match_files(input_path, r".*\.rpym?c$"):
            RPYCD.decompile_file(
                os.path.join(input_path, filename),
                os.path.join(output_path, filename.removesuffix("c")),
            )

class Path():
    def getpath():
        "Creates a window for selecting a path. Used in conjunction with a variable to save."
        window = Tk()
        window.withdraw()
        path = askdirectory(parent=window, title='Select path')
        return path
    def checkpath(path):
        needed = ['renpy','lib','game']
        dir = path
        if dir.endswith('game'):
            with except_handler(err):
                raise Exception('You selected a "game" directory! Please select a ROOT path (i.e. without "/game").')
        dir_list = os.listdir(dir)
        check_needed = set(needed).issubset(dir_list)
        if not check_needed:
            with except_handler(err):
                raise Exception("I can't find the novell in this folder as there is no 'renpy', 'lib' and 'game' folders. So you're either trying to open your Ren'Py project, or this folder is not a novell folder. Try again.")

@contextmanager
def except_handler(exc_handler):
    "Modified exception output module handler."
    sys.excepthook = exc_handler
    yield
    sys.excepthook = sys.__excepthook__

def err(type, value, traceback):
    "New type of exception."
    print(': '.join([str(type.__name__), str(value)]))
    print("~ Oops! I'll leave you with an error, mane. ~")
    errwait()
    print("")
def errwait():
    "A simple 1-second pause after outputting an error."
    time.sleep(1)

def clear():
    "Clears the command line."
    os.system('cls')