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

if result == '1':
    print('Select path to your novell.')
    dir = getpath()
    print(dir)

exit()