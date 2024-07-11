### Main script.

from utils.orth_base import *

while True:
    clear()
    ui = ['Information about novell build', 'Run novell build']
    func_enum = []
    func_names = []

    print('Welcome to 1Ren2Hack.')
    print('')
    print('Select what you need:')

    for x,i in enumerate(ui):
        func_enum.append(x)
        func_names.append(i)
        print(f'    [{func_enum[x]}] {i}')

    print('')
    result = input()
    func_enum = str(func_enum)

    if result not in func_enum:
        clear()
        exit()

    if result == '0':
        print('Select path to novell.')
        dir = Path.getpath()
        if dir == '':
            continue
        Path.checkpath(dir)
        dir_flist = os.listdir(dir+'/game/')
        print('...')
        print('')
        try:
            if os.path.exists(dir+'/game/options.rpy'):
                options = open(dir+'/game/options.rpy').read()
                options_split = options.splitlines()
                options_result = IANB.opt_check(options_split)
            elif os.path.exists(dir+'/game/options.rpyc'):
                try:
                    options = RPYCD.decompile_file_return(dir+'/game/options.rpyc')
                except Exception as e:
                    with except_handler(err):
                        raise Exception('Decompile error: {0}'.format(e))
                options_split = options.splitlines()
                options_result = IANB.opt_check(options_split)
            else:
                for i in dir_flist:
                    if i.endswith('.rpa'):
                        try:
                            options = rpa.RenPyArchive(dir+'/game/'+i,version=3.2).read("options.rpyc")
                        except Exception as e:
                            pass
                with open("cache/temp_{0}.rpyc".format(date.now().strftime('%Y-%m-%d %H:%M:%S').strip().replace(':','-')), "wb") as f:
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
                options_result = IANB.opt_check(options_result)
        except:
            options_result = IANB.opt_check('0')
        if os.path.exists(dir+'/renpy/common/00console_RulesWereMadeToBeBroken.rpy'):
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
            print('Are you want to: Enable Developer Mode? (y/n)')
            answer = input().lower()
            if answer == 'y':
                console = dir+'/renpy/common/00console.rpy'
                console_c = dir+'/renpy/common/00console.rpyc'
                if os.path.exists(console):
                    os.remove(console)
                if os.path.exists(console_c):
                    os.remove(console_c)
                shutil.copy('utils/00console.rpy',dir+'/renpy/common/00console_RulesWereMadeToBeBroken.rpy')
                print('Done.')
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
