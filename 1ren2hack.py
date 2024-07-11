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
        if os.path.exists(dir+'/game/options.rpyc'):
            try:
                options = RPYCD.decompile_file_return(dir+'/game/options.rpyc')
            except Exception as e:
                with except_handler(err):
                    raise Exception('Decompile error: {0}'.format(e))
            options = options.splitlines()
            options = IANB.opt_check(options)
        elif os.path.exists(dir+'/game/options.rpy'):
            options = open(dir+'/game/options.rpy').read()
            options = options.splitlines()
            options = IANB.opt_check(options)
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
            options = options.splitlines()
            options = IANB.opt_check(options)
            os.remove(fname)
        
        print('----------------------------------------------------------------')
        print()
        print(f'BUILD NAME:     {options[0]}')
        print(f'NAME:           {options[1]}')
        print(f'VERSION:        {options[2]}')
        print(f'DEVELOPER MODE: {options[3]}')
        print()
        print('----------------------------------------------------------------')
        print()
        print()
        wait(1)
        if options[3] in ['False','*1R2H* Unknown value.']:
            print('Are you want to: Enable Developer Mode? (y/n)')
            answer = input().lower()
            if answer == 'y':
                temp_path_file = "backup/options_{0}_backup.rpy".format(options[0].strip('"'))
                if os.path.exists(temp_path_file):
                    os.remove(temp_path_file)
                with open(temp_path_file,"a+", encoding="utf-8") as backup:
                    options = RPYCD.decompile_file_return(dir+'/game/options.rpyc')
                    backup.write(options)
                    os.remove(dir+'/game/options.rpyc')
                print()
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
