### Main script.

from utils.orth_base import *

while True:
    clear()
    ui = ['Information about novell build (+ CHP Module)', 'Tweaks']
    func_enum = []
    func_names = []

    print('Welcome to 1Ren2Hack.')
    print('')
    print('Select what you need:')

    for x,i in enumerate(ui):
        func_enum.append(x)
        func_names.append(i)
        print(f'    [{func_enum[x]}] {i}')
    print()
    print('    [SMTH ELSE] Exit program')

    print()
    result = input()
    func_enum = str(func_enum)

    if result not in func_enum:
        clear()
        exit()

    if result == '0':
        if '_answer' and '_gamedir' in locals():
            if _answer:
                _answer = input('Do you want to use the last open path? (y/n)\n')
                if _answer.lower() == 'y':
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
        print('Are you want to return back? (y/n)')
        answer = input().lower()
        if answer == 'y':
            _answer = True
            _gamedir = gamedir
            continue
        else:
            clear()
            break
    
    if result == '1':
        print('TEST')
        wait(1)
        print('Are you want to return back? (y/n)')
        answer = input().lower()
        if answer == 'y':
            continue
        else:
            clear()
            break