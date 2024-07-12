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
import platform
import shutil
import utils.rpatool as rpa
from datetime import datetime as date

RPYC2_HEADER = b"RENPY RPC2"
datenow = date.now().strftime('%Y-%m-%d %H:%M:%S').strip().replace(':','-')

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

class IANB():
    def opt_check(var):
        opt_build_name = '*1R2H* Unknown value.'
        opt_config_name = '*1R2H* Unknown value.'
        opt_config_version = '*1R2H* Unknown value.'
        opt_config_developer = '*1R2H* Unknown value.'
        for i in var:
            i = i.split('=')
            if 'define build.name' in i[0]:
                opt_build_name = i[1]
                opt_build_name = opt_build_name.strip()
            if 'define config.name' in i[0]:
                opt_config_name = i[1]
                opt_config_name = opt_config_name.strip()
            if 'define config.version' in i[0]:
                opt_config_version = i[1]
                opt_config_version = opt_config_version.strip()
            if 'define config.developer' in i[0]:
                opt_config_developer = i[1]
                opt_config_developer = opt_config_developer.strip()
        return [opt_build_name,
                opt_config_name,
                opt_config_version,
                opt_config_developer]

class CHP():
    """
    Console Hacking Patch is the first 1Ren2Hack technology
    that allows you to hack absolutely any novel with a Developer Console patch.
    """
    def __init__(self, gamedir, options_result):
        self.gamedir = gamedir
        self.console = '{0}/renpy/common/00console.rpy'.format(gamedir)
        self.console_c = '{0}/renpy/common/00console.rpyc'.format(gamedir)
        self.options_result = options_result
        self.newcmd = """
    @command(_("onerentohack: send hacking method output"))
    def onerentohack(l):
        return 'Thank you for using 1Ren2Hack. Lead, suck my dick! (By: tetyastan. vk.com/tetyastan)'\n"""
    def hack(self):
        console = '{0}/renpy/common/00console.rpy'.format(self.gamedir)
        console_c = '{0}/renpy/common/00console.rpyc'.format(self.gamedir)
        console_rename = '{0}/renpy/common/00console_RulesWereMadeToBeBroken.rpy'.format(self.gamedir)
        if os.path.exists(console):
            shutil.copy(console, "backup/00console_{0}_{1}.rpy".format(self.options_result[0].strip().replace('"',''),datenow))
            if os.path.exists(console_c):
                os.remove(console_c)
            self._consolePatch()
        elif os.path.exists(console_c):
            console_c_dcp = RPYCD.decompile_file_return(console_c)
            shutil.copy(console_c, "backup/00console_{0}_{1}_decompiled.rpy".format(self.options_result[0].strip().replace('"',''),datenow))
            os.remove(console_c)
            with open(console, 'w') as f:
                f.write(console_c_dcp)
            self._consolePatch()
        os.rename(console,console_rename)
    def _consolePatch(self):
        with open(self.console) as f:
            lines = f.readlines()
        with open(self.console,"w") as f:
            for line in lines:
                if not re.search('if config.developer or config.console:',line):
                    f.write(line)
                if re.search('return "Saved slot',line):
                    f.write(self.newcmd)
            f.close()

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
def wait(i):
    "A simple X-second pause."
    time.sleep(i)

def clear():
    "Clears the command line."
    if platform.system() == "Windows":
        os.system('cls')
    elif platform.system() == "Linux":
        os.system('clear')
    else:
        pass