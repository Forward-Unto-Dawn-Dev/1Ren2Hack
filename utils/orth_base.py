import os
from contextlib import contextmanager
from tkinter.filedialog import askdirectory, askopenfilenames
from tkinter import *
import io
import os
import pickle
import pickletools
import re
import struct
import zlib
import utils.RPYCDecompiler.ast as ast
import utils.RPYCDecompiler.util as rpycd_u
import platform
import shutil
import inquirer
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

    def load_file(filename, disasm: bool = False) -> ast.Node:
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
        code = rpycd_u.get_code(stmts)
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
        code = rpycd_u.get_code(stmts)
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

# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Ren'Py archiver. This builds a Ren'Py archive file, and the
# associated index file. These files are really easy to
# reverse-engineer, but are probably better than nothing.

import zlib

from pickle import dumps, HIGHEST_PROTOCOL


class RPAPU(object):
    """
    Adds files from disk to a rpa archive.
    """

    def __init__(self, filename):

        self.python_dict = self._dict = dict
        self.python_list = self._list = list

        # The archive file.
        self.f = open(filename, "wb")

        # The index to the file.
        self.index = self._dict()

        # A fixed key minimizes difference between archive versions.
        self.key = 0x42424242

        padding = b"RPA-3.0 XXXXXXXXXXXXXXXX XXXXXXXX\n"
        self.f.write(padding)

    def add(self, name, path):
        """
        Adds a file to the archive.
        """

        self.index[name] = self._list()

        with open(path, "rb") as df:
            data = df.read()
            dlen = len(data)

        # Pad.
        padding = b"Made with Ren'Py."
        self.f.write(padding)

        offset = self.f.tell()

        self.f.write(data)

        self.index[name].append((offset ^ self.key, dlen ^ self.key, b""))

    def close(self):

        indexoff = self.f.tell()

        self.f.write(zlib.compress(dumps(self.index, HIGHEST_PROTOCOL)))

        self.f.seek(0)
        self.f.write(b"RPA-3.0 %016x %08x\n" % (indexoff, self.key))

        self.f.close()

class Path():
    def getfile():
        "Creates a window for selecting a file(s). Used in conjunction with a variable to save."
        window = Tk()
        window.withdraw()
        paths = askopenfilenames(parent=window, title='Select file(s)')
        return paths
    def getpath():
        "Creates a window for selecting a path. Used in conjunction with a variable to save."
        window = Tk()
        window.withdraw()
        path = askdirectory(parent=window, title='Select path')
        return path
    def checkpath(path, needed):
        "Checking the path for engine and novel files."
        if path.endswith('game'):
            print("WARN: You selected a \"game\" directory! Please select a ROOT path (i.e. without \"/game\").")
        for i in needed:
            if i not in os.listdir(path):
                print(f"WARN: Can't find engine folder: {i}.")

class VCHECK():
    """
    VCHECK is a special function to check files for required variables.
    """
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
        self.console_rename = '{0}/renpy/common/00console_RulesWereMadeToBeBroken.rpy'.format(gamedir)
        self.dev = '{0}/renpy/common/_developer/developer.rpym'.format(gamedir)
        self.dev_rename = '{0}/renpy/common/_developer/developer.rpy'.format(gamedir)
        self.dev_c = '{0}/renpy/common/_developer/developer.rpymc'.format(gamedir)
        self.options_result = options_result
        self.newcmd = """
    @command(_("onerentohack: meet the POWER!"))
    def onerentohack(l):
        return 'Thank you for using 1Ren2Hack. By: tetyastan. vk.com/tetyastan'\n"""
        self.hack()

    def hack(self):
        if not os.path.exists(self.console) and not os.path.exists(self.console_c):
            print("Can't use Console Hacking Patch.")
            return
        if self.options_result[3] in ['False','*1R2H* Unknown value.']:
            print('Are you want to use Console Hacking Patch? (y/n)\nWARNING: Save the "renpy" folder as a backup before patching! The patch will overwrite the files, which may cause the engine files to crash.')
            answer = input().lower()
            if answer == 'y':
                if self.options_result[0] == '*1R2H* Unknown value.':
                    self.options_result[0] = 'UNKNOWN_VALUE'
                else:
                    pass
                pass
            else:
                return
        print()
        if os.path.exists(self.console):
            shutil.copy(self.console, "backup/00console_{0}_{1}.rpy".format(self.options_result[0].strip().replace('"',''),datenow))
            if os.path.exists(self.console_c):
                os.remove(self.console_c)
            self._consolePatch()
            os.rename(self.console,self.console_rename)
        elif os.path.exists(self.console_c):
            console_c_dcp = RPYCD.decompile_file_return(self.console_c)
            shutil.copy(self.console_c, "backup/00console_{0}_{1}_decompiled.rpy".format(self.options_result[0].strip().replace('"',''),datenow))
            os.remove(self.console_c)
            with open(self.console, 'w') as f:
                f.write(console_c_dcp)
            self._consolePatch()
            os.rename(self.console,self.console_rename)
        if os.path.exists(self.dev):
            shutil.copy(self.dev, "backup/developer_{0}_{1}.rpy".format(self.options_result[0].strip().replace('"',''),datenow))
            if os.path.exists(self.dev_c):
                os.remove(self.dev_c)
            os.rename(self.dev,self.dev_rename)
        elif os.path.exists(self.dev_c):
            dev_c_dcp = RPYCD.decompile_file_return(self.dev_c)
            shutil.copy(self.dev_c, "backup/developer_{0}_{1}_decompiled.rpy".format(self.options_result[0].strip().replace('"',''),datenow))
            os.remove(self.dev_c)
            with open(self.dev_rename, 'w') as f:
                f.write(dev_c_dcp)
        if answer == 'y':
            print("""
    Done! Now you can use Shift+O in this game build to open console.
    
    If for some reason the game doesn't work (won't start, gives an error, etc.):
    
    1. Rename the file from the backup folder with a name starting with '00console' to '00console.rpy'.
    2. Move the file to the following path in the game:
            [ur_game_folder]/renpy/common.
    3. Remove the files from the above directory:
        00console_RulesWereMadeToBeBroken.rpy
        00console_RulesWereMadeToBeBroken.rpyc (if exists)""")
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

def menu(key,msg,choices):
    "Using Inquirer to create a menu."
    x = inquirer.prompt([inquirer.List(
                            key,
                            message=msg,
                            choices=choices,
                            )])
    return x

def confirm(key,msg):
    x = menu(key, msg, ["Yes", "No"])
    return x
def clear():
    "Clears the command line."
    if platform.system() == "Windows":
        os.system('cls')
    elif platform.system() == "Linux":
        os.system('clear')
    else:
        pass