### Main script.

from utils.orth_base import *
f_firstrun = f"{os.path.dirname(__file__)}/!firstrun"

if not os.path.exists(f_firstrun):
    with open(f_firstrun, 'w') as fp:
        pass
    print('\nFirst run detected.\n\nAttempting installing requirements...')
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
    print('Success.')
    time.sleep(1)

while True:
    clear()

    print('Welcome to 1Ren2Hack.')
    print('')
    result = menu("result", "Select an option", ["Information about novell build (+ CHP Module)", "Tweaks", "Close 1Ren2Hack"])

    print()

    if not result:
        break

    if result.get("result") == "Information about novell build (+ CHP Module)":
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
        if gamedir == '' or gamedir == ():
            continue
        Path.checkpath(gamedir)
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
                    with except_handler(err):
                        raise Exception('(RPYC) Decompile error: {0}'.format(e))
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
                    with except_handler(err):
                        raise Exception('(RPA + RPYC) Decompile error: {0}'.format(e))
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
        wait(1)
        CHP(gamedir, options_result)
        wait(1)
        answer = confirm("answer", "Are you want to return back?")
        if answer.get("answer") == "Yes":
            _answer = True
            _gamedir = gamedir
            continue
        else:
            clear()
            break
    
    if result.get("result") == "Tweaks":
        print("This option doesn't work yet! :(\n")
        wait(1)
        answer = confirm("answer", "Are you want to return back?")
        if answer.get("answer") == "Yes":
            continue
        else:
            clear()
            break
    
    if result.get("result") == "Close 1Ren2Hack":
        break