### Main script.

from utils.orth_base import *

clear()
ui = ['Information about novell build', 'Run novell build']

print('Welcome to 1Ren2Hack.')
print('')
print('Select what you need:')

for x,i in enumerate(ui):
    print(f'    [{x+1}] {i}')

print('')
result = input()

if result == '':
    clear()
    exit()

exit()