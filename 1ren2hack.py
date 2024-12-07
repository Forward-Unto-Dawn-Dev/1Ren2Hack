### Main script.

from utils.orth_base import *

while True:
    clear()

    print('Welcome to 1Ren2Hack.\n')
    result = menu("result", "Select an option", ["Info about novell build (+ Console Hack Patch Module)", "RPYC Decompiler", "RPA Packer/Unpacker", "Saves Editor", "Engine Files Editor", "Close 1Ren2Hack"])

    print()

    if not result: break

    if result.get("result") == "Info about novell build (+ Console Hack Patch Module)":
        if '_answer' and '_gamedir' in locals():
            if _answer:
                _answer = confirm("_answer", "Do you want to use the last open path?")
                if _answer.get("_answer") == "Yes":
                    pass
                else:
                    print('Select path to novell.')
                    gamedir = Path.getpath()
                    if gamedir == '' or gamedir == ():
                        gamedir = _gamedir
        else:
            print('Select path to novell.')
            gamedir = Path.getpath()
        if gamedir in ['', ()]:
            continue
        Path.checkpath(gamedir, ['renpy','lib','game'])
        dir_flist = os.listdir(gamedir+'/game/')
        print()
        try:
            if os.path.exists(gamedir+'/game/options.rpy'):
                options = open(gamedir+'/game/options.rpy').read()
                options_split = options.splitlines()
                options_result = VCHECK.opt_check(options_split)
            elif os.path.exists(gamedir+'/game/options.rpyc'):
                try:
                    options = RPYCD.decompile_file_return(gamedir+'/game/options.rpyc')
                except Exception as e:
                    print('(RPYC) Decompile error: {0}'.format(e))
                options_split = options.splitlines()
                options_result = VCHECK.opt_check(options_split)
            else:
                for i in dir_flist:
                    if i.endswith('.rpa'):
                        try:
                            options = rpa.RenPyArchive(gamedir+'/game/'+i).read("options.rpyc")
                        except Exception as e:
                            pass
                with open("{0}/cache/temp_{1}.rpyc".format(os.path.dirname(__file__),datenow), "wb") as f:
                    f.write(options)
                    fname = f.name
                    f.close()
                try:
                    options = RPYCD.decompile_file_return(fname)
                except Exception as e:
                    print('(RPA + RPYC) Decompile error: {0}'.format(e))
                os.remove(fname)
                options_result = options.splitlines()
                options_result = VCHECK.opt_check(options_result)
        except Exception as e:
            print(e)
            options_result = VCHECK.opt_check('0')
        if os.path.exists(gamedir+'/renpy/common/00console_RulesWereMadeToBeBroken.rpy'):
            options_result[3] = '*1R2H* Hacked.'
        
        print('----------------------------------------------------------------')
        print()
        print(f'BUILD NAME:     {options_result[0]}')
        print(f'NAME:           {options_result[1]}')
        print(f'VERSION:        {options_result[2]}')
        print(f'DEVELOPER MODE: {options_result[3]}')
        print()
        print('----------------------------------------------------------------')
        print()
        print()
        CHP(gamedir, options_result)
        answer = confirm("answer", "Are you want to return back?")
        if answer.get("answer") == "Yes":
            _answer = True
            _gamedir = gamedir
            continue
        else:
            clear()
            break

    if result.get("result") == "RPYC Decompiler":
        print('Select RPYC file(s).')
        files_paths = Path.getfile()
        if files_paths in ['', ()]:
            continue
        print('Select directory to extract.')
        extract_path = Path.getpath()
        if extract_path in ['', ()]:
            continue
        for i in files_paths:
            if i.split("/")[-1].split(".")[-1] != "rpyc":
                print(f"!!! Skipped extracting: \"{extract_path}/{i.split("/")[-1]}\". NOT A RPYC FILE.")
            elif os.path.exists(f"{extract_path}/{i.split("/")[-1].replace("rpyc", "rpy")}"):
                print(f"!!! Skipped extracting: \"{extract_path}/{i.split("/")[-1]}\". RPY FILE WITH THIS NAME ALREADY EXISTS.")
            else:
                print(f"Extracting: \"{extract_path}/{i.split("/")[-1]}\"...")
                RPYCD.decompile_file(i, extract_path)
        print("\nDecompiling completed!")
        answer = confirm("answer", "Are you want to return back?")
        if answer.get("answer") == "Yes":
            continue
        else:
            clear()
            break
    
    if result.get("result") == "Close 1Ren2Hack":
        clear()
        break

    else:
        print("This option is not exists.\n")
        answer = confirm("answer", "Are you want to return back?")
        if answer.get("answer") == "Yes":
            continue
        else:
            clear()
            break