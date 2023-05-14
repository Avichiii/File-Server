PATH = r'C:\Socket Programming\file_server'
for i in range(10000):
    with open(f'{PATH}\\file2.txt', 'a') as file:
        file.write('this is sparta.\n')