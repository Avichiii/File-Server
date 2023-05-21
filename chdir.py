import os
PATH = r'C:\Users\abhijit Dey\OneDrive\Desktop\file_server'

os.chdir(f'{PATH}\\serverFiles')
PATH = os.getcwd() # NEW PATH
with open(f'{PATH}\\file8.txt', 'r') as f:
    s = f.read()
    print(s)

os.chdir('..') # revert

print(os.getcwd())
