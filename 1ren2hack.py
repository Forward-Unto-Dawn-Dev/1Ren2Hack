### Main script.

from utils.orth_base import *

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
    print('...')
    print('')
    Path.checkpath(dir)
    if os.path.exists(dir+'/game/options.rpyc'):
        options = RPYCD.decompile_file_return(dir+'/game/options.rpyc')
        opt_config_name = re.search('config.name = "(.*?)"', options).group(1)
    else:
        opt_config_name = 'Unknown Novell'
    print('----------------------------------------------------------------')
    print()
    print(f'NOVELL NAME: {opt_config_name}')
    print()
    print('----------------------------------------------------------------')

exit()