### Main script.

from utils.orth_base import *

while True:
    clear()
    ui = ['Information about novell build (+ CHP Module)', 'Run novell build']
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
        print('Select path to novell.')
        gamedir = Path.getpath()
        if gamedir == '':
            continue
        Path.checkpath(gamedir)
        dir_flist = os.listdir(gamedir+'/game/')
        print('...')
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
                        raise Exception('Decompile error: {0}'.format(e))
                options_split = options.splitlines()
                options_result = VCHECK.opt_check(options_split)
            else:
                for i in dir_flist:
                    if i.endswith('.rpa'):
                        try:
                            options = rpa.RenPyArchive(gamedir+'/game/'+i,version=3.2).read("options.rpyc")
                        except Exception as e:
                            pass
                with open("cache/temp_{0}.rpyc".format(datenow), "wb") as f:
                    f.write(options)
                    fname = f.name
                    f.close()
                try:
                    options = RPYCD.decompile_file_return(fname)
                except Exception as e:
                    with except_handler(err):
                        raise Exception('Decompile error: {0}'.format(e))
                os.remove(fname)
                options_result = options.splitlines()
                options_result = VCHECK.opt_check(options_result)
        except:
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
        if options_result[3] in ['False','*1R2H* Unknown value.']:
            print('Are you want to: Enable Developer Mode? (y/n)\nWARNING: Save the "renpy" folder as a backup before patching! The patch will overwrite the files, which may cause the engine files to crash.')
            answer = input().lower()
            if answer == 'y':
                if options_result[0] == '*1R2H* Unknown value.':
                    options_result[0] = 'UNKNOWN_VALUE'
                CHP(gamedir, options_result).hack()
                print("""
            Done!
            
            If for some reason the game doesn't work (won't start, gives an error, etc.):
            
            1. Rename the file from the backup folder with a name starting with '00console' to '00console.rpy'.
            2. Move the file to the following path in the game:
                    [ur_game_folder]/renpy/common.
            3. Remove the files from the above directory:
                00console_RulesWereMadeToBeBroken.rpy
                00console_RulesWereMadeToBeBroken.rpyc (if exists)""")
        else:
            pass
        wait(1)
        print('Are you want to return back? (y/n)')
        answer = input().lower()
        if answer == 'y':
            continue
        else:
            clear()
            break
